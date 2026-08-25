from langdetect import detect, LangDetectException


def detect_language(text: str) -> str:
    """
    Detect the language of the user input.

    Returns:
        English, Hindi, or Hinglish
    """

    if not text or not text.strip():
        return "unknown"

    try:
        detected = detect(text)

        if detected == "en":
            return "English"

        if detected == "hi":
            return "Hindi"

        return detected

    except LangDetectException:
        return "unknown"


def detect_hinglish(text: str) -> bool:
    """
    Basic Hinglish detection.

    This is an initial heuristic and will be improved
    in later phases.
    """

    hinglish_words = {
        "mujhe",
        "hai",
        "chahiye",
        "karo",
        "karna",
        "kaise",
        "mera",
        "meri",
        "ye",
        "woh",
        "aur",
        "mein",
        "ke",
        "ko",
        "se",
        "bana",
        "banana",
    }

    words = set(text.lower().split())

    return len(words.intersection(hinglish_words)) >= 2


def get_language(text: str) -> str:
    """
    Detect English, Hindi, or basic Hinglish.
    """

    if detect_hinglish(text):
        return "Hinglish"

    return detect_language(text)