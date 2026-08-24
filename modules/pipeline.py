"""Core foundation pipeline for MindBridge."""

from dataclasses import dataclass, field

from .config import DEFAULT_CONFIG, PipelineConfig
from .intent import Intent, analyze_intent
from .language import DetectedLanguage, detect_language
from .requirements import RequirementSet, extract_requirements


class PipelineError(ValueError):
    """Raised when the core pipeline cannot process a request."""


@dataclass(frozen=True)
class UserInput:
    """Input supplied to the MindBridge pipeline."""

    text: str
    context: str | None = None


@dataclass(frozen=True)
class PipelineResult:
    """Structured representation produced by the foundation pipeline."""

    user_input: UserInput
    detected_language: DetectedLanguage
    intent: Intent
    task: str
    context: str | None
    requirements: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    expected_output: str | None = None


def run_pipeline(user_input: UserInput | str, config: PipelineConfig = DEFAULT_CONFIG) -> PipelineResult:
    """Run language detection, intent analysis, and extraction in sequence."""
    if isinstance(user_input, str):
        user_input = UserInput(user_input)
    if not isinstance(user_input, UserInput):
        raise PipelineError("user_input must be a UserInput instance or string.")
    if not isinstance(user_input.text, str) or len(user_input.text.strip()) < config.minimum_input_length:
        raise PipelineError("User input must contain meaningful text.")

    language = detect_language(user_input.text)
    intent = analyze_intent(user_input.text)
    extracted: RequirementSet = extract_requirements(user_input.text)
    return PipelineResult(
        user_input=user_input,
        detected_language=language,
        intent=intent,
        task=intent.task,
        context=user_input.context,
        requirements=extracted.requirements,
        constraints=extracted.constraints,
        expected_output=extracted.expected_output,
    )
