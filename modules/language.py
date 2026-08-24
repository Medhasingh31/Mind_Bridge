"""Language detection interfaces for MindBridge."""

from dataclasses import dataclass


class LanguageDetectionError(ValueError):
    """Raised when language detection receives invalid input."""


@dataclass(frozen=True)
class DetectedLanguage:
    """Language information produced from user input."""

    code: str
    name: str
    confidence: float
    is_mixed: bool = False


def detect_language(text: str) -> DetectedLanguage:
    """Return a lightweight language estimate without external services."""
    if not isinstance(text, str) or not text.strip():
        raise LanguageDetectionError("User input must be a non-empty string.")

    devanagari = sum("\u0900" <= character <= "\u097f" for character in text)
    latin = sum(character.isascii() and character.isalpha() for character in text)

    if devanagari and latin:
        return DetectedLanguage("hi-en", "Hindi-English", 0.70, is_mixed=True)
    if devanagari:
        return DetectedLanguage("hi", "Hindi", 0.90)
    return DetectedLanguage("en", "English", 0.75)
