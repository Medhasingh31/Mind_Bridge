import unittest

from modules.requirements import extract_requirements


class RequirementExtractionTests(unittest.TestCase):
    def test_separates_constraints_and_expected_output(self) -> None:
        result = extract_requirements("Write a report. It must be concise. Output it as JSON.")
        self.assertEqual(result.requirements, ["Write a report", "Output it as JSON"])
        self.assertEqual(result.constraints, ["It must be concise"])
        self.assertEqual(result.expected_output, "Output it as JSON")


if __name__ == "__main__":
    unittest.main()
