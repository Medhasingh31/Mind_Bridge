import unittest

from modules.intent import analyze_intent


class IntentAnalysisTests(unittest.TestCase):
    def test_uses_first_sentence_as_task(self) -> None:
        intent = analyze_intent("Summarize this text. Use bullet points.")
        self.assertEqual(intent.name, "general_request")
        self.assertEqual(intent.task, "Summarize this text")


if __name__ == "__main__":
    unittest.main()
