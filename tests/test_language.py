import unittest

from modules.language import LanguageDetectionError, detect_language


class LanguageDetectionTests(unittest.TestCase):
    def test_detects_english(self) -> None:
        self.assertEqual(detect_language("Build a summary").code, "en")

    def test_rejects_empty_input(self) -> None:
        with self.assertRaises(LanguageDetectionError):
            detect_language(" ")


if __name__ == "__main__":
    unittest.main()
