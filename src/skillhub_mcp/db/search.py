import json
import sys
from typing import List, Optional, Any, Dict

import lancedb

from .embeddings import get_embedding
from .models import SkillRecord
from ..config import settings
from ..utils import parse_frontmatter


class SkillDB:
    def __init__(self):
        self.db_path = settings.get_effective_db_path()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.db = lancedb.connect(self.db_path)
        self.table_name = "skills"
        self._normalize = lambda q: " ".join(q.strip().split())

    # --- Normalization helpers ---
    def _norm_token(self, value: str) -> str:
        """Lowercase + trim for category/tags normalization."""
        return " ".join(str(value).strip().split()).lower()

    def _escape_sql_string(self, value: str) -> str:
        """Basic SQL escaping for string literals."""
        return value.replace("'", "''")

    # --- Table helpers ---
    def _get_table(self):
        if self.table_name in self.db.table_names():
            return self.db.open_table(self.table_name)
        return None

    def _build_prefilter(self) -> str:
        """
        Constructs a SQL WHERE clause based on enabled skills/categories settings.
        Mirrors is_skill_enabled logic:
        1) If skills specified: restrict to names.
        2) Else if categories specified: restrict to categories.
        3) Else: no filter.
        """
        if settings.skillhub_enabled_skills:
            safe_skills = [f"'{self._escape_sql_string(s)}'" for s in settings.skillhub_enabled_skills]
            return f"name IN ({', '.join(safe_skills)})"

        if settings.skillhub_enabled_categories:
            safe_cats = [f"'{self._escape_sql_string(self._norm_token(c))}'" for c in settings.skillhub_enabled_categories]
            return f"category IN ({', '.join(safe_cats)})"

        return ""

    # --- Index lifecycle ---
    def initialize_index(self):
        """Scans SKILLS_DIR and (re)creates the index."""

        # Fail fast if embeddings are requested but credentials are missing.
        if settings.embedding_provider == "openai" and not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when embedding_provider='openai'")
        if settings.embedding_provider == "gemini" and not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY or GOOGLE_API_KEY is required when embedding_provider='gemini'")

        skills_dir = settings.get_effective_skills_dir()
        if not skills_dir.exists():
            print(f"Skills dir not found: {skills_dir}", file=sys.stderr)
            return

        records: List[SkillRecord] = []
        vectors_present = False

        for skill_path in skills_dir.iterdir():
            if not skill_path.is_dir():
                continue
            skill_md = skill_path / "SKILL.md"
            if not skill_md.exists():
                continue

            meta, body = parse_frontmatter(skill_md)

            name = meta.get("name", skill_path.name)
            description = meta.get("description", "")
            category = meta.get("category", "")
            tags = meta.get("tags", [])
            always_apply = meta.get("alwaysApply", False)
            if not isinstance(always_apply, bool):
                always_apply = False

            # Normalize category/tags for consistent search & filtering
            category_norm = self._norm_token(category) if category else ""
            tags_norm: List[str] = []
            if isinstance(tags, list):
                tags_norm = [self._norm_token(t) for t in tags]
            elif isinstance(tags, str):
                tags_norm = [self._norm_token(tags)]

            text_to_embed = f"{name} {description} {category_norm} {' '.join(tags_norm)}"
            vec = get_embedding(text_to_embed)
            if vec:
                vectors_present = True

            record = SkillRecord(
                name=name,
                description=description,
                category=category_norm,
                tags=tags_norm,
                always_apply=always_apply,
                instructions=body,
                path=str(skill_path.absolute()),
                metadata=json.dumps(meta),
                vector=vec,
            )
            records.append(record)

        if not records:
            return

        # Drop & recreate to keep schema simple in v0.x
        if self.table_name in self.db.table_names():
            self.db.drop_table(self.table_name)

        data: List[Dict[str, Any]] = []
        for r in records:
            d = r.model_dump()
            if isinstance(d.get("tags"), list):
                d["tags_text"] = " ".join(d["tags"])
            else:
                d["tags_text"] = str(d.get("tags", ""))
            if not vectors_present:
                d.pop("vector", None)
            data.append(d)

        if not data:
            return

        self.db.create_table(self.table_name, data=data, mode="overwrite")

        tbl = self.db.open_table(self.table_name)
        try:
            tbl.create_fts_index(
                ["name", "description", "tags_text", "category"],
                replace=True,
                use_tantivy=True,
            )
        except Exception as e:
            print(f"FTS index creation failed (maybe already exists or not supported): {e}", file=sys.stderr)

        try:
            tbl.create_scalar_index("category", index_type="BITMAP", replace=True)
        except Exception as e:
            print(f"Category scalar index creation failed: {e}", file=sys.stderr)
        try:
            tbl.create_scalar_index("tags", index_type="LABEL_LIST", replace=True)
        except Exception as e:
            print(f"Tags scalar index creation failed: {e}", file=sys.stderr)

    # --- Query helpers ---
    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        tbl = self._get_table()
        if not tbl:
            return []

        threshold = settings.search_threshold
        query = self._normalize(query)
        prefilter = self._build_prefilter()
        fetch_limit = limit * 4

        try:
            vec = get_embedding(query)
        except Exception as e:
            print(f"Embedding fetch failed, falling back to FTS: {e}", file=sys.stderr)
            vec = None

        results: List[Dict[str, Any]] = []

        try:
            if vec:
                search_op = tbl.search(vec)
                if prefilter:
                    search_op = search_op.where(prefilter)
                results = search_op.limit(fetch_limit).to_list()
            else:
                try:
                    search_op = tbl.search(query, query_type="fts")
                    if prefilter:
                        search_op = search_op.where(prefilter)
                    results = search_op.limit(fetch_limit).to_list()
                except Exception as e:
                    print(f"FTS search failed, using substring fallback: {e}", file=sys.stderr)
                    search_op = tbl.search()
                    if prefilter:
                        search_op = search_op.where(prefilter)
                    rows = search_op.limit(fetch_limit * 3).to_list()

                    qlow = query.lower()
                    for row in rows:
                        if qlow in str(row.get("name", "")).lower() or qlow in str(row.get("description", "")).lower():
                            row["_score"] = 0.1
                            results.append(row)
                            if len(results) >= fetch_limit:
                                break
        except Exception as e:
            print(f"Search error: {e}", file=sys.stderr)
            return []

        if not results:
            return []

        results.sort(key=lambda x: x.get("_score", 0), reverse=True)

        if len(results) <= 5:
            return results[:limit]

        top_score = results[0].get("_score", 0)
        if top_score <= 0:
            return results[:limit]

        filtered_results = []
        for res in results:
            score = res.get("_score", 0)
            if score / top_score >= threshold:
                filtered_results.append(res)
            else:
                break

        return filtered_results[:limit]

    def get_skill(self, skill_name: str) -> Optional[Dict[str, Any]]:
        tbl = self._get_table()
        if not tbl:
            return None

        safe_name = self._escape_sql_string(skill_name)
        res = tbl.search().where(f"name = '{safe_name}'").limit(1).to_list()
        if res:
            return res[0]
        return None

    def get_core_skills(self) -> List[Dict[str, Any]]:
        tbl = self._get_table()
        if not tbl:
            return []

        base_clause = "always_apply = true"
        prefilter = self._build_prefilter()
        where_clause = base_clause if not prefilter else f"{base_clause} AND ({prefilter})"
        try:
            return tbl.search().where(where_clause).limit(100).to_list()
        except Exception as e:
            print(f"Error fetching core skills: {e}", file=sys.stderr)
            return []


db = SkillDB()

