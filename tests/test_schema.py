from mindbridge.schema import StructuredRequirement


def test_structured_requirement():
    result = StructuredRequirement(
        user_input="Create a Python program",
        language="English",
        intent="code_generation",
        task="Create a Python program",
    )

    assert result.language == "English"
    assert result.intent == "code_generation"
    assert result.task == "Create a Python program"