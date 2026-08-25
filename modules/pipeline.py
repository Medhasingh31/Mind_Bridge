from .language import get_language
from .intent import detect_intent
from .requirements import extract_requirements
from .schema import StructuredRequirement


def process_requirement(user_input: str) -> StructuredRequirement:
    """
    Process raw user input and convert it into
    a structured requirement.
    """

    if not user_input or not user_input.strip():
        raise ValueError("User input cannot be empty.")

    language = get_language(user_input)

    intent = detect_intent(user_input)

    structured_requirement = extract_requirements(
        user_input=user_input,
        language=language,
        intent=intent,
    )

    return structured_requirement