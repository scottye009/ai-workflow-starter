from typing import TypedDict
from langgraph.graph import START, END, StateGraph

class State(TypedDict, total=False):
    input: dict
    result: dict
    status: str

def process(state: State) -> State:
    return {"result": {"processed": state["input"]}, "status": "ok"}

graph = StateGraph(State)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)

app = graph.compile()

if __name__ == "__main__":
    print(app.invoke({"input": {"id": "123"}}))
