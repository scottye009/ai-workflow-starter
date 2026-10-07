from __future__ import annotations

import json
from typing import Literal

from pydantic import BaseModel, Field, ValidationError


class Classification(BaseModel):
    label: Literal["relevant", "irrelevant", "needs_review"]
    confidence: float = Field(ge=0.0, le=1.0)
    evidence: list[str] = Field(default_factory=list)
    rationale: str


def parse_classification(raw: str) -> Classification:
    try:
        return Classification.model_validate(json.loads(raw))
    except (json.JSONDecodeError, ValidationError) as exc:
        raise ValueError(f"Invalid model output: {exc}") from exc


def output_schema() -> dict:
    return Classification.model_json_schema()


if __name__ == "__main__":
    example = """
    {
      "label": "needs_review",
      "confidence": 0.72,
      "evidence": ["The source contains conflicting dates."],
      "rationale": "The evidence is insufficient for a deterministic decision."
    }
    """
    print(parse_classification(example))
