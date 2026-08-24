"""Configuration values for the MindBridge foundation."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PipelineConfig:
    """Settings used by the foundation pipeline."""

    default_language: str = "en"
    minimum_input_length: int = 1


DEFAULT_CONFIG = PipelineConfig()
