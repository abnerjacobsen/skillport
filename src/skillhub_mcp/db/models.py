from typing import List, Literal, Optional

from lancedb.pydantic import LanceModel

# Runtime type: python, node, or none (prompt-only/native)
RuntimeType = Literal["python", "node", "none"]


class SkillRecord(LanceModel):
    name: str
    description: str
    category: str = ""
    tags: List[str] = []
    always_apply: bool = False
    # Execution environment fields (EXECUTION_ENV.md v2.2)
    runtime: str = "none"  # python | node | none
    requires_setup: bool = False  # If true, ready check is performed before execution
    instructions: str
    path: str
    metadata: str  # JSON string
    # Using List[float] allows flexibility for different embedding models (OpenAI: 1536, Gemini: 768, etc.)
    # without strict schema validation failures on dimension mismatch during development/model switching.
    vector: Optional[List[float]] = None

