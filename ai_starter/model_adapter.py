from __future__ import annotations

from typing import Any


def call_model(
    messages: list[dict[str, Any]],
    *,
    tools: list[dict[str, Any]] | None = None,
    response_schema: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Connect this function to the model SDK available in the project.

    Return a normalized dictionary with either:
      {"type": "final", "content": "..."}
    or
      {
        "type": "tool_call",
        "name": "tool_name",
        "arguments": {...}
      }

    If using structured output, validate it outside this adapter.
    """
    raise NotImplementedError("Connect call_model() to the project's model SDK.")
