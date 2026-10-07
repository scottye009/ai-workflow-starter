from typing import Literal, TypedDict
from langgraph.graph import START, END, StateGraph

class State(TypedDict, total=False):
    input: dict
    valid: bool
    status: Literal["ok", "needs_review", "error"]

def validate(state: State) -> State:
    return {"valid": bool(state.get("input"))}

def route(state: State) -> str:
    return "process" if state.get("valid") else "review"

def process(state: State) -> State:
    return {"status": "ok"}

def review(state: State) -> State:
    return {"status": "needs_review"}

graph = StateGraph(State)
graph.add_node("validate", validate)
graph.add_node("process", process)
graph.add_node("review", review)

graph.add_edge(START, "validate")
graph.add_conditional_edges("validate", route, {
    "process": "process",
    "review": "review",
})
graph.add_edge("process", END)
graph.add_edge("review", END)

app = graph.compile()
