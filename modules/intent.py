"""Intent analysis interfaces for MindBridge."""

from dataclasses import dataclass
import re


class IntentAnalysisError(ValueError):
    """Raised when intent analysis receives invalid input."""


@dataclass(frozen=True)
class Intent:
    """The initial semantic intent of a user request."""

    name: str
    task: str
    confidence: float


def analyze_intent(text: str) -> Intent:
    """Create a deterministic baseline intent from a user request."""
    if not isinstance(text, str) or not text.strip():
        raise IntentAnalysisError("User input must be a non-empty string.")

    task = re.split(r"[.!?\n]+", text.strip(), maxsplit=1)[0].strip()
    return Intent(name="general_request", task=task, confidence=0.50)
