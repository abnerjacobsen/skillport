from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class SourceType(Enum):
    BUILTIN = "builtin"
    LOCAL = "local"
    GITHUB = "github"


@dataclass
class SkillInfo:
    """Detected skill metadata."""

    name: str
    source_path: Path


@dataclass
class AddResult:
    """Result of add/remove operations."""

    success: bool
    skill_id: str
    message: str
