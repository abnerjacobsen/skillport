"""Domain exceptions for SkillSouko."""


class SkillSoukoError(Exception):
    """Base exception for SkillSouko."""


class SkillNotFoundError(SkillSoukoError):
    def __init__(self, identifier: str):
        self.identifier = identifier
        super().__init__(f"Skill not found: {identifier}")


class AmbiguousSkillError(SkillSoukoError):
    def __init__(self, identifier: str, candidates: list[str]):
        self.identifier = identifier
        self.candidates = candidates
        super().__init__(
            f"Ambiguous skill: {identifier}. Candidates: {', '.join(candidates)}"
        )


class ValidationError(SkillSoukoError):
    """Skill validation failed."""


class IndexingError(SkillSoukoError):
    """Index operation failed."""


class SourceError(SkillSoukoError):
    """Source (GitHub/local) operation failed."""


__all__ = [
    "SkillSoukoError",
    "SkillNotFoundError",
    "AmbiguousSkillError",
    "ValidationError",
    "IndexingError",
    "SourceError",
]
