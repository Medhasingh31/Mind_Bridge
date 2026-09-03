from pydantic import BaseModel, Field
from typing import List, Optional


class StructuredRequirement(BaseModel):
    user_input: str
    language: str
    intent: str

    task: str = ""

    context: Optional[str] = None

    requirements: List[str] = Field(default_factory=list)

    constraints: List[str] = Field(default_factory=list)

    expected_output: Optional[str] = None

    entities: List[str] = Field(default_factory=list)

    missing_information: List[str] = Field(default_factory=list)

    confidence: Optional[float] = None