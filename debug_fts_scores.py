
import lancedb
from lancedb.pydantic import LanceModel, Vector
from typing import List
import shutil
from pathlib import Path

# Clean up previous test db
test_db_path = Path("./test_lancedb_scores")
if test_db_path.exists():
    shutil.rmtree(test_db_path)

db = lancedb.connect(test_db_path)

class Skill(LanceModel):
    name: str
    description: str
    category: str
    tags: List[str]

data = [
    Skill(name="search_web", description="Search the internet for information using Google", category="search", tags=["web", "google"]),
    Skill(name="search_code", description="Search the local codebase for functions and classes", category="search", tags=["code", "grep"]),
    Skill(name="read_file", description="Read the contents of a file from the filesystem", category="fs", tags=["read", "file"]),
    Skill(name="write_file", description="Write content to a file", category="fs", tags=["write", "file"]),
    Skill(name="git_commit", description="Commit changes to git", category="git", tags=["version control"]),
]

table = db.create_table("skills", schema=Skill, mode="overwrite")
table.add(data)

# Create FTS index
table.create_fts_index(["name", "description"], replace=True, use_tantivy=True)

queries = ["search", "file", "web search", "git"]

print("--- FTS Score Analysis ---")
for q in queries:
    print(f"\nQuery: '{q}'")
    # Note: LanceDB FTS search syntax
    results = table.search(q, query_type="fts").limit(10).to_list()
    for r in results:
        # LanceDB usually puts score in _score
        score = r.get("_score", "N/A")
        print(f"  - {r['name']}: {score}")
