from langgraph.graph import StateGraph, END
from .state import IncidentState
from .perception import perception_node
from .smell import smell_node
from .water import water_node
from .hygiene import hygiene_node
from .policy import policy_node
from .routing import routing_node

def build_graph():
    builder = StateGraph(IncidentState)
    
    # Add Nodes
    builder.add_node("perception", perception_node)
    builder.add_node("smell", smell_node)
    builder.add_node("water", water_node)
    builder.add_node("hygiene", hygiene_node)
    builder.add_node("policy", policy_node)
    builder.add_node("routing", routing_node)
    
    # Simple linear progression for POC
    builder.set_entry_point("perception")
    builder.add_edge("perception", "smell")
    builder.add_edge("smell", "water")
    builder.add_edge("water", "hygiene")
    builder.add_edge("hygiene", "policy")
    builder.add_edge("policy", "routing")
    builder.add_edge("routing", END)
    
    return builder.compile()

# Expose compiled graph
graph = build_graph()
