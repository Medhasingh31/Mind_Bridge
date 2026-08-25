from typing import List

from .schema import StructuredRequirement


def extract_requirements(
    user_input: str,
    language: str,
    intent: str
) -> StructuredRequirement:

    text = user_input.strip()

    task = _extract_task(text)

    requirements = _extract_requirements(text)

    constraints = _extract_constraints(text)

    expected_output = _extract_expected_output(text)

    entities = _extract_entities(text)

    return StructuredRequirement(
        user_input=text,
        language=language,
        intent=intent,
        task=task,
        requirements=requirements,
        constraints=constraints,
        expected_output=expected_output,
        entities=entities,
    )


def _extract_task(text: str) -> str:
    """
    Basic task extraction.
    """

    sentences = _split_sentences(text)

    if not sentences:
        return text

    return sentences[0]


def _extract_requirements(text: str) -> List[str]:
    """
    Extract basic requirement statements.
    """

    requirements = []

    keywords = [
        "need",
        "want",
        "should",
        "must",
        "create",
        "build",
        "generate",
        "read",
        "handle",
        "analyze",
        "make",
        "chahiye",
        "banana",
        "karna",
        "kare",
        "karo",
    ]

    sentences = _split_sentences(text)

    for sentence in sentences:

        sentence_lower = sentence.lower()

        if any(keyword in sentence_lower for keyword in keywords):
            requirements.append(sentence.strip())

    return _unique(requirements)


def _extract_constraints(text: str) -> List[str]:
    """
    Extract constraint-like statements.
    """

    constraints = []

    constraint_keywords = [
        "must",
        "should",
        "only",
        "without",
        "avoid",
        "beginner",
        "simple",
        "efficient",
        "exactly",
        "maximum",
        "minimum",
        "sirf",
        "bina",
        "simple",
        "easy",
    ]

    sentences = _split_sentences(text)

    for sentence in sentences:

        sentence_lower = sentence.lower()

        if any(
            keyword in sentence_lower
            for keyword in constraint_keywords
        ):
            constraints.append(sentence.strip())

    return _unique(constraints)


def _extract_expected_output(text: str) -> str | None:
    """
    Basic expected-output detection.
    """

    output_keywords = [
        "output",
        "result",
        "code",
        "program",
        "report",
        "answer",
        "response",
    ]

    text_lower = text.lower()

    for keyword in output_keywords:
        if keyword in text_lower:
            return keyword

    return None


def _extract_entities(text: str) -> List[str]:
    """
    Basic entity extraction.

    This will be replaced/improved with NLP/LLM-based
    extraction in later phases.
    """

    entities = []

    known_entities = [
        "python",
        "javascript",
        "java",
        "c++",
        "csv",
        "json",
        "sql",
        "react",
        "html",
        "css",
        "pandas",
        "numpy",
    ]

    text_lower = text.lower()

    for entity in known_entities:
        if entity in text_lower:
            entities.append(entity)

    return entities


def _split_sentences(text: str) -> List[str]:
    """
    Simple sentence splitting.
    """

    separators = [".", "?", "!", "\n"]

    sentences = [text]

    for separator in separators:
        new_sentences = []

        for sentence in sentences:
            new_sentences.extend(sentence.split(separator))

        sentences = new_sentences

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def _unique(items: List[str]) -> List[str]:
    """
    Remove duplicate items while preserving order.
    """

    seen = set()
    result = []

    for item in items:

        normalized = item.lower()

        if normalized not in seen:
            seen.add(normalized)
            result.append(item)

    return result