from typing import List, Optional

from lancedb.pydantic import LanceModel


class SkillRecord(LanceModel):
    id: str
    name: str
    description: str
    category: str = ""
    tags: List[str] = []
    always_apply: bool = False
    instructions: str
    path: str
    lines: int = 0
    metadata: str
    vector: Optional[List[float]] = None
