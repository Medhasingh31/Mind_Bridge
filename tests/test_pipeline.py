import unittest

from modules.pipeline import PipelineError, UserInput, run_pipeline


class PipelineTests(unittest.TestCase):
    def test_composes_foundation_result(self) -> None:
        result = run_pipeline(UserInput("Draft a plan. It should be concise.", context="A software project"))
        self.assertEqual(result.task, "Draft a plan")
        self.assertEqual(result.context, "A software project")
        self.assertEqual(result.constraints, ["It should be concise"])

    def test_rejects_invalid_input(self) -> None:
        with self.assertRaises(PipelineError):
            run_pipeline(" ")


if __name__ == "__main__":
    unittest.main()
