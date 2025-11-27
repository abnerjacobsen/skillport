"""Domain exceptions for SkillPod."""


class SkillPodError(Exception):
    """Base exception for SkillPod."""


class SkillNotFoundError(SkillPodError):
    def __init__(self, identifier: str):
        self.identifier = identifier
        super().__init__(f"Skill not found: {identifier}")


class AmbiguousSkillError(SkillPodError):
    def __init__(self, identifier: str, candidates: list[str]):
        self.identifier = identifier
        self.candidates = candidates
        super().__init__(
            f"Ambiguous skill: {identifier}. Candidates: {', '.join(candidates)}"
        )


class ValidationError(SkillPodError):
    """Skill validation failed."""


class IndexingError(SkillPodError):
    """Index operation failed."""


class SourceError(SkillPodError):
    """Source (GitHub/local) operation failed."""


__all__ = [
    "SkillPodError",
    "SkillNotFoundError",
    "AmbiguousSkillError",
    "ValidationError",
    "IndexingError",
    "SourceError",
]
