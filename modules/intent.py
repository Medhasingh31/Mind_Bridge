def detect_intent(text: str) -> str:
    """
    Detect the primary intent of the user's request.
    """

    text_lower = text.lower()

    intent_keywords = {
        "code_generation": [
            "code",
            "program",
            "python",
            "javascript",
            "function",
            "script",
            "website",
            "app",
        ],
        "summarization": [
            "summarize",
            "summary",
            "shorten",
            "brief",
            "संक्षेप",
        ],
        "translation": [
            "translate",
            "translation",
            "convert language",
            "अनुवाद",
        ],
        "explanation": [
            "explain",
            "explanation",
            "meaning",
            "how does",
            "what is",
        ],
        "research": [
            "research",
            "study",
            "paper",
            "analyze",
            "analysis",
        ],
        "writing": [
            "write",
            "essay",
            "article",
            "email",
            "letter",
        ],
    }

    scores = {}

    for intent, keywords in intent_keywords.items():
        score = sum(
            1 for keyword in keywords
            if keyword in text_lower
        )

        if score > 0:
            scores[intent] = score

    if not scores:
        return "general_request"

    return max(scores, key=scores.get)