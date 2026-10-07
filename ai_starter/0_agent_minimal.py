from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

from model_adapter import call_model


ToolFn = Callable[..., Any]


@dataclass
class AgentState:
    goal: str
    messages: list[dict[str, Any]] = field(default_factory=list)
    steps: int = 0
    errors: list[str] = field(default_factory=list)


class Agent:
    def __init__(
        self,
        tools: dict[str, ToolFn],
        tool_schemas: list[dict[str, Any]],
        *,
        max_steps: int = 8,
    ) -> None:
        self.tools = tools
        self.tool_schemas = tool_schemas
        self.max_steps = max_steps

    def run(self, goal: str) -> AgentState:
        state = AgentState(
            goal=goal,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Complete the user's goal using only the available tools. "
                        "Do not invent tool results. Ask for clarification when required. "
                        "Prefer the smallest safe action. Stop when the goal is satisfied."
                    ),
                },
                {"role": "user", "content": goal},
            ],
        )

        while state.steps < self.max_steps:
            state.steps += 1
            decision = call_model(state.messages, tools=self.tool_schemas)

            if decision["type"] == "final":
                state.messages.append(
                    {"role": "assistant", "content": decision["content"]}
                )
                return state

            if decision["type"] != "tool_call":
                raise ValueError(f"Unknown model decision: {decision}")

            name = decision["name"]
            args = decision.get("arguments", {})

            if name not in self.tools:
                result = {"ok": False, "error": f"Unknown tool: {name}"}
            else:
                try:
                    result = {"ok": True, "data": self.tools[name](**args)}
                except Exception as exc:
                    result = {"ok": False, "error": str(exc)}
                    state.errors.append(f"{name}: {exc}")

            state.messages.append(
                {
                    "role": "assistant",
                    "content": "",
                    "tool_call": {"name": name, "arguments": args},
                }
            )
            state.messages.append(
                {
                    "role": "tool",
                    "name": name,
                    "content": str(result),
                }
            )

        state.errors.append("max_steps_reached")
        state.messages.append(
            {
                "role": "assistant",
                "content": "Stopped because the maximum number of steps was reached.",
            }
        )
        return state


# Example
def get_record(record_id: str) -> dict[str, Any]:
    return {"record_id": record_id, "status": "example"}


TOOLS = {"get_record": get_record}

TOOL_SCHEMAS = [
    {
        "name": "get_record",
        "description": "Read one record by ID.",
        "input_schema": {
            "type": "object",
            "properties": {"record_id": {"type": "string"}},
            "required": ["record_id"],
            "additionalProperties": False,
        },
    }
]


if __name__ == "__main__":
    agent = Agent(TOOLS, TOOL_SCHEMAS)
    result = agent.run("Inspect record 123 and report its current status.")
    print(result.messages[-1]["content"])
