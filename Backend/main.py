"""Command-line entry point for the MindBridge foundation."""

from modules import PipelineResult, UserInput, run_pipeline


def process_request(text: str, context: str | None = None) -> PipelineResult:
    """Process one user request through the core pipeline."""
    return run_pipeline(UserInput(text=text, context=context))


if __name__ == "__main__":
    result = process_request("Create a concise project summary. Output it as bullet points.")
    print(result)
