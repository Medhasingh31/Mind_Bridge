"""Requirement and constraint extraction interfaces."""

from dataclasses import dataclass, field
import re


class RequirementExtractionError(ValueError):
    """Raised when requirement extraction receives invalid input."""


@dataclass(frozen=True)
class RequirementSet:
    """Structured requirements extracted from user input."""

    requirements: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    expected_output: str | None = None


def extract_requirements(text: str) -> RequirementSet:
    """Extract simple sentence-level requirements for later refinement."""
    if not isinstance(text, str) or not text.strip():
        raise RequirementExtractionError("User input must be a non-empty string.")

    statements = [part.strip() for part in re.split(r"[.!?\n]+", text) if part.strip()]
    constraints: list[str] = []
    requirements: list[str] = []
    for statement in statements:
        lowered = statement.lower()
        if any(marker in lowered for marker in ("must", "should", "only", "without", "不要")):
            constraints.append(statement)
        else:
            requirements.append(statement)

    expected_output = None
    for statement in statements:
        if any(marker in statement.lower() for marker in ("output", "return", "provide", "generate")):
            expected_output = statement
            break

    return RequirementSet(requirements, constraints, expected_output)
