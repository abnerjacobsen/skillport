import os
import json
from pathlib import Path
from typing import List, Optional, Any, Dict
import lancedb
from lancedb.pydantic import LanceModel, Vector
from lancedb.embeddings import EmbeddingFunctionRegistry
from .config import settings
from .utils import parse_frontmatter
import openai
from google import genai

import sys

# --- Embedding Handling ---

def get_embedding(text: str) -> Optional[List[float]]:
    """
    Provider-agnostic embedding fetcher.
    """
    if settings.embedding_provider == "none":
        return None

    provider = settings.embedding_provider
    text = text.replace("\n", " ")

    try:
        if provider == "openai":
            if not settings.openai_api_key:
                raise ValueError("OPENAI_API_KEY is required when embedding_provider='openai'")
            client = openai.Client(api_key=settings.openai_api_key)
            response = client.embeddings.create(input=[text], model=settings.embedding_model)
            return response.data[0].embedding

        if provider == "gemini":
            if not settings.gemini_api_key:
                raise ValueError("GEMINI_API_KEY is required when embedding_provider='gemini'")
            client = genai.Client(api_key=settings.gemini_api_key)
            result = client.models.embed_content(
                model=settings.gemini_embedding_model,
                contents=text,
            )
            # google-genai returns embeddings list with .values
            if result.embeddings:
                return list(result.embeddings[0].values)
            raise ValueError("Gemini embedding response missing embeddings")

        raise ValueError(f"Unsupported embedding_provider: {provider}")

    except Exception as e:
        print(f"Embedding error ({provider}): {e}", file=sys.stderr)
        raise

# --- Schema ---

# We define schema dynamically or allow nullable vector? 
# LanceDB pydantic integration usually wants fixed size.
# But if we use custom embedding function we might not need to specify size here if we handle it?
# Let's try to define a generic size or use the fact that we store it as list?
# LanceDB requires dimension for Vector type usually.
# OpenAI text-embedding-3-small is 1536.
# Ollama depends on model.
# If we want to support multiple, we might need to handle schema evolution or just list[float].
# But for vector index, we need fixed dims.
# For v0.0.0 let's assume 1536 if openai.
# If we don't know dimension, we might struggle with strictly typed Vector(dim).
# Let's use a plain list for now in Pydantic and let LanceDB infer or handle it, 
# OR just define it as 1536 and warn if different?
# PRD says "Vector" column.
# Let's check if we can infer it.
# To keep it simple and robust for v0.0.0:
# We will try to fetch one embedding to determine size, or default to 1536.

class SkillRecord(LanceModel):
    name: str
    description: str
    category: str = "" # Optional but LanceModel fields are required unless Optional type?
    tags: List[str] = []
    always_apply: bool = False # New field
    instructions: str
    path: str
    metadata: str # JSON string
    vector: Optional[List[float]] = None # We use List[float] to be flexible with dimensions? 
                                         # Or use Vector(1536) if we want index?
                                         # To use vector search we need Vector type.
                                         
    # For FTS we need to specify which fields. LanceDB 0.1+ supports FTS.
    
# --- DB Manager ---

class SkillDB:
    def __init__(self):
        self.db_path = settings.get_effective_db_path()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.db = lancedb.connect(self.db_path)
        self.table_name = "skills"
        # lightweight query normalization
        self._normalize = lambda q: " ".join(q.strip().split())

    def _get_table(self):
        if self.table_name in self.db.table_names():
            return self.db.open_table(self.table_name)
        return None

    def initialize_index(self):
        """
        Scans SKILLS_DIR and re-creates the index.
        """
        # Fail fast if embeddings are requested but credentials are missing to avoid
        # creating a broken table schema.
        if settings.embedding_provider == "openai" and not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when embedding_provider='openai'")
        if settings.embedding_provider == "gemini" and not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY or GOOGLE_API_KEY is required when embedding_provider='gemini'")

        skills_dir = settings.get_effective_skills_dir()
        if not skills_dir.exists():
            print(f"Skills dir not found: {skills_dir}", file=sys.stderr)
            return

        records = []
        vectors_present = False
        
        # Walk through subdirectories
        for skill_path in skills_dir.iterdir():
            if skill_path.is_dir():
                skill_md = skill_path / "SKILL.md"
                if skill_md.exists():
                    meta, body = parse_frontmatter(skill_md)
                    
                    name = meta.get("name", skill_path.name)
                    description = meta.get("description", "")
                    category = meta.get("category", "")
                    tags = meta.get("tags", [])
                    always_apply = meta.get("alwaysApply", False)
                    if not isinstance(always_apply, bool):
                        always_apply = False
                    
                    # Combine for embedding
                    text_to_embed = f"{name} {description} {category} {' '.join(tags)}"
                    
                    vec = get_embedding(text_to_embed)
                    if vec:
                        vectors_present = True
                    
                    record = SkillRecord(
                        name=name,
                        description=description,
                        category=category or "",
                        tags=tags or [],
                        always_apply=always_apply,
                        instructions=body,
                        path=str(skill_path.absolute()),
                        metadata=json.dumps(meta),
                        vector=vec
                    )
                    records.append(record)

        if not records:
            return

        # Create or Overwrite table
        # We drop and recreate to handle schema changes or clean state easily for v0
        if self.table_name in self.db.table_names():
            self.db.drop_table(self.table_name)
            
        # Convert records to list of dicts to allow flexible schema inference
        # If provider is none, we want to ensure vector column is handled correctly (or omitted)
        data = []
        for r in records:
            d = r.model_dump()
            # If we have no vectors at all, drop the column to avoid schema inference issues.
            if not vectors_present:
                d.pop("vector", None)
            data.append(d)

        if not data:
            return

        self.db.create_table(self.table_name, data=data, mode="overwrite")
        
        # Create FTS index
        tbl = self.db.open_table(self.table_name)
        try:
            # Light, multilingual-friendly index: name (high), description (medium). Instructions omitted for size.
            tbl.create_fts_index(["name", "description"], replace=True, use_tantivy=True)
        except Exception as e:
            print(f"FTS index creation failed (maybe already exists or not supported): {e}", file=sys.stderr)

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        tbl = self._get_table()
        if not tbl:
            return []

        query = self._normalize(query)

        # Hybrid Search logic
        # If embedding enabled, use vector search.
        # Also use FTS? LanceDB python client hybrid search API is experimental or specific.
        # PRD says: "Vector search + FTS... Combined score"
        
        # Simple implementation:
        # If embedding provider != none, get query vector -> search
        # Else -> FTS search
        
        # Note: Pure LanceDB search().limit() usually does vector search if vector provided.
        # To do FTS, we use .search(query, query_type="fts").
        
        # For "Hybrid", we might need to manual merge or use advanced features.
        # Let's try to stick to standard lancedb "search()" which often handles vector if vector is passed.
        
        vec = get_embedding(query)
        
        if vec:
            # Vector Search
            # We can also add a prefilter if we supported it, but filtering happens later in app logic per PRD?
            # PRD: "Server settings filter... but Index keeps all"
            # So we search all, then filter in Python?
            # Wait, if we limit to 5 in DB, and all 5 are disabled, we return 0?
            # Ideally we fetch more then filter.
            # But PRD says "search_skills is filtered by server settings".
            # Let's fetch limit * 3 candidates then filter.
            
            results = tbl.search(vec).limit(limit * 4).to_list()
            # LanceDB returns dicts
        else:
            # FTS Search
            try:
                results = tbl.search(query, query_type="fts").limit(limit * 4).to_list()
            except Exception as e:
                # Fallback: simple substring match on name/description with fixed low score
                print(f"FTS search failed, using substring fallback: {e}", file=sys.stderr)
                try:
                    rows = tbl.search().limit(limit * 10).to_list()
                except Exception:
                    return []
                qlow = query.lower()
                results = []
                for row in rows:
                    if qlow in str(row.get("name", "")).lower() or qlow in str(row.get("description", "")).lower():
                        row["_score"] = 0.1
                        results.append(row)
                        if len(results) >= limit:
                            break

        return results

    def get_skill(self, skill_name: str) -> Optional[Dict[str, Any]]:
        tbl = self._get_table()
        if not tbl:
            return None
        
        # Simple equality check with sanitized value to avoid breaking the filter expression
        safe_name = skill_name.replace("'", "''")
        res = tbl.search().where(f"name = '{safe_name}'").limit(1).to_list()
        if res:
            return res[0]
        return None

    def get_core_skills(self) -> List[Dict[str, Any]]:
        tbl = self._get_table()
        if not tbl:
            return []
        # LanceDB doesn't support boolean literals easily in SQL sometimes, but True/False usually works.
        # Or we can use where string "always_apply = true"
        try:
            return tbl.search().where("always_apply = true").limit(100).to_list()
        except Exception as e:
            print(f"Error fetching core skills: {e}", file=sys.stderr)
            return []

db = SkillDB()
