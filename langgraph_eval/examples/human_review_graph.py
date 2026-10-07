from typing import TypedDict
from langgraph.graph import START, END, StateGraph

class State(TypedDict, total=False):
    text: str
    confidence: float
    proposed_label: str
    needs_review: bool

def classify(state: State) -> State:
    # Replace with validated model output.
    return {
        "proposed_label": "example",
        "confidence": 0.65,
    }

def decide_review(state: State) -> State:
    return {"needs_review": state["confidence"] < 0.80}

def route(state: State) -> str:
    return "review" if state["needs_review"] else "complete"

def review(state: State) -> State:
    # In production, pause / hand off to reviewer here.
    return state

def complete(state: State) -> State:
    return state

graph = StateGraph(State)
graph.add_node("classify", classify)
graph.add_node("decide_review", decide_review)
graph.add_node("review", review)
graph.add_node("complete", complete)

graph.add_edge(START, "classify")
graph.add_edge("classify", "decide_review")
graph.add_conditional_edges("decide_review", route, {
    "review": "review",
    "complete": "complete",
})
graph.add_edge("review", END)
graph.add_edge("complete", END)

app = graph.compile()
