from langgraph.graph import StateGraph, START, END
from .state import State
from .nodes import baNode, architectNode, developerNode

builder = StateGraph(State)
builder.add_node("BA", baNode)
builder.add_node("Architect", architectNode)
builder.add_node("Developer", developerNode)
builder.add_edge(START, "BA")
builder.add_edge("BA","Architect")
builder.add_edge("Architect","Developer")
builder.add_edge("Developer", END)

graph = builder.compile()