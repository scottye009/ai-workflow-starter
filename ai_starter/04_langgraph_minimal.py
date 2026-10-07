from __future__ import annotations

from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict, total=False):
    input: dict
    validated: bool
    result: dict
    status: Literal["ok", "needs_review", "error"]
    errors: list[str]


def validate(state: State) -> State:
    payload = state.get("input", {})
    if not payload:
        return {"validated": False, "status": "error", "errors": ["empty_input"]}
    return {"validated": True}


def route_after_validate(state: State) -> str:
    return "process" if state.get("validated") else "finish"


def process(state: State) -> State:
    return {
        "result": {"processed": state["input"]},
        "status": "ok",
    }


def finish(state: State) -> State:
    return state


def build_graph():
    graph = StateGraph(State)
    graph.add_node("validate", validate)
    graph.add_node("process", process)
    graph.add_node("finish", finish)

    graph.add_edge(START, "validate")
    graph.add_conditional_edges(
        "validate",
        route_after_validate,
        {"process": "process", "finish": "finish"},
    )
    graph.add_edge("process", "finish")
    graph.add_edge("finish", END)

    return graph.compile()


if __name__ == "__main__":
    app = build_graph()
    print(app.invoke({"input": {"record_id": "123"}, "errors": []}))
