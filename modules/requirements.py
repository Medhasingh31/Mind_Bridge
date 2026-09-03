import re
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

    missing_information = _detect_missing_information(
        text,
        intent,
        entities
    )

    confidence = _calculate_confidence(
        task,
        requirements,
        constraints,
        entities,
        missing_information
    )

    return StructuredRequirement(
        user_input=text,
        language=language,
        intent=intent,
        task=task,
        requirements=requirements,
        constraints=constraints,
        expected_output=expected_output,
        entities=entities,
        missing_information=missing_information,
        confidence=confidence,
    )


# --------------------------------------------------
# TASK
# --------------------------------------------------

def _extract_task(text: str) -> str:
    """
    Extract the main task from the user's request.
    """

    sentences = _split_sentences(text)

    if not sentences:
        return text

    first_sentence = sentences[0]

    task_patterns = [
        r"(?:i want|i need|i would like)\s+(?:to\s+)?(.+)",
        r"(?:mujhe)\s+(.+?)(?:\s+chahiye|\s+hai|$)",
        r"(?:create|build|make|develop|generate)\s+(.+)",
    ]

    for pattern in task_patterns:

        match = re.search(
            pattern,
            first_sentence,
            re.IGNORECASE
        )

        if match:
            task = match.group(1).strip()

            return _clean_task(task)

    return first_sentence.strip()


def _clean_task(task: str) -> str:

    task = re.sub(
        r"\b(please|pls|kindly)\b",
        "",
        task,
        flags=re.IGNORECASE
    )

    task = re.sub(r"\s+", " ", task)

    return task.strip()


# --------------------------------------------------
# REQUIREMENTS
# --------------------------------------------------

def _extract_requirements(text: str) -> List[str]:
    """
    Extract individual actionable requirements
    instead of storing entire sentences.
    """

    requirements = []

    clauses = _split_clauses(text)

    action_patterns = [
        r"\bread\b.+",
        r"\bhandle\b.+",
        r"\bprocess\b.+",
        r"\banaly[sz]e\b.+",
        r"\bgenerate\b.+",
        r"\bcreate\b.+",
        r"\bbuild\b.+",
        r"\bcalculate\b.+",
        r"\bdetect\b.+",
        r"\bextract\b.+",
        r"\bconvert\b.+",
        r"\bstore\b.+",
        r"\bdisplay\b.+",
        r"\buse\b.+",

        # Hinglish
        r"\bpadhe\b.+",
        r"\bpadna\b.+",
        r"\bhandle\b.+",
        r"\bbanao\b.+",
        r"\bbanaye\b.+",
        r"\bkaro\b.+",
        r"\bkarna\b.+",
    ]

    for clause in clauses:

        clause = clause.strip()

        if not clause:
            continue

        clause_lower = clause.lower()

        # Skip obvious task statements
        if _looks_like_task(clause_lower):
            continue

        for pattern in action_patterns:

            if re.search(
                pattern,
                clause_lower,
                re.IGNORECASE
            ):
                normalized = _normalize_requirement(clause)

                if normalized:
                    requirements.append(normalized)

                break

    return _unique(requirements)


def _split_clauses(text: str) -> List[str]:
    """
    Split sentences into smaller actionable clauses.
    """

    sentences = _split_sentences(text)

    clauses = []

    for sentence in sentences:

        parts = re.split(
            r"\b(?:and|also|then|aur|phir)\b|,",
            sentence,
            flags=re.IGNORECASE
        )

        for part in parts:

            part = part.strip()

            if part:
                clauses.append(part)

    return clauses


def _looks_like_task(text: str) -> bool:

    task_patterns = [
        "i want",
        "i need",
        "i would like",
        "mujhe",
        "create a",
        "build a",
        "make a",
        "develop a",
        "generate a",
    ]

    return any(
        pattern in text
        for pattern in task_patterns
    )


def _normalize_requirement(requirement: str) -> str:
    """
    Normalize requirement wording while preserving meaning.
    """

    requirement = requirement.strip()

    requirement = re.sub(
        r"^(that|which|and|also)\s+",
        "",
        requirement,
        flags=re.IGNORECASE
    )

    requirement = re.sub(
        r"\s+",
        " ",
        requirement
    )

    return requirement.strip()


# --------------------------------------------------
# CONSTRAINTS
# --------------------------------------------------

def _extract_constraints(text: str) -> List[str]:

    constraints = []

    sentences = _split_sentences(text)

    constraint_patterns = [
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
        "easy",
        "sirf",
        "bina",
        "simple",
    ]

    for sentence in sentences:

        sentence_lower = sentence.lower()

        if any(
            keyword in sentence_lower
            for keyword in constraint_patterns
        ):
            constraints.append(
                sentence.strip()
            )

    return _unique(constraints)


# --------------------------------------------------
# EXPECTED OUTPUT
# --------------------------------------------------

def _extract_expected_output(text: str) -> str | None:

    text_lower = text.lower()

    output_mapping = {
        "code": "code",
        "program": "code",
        "script": "code",
        "report": "report",
        "summary": "summary",
        "answer": "answer",
        "explanation": "explanation",
        "response": "response",
    }

    for keyword, output_type in output_mapping.items():

        if keyword in text_lower:
            return output_type

    return None


# --------------------------------------------------
# ENTITIES
# --------------------------------------------------

def _extract_entities(text: str) -> List[str]:

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
        "tensorflow",
        "pytorch",
        "excel",
        "mongodb",
        "mysql",
        "postgresql",
    ]

    text_lower = text.lower()

    for entity in known_entities:

        if re.search(
            r"\b" + re.escape(entity) + r"\b",
            text_lower
        ):
            entities.append(entity)

    return entities


# --------------------------------------------------
# MISSING INFORMATION
# --------------------------------------------------

def _detect_missing_information(
    text: str,
    intent: str,
    entities: List[str]
) -> List[str]:

    missing = []

    text_lower = text.lower()

    if intent == "code_generation":

        if not entities:
            missing.append("technology or programming language")

        if not any(
            word in text_lower
            for word in [
                "create",
                "build",
                "make",
                "program",
                "code",
                "develop",
                "script",
                "banana",
            ]
        ):
            missing.append("specific coding task")

    elif intent == "writing":

        if len(text.split()) < 5:
            missing.append("writing purpose or topic")

    elif intent == "translation":

        if len(text.split()) < 3:
            missing.append("text to translate")

    elif intent == "explanation":

        if len(text.split()) < 3:
            missing.append("topic to explain")

    return missing


# --------------------------------------------------
# CONFIDENCE
# --------------------------------------------------

def _calculate_confidence(
    task: str,
    requirements: List[str],
    constraints: List[str],
    entities: List[str],
    missing_information: List[str]
) -> float:

    score = 0.0

    if task:
        score += 0.30

    if requirements:
        score += 0.30

    if constraints:
        score += 0.10

    if entities:
        score += 0.15

    if not missing_information:
        score += 0.15

    else:
        score -= min(
            0.20,
            len(missing_information) * 0.05
        )

    return round(
        max(0.0, min(1.0, score)),
        2
    )


# --------------------------------------------------
# SENTENCE SPLITTER
# --------------------------------------------------

def _split_sentences(text: str) -> List[str]:

    sentences = re.split(
        r"[.!?\n]+",
        text
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


# --------------------------------------------------
# DUPLICATE REMOVAL
# --------------------------------------------------

def _unique(items: List[str]) -> List[str]:

    seen = set()

    result = []

    for item in items:

        normalized = item.lower().strip()

        if normalized not in seen:

            seen.add(normalized)

            result.append(item)

    return result