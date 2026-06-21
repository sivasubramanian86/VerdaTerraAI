from typing import Dict, Any, Literal
from langgraph.graph import StateGraph, END
from .guardrails import check_harmful_content, check_pii_leakage
from verdaterrakai.utils.logger import setup_logger

logger = setup_logger(__name__)
from .types import AgentState
from .perception_agent import perception_node
from .sub_agents import (
    hygiene_hotspot_agent_stub, policy_rag_agent_stub, routing_governance_agent_stub
)
from .tools import PolicyRAGTool, AlloyDBMCPClient
import asyncio

async def planner_node(state: AgentState) -> Dict[str, Any]:
    """
    ReAct/CoT Planner Agent.
    Evaluates the input and the current state to decide the next action.
    """
    messages = state.get("messages", [])
    last_msg = messages[-1]["content"] if messages else ""
    corr_id = state.get("correlation_id", "unknown")
    
    is_harmful, reason = check_harmful_content(last_msg)
    is_pii, pii_reason = check_pii_leakage(last_msg)
    if is_harmful or is_pii:
        full_reason = reason or pii_reason
        logger.warning(f"SECURITY_VIOLATION: {full_reason}", extra={"correlation_id": corr_id})
        return {
            "final_response": f"Escalated to Human Review: Security Violation.",
            "next_action": "END"
        }
    
    
    current_trace = state.get("reasoning_trace", [])
    new_reasoning = []
    
    # If perceived_state is populated, we already ran perception.
    # Route to policy.
    if state.get("perceived_state"):
        new_reasoning.append("Perception state is complete. Routing to Hygiene Assessment.")
        next_action = "hygiene"
        
        loc_id = state.get("location_id", "loc_bengaluru")
        # Parallel Execution: Fetch RAG prep and Metrics simultaneously
        rag_task = asyncio.to_thread(PolicyRAGTool.search_policies, loc_id, last_msg)
        metrics_task = asyncio.to_thread(AlloyDBMCPClient.fetch_aggregated_metrics, loc_id)
        await asyncio.gather(rag_task, metrics_task)
        new_reasoning.append("Parallelized RAG lookups and Metrics pre-fetching completed via asyncio.")
        
        return {
            "reasoning_trace": current_trace + new_reasoning,
            "next_action": next_action
        }
    
    # Mock LLM Routing Decision
    if "image" in last_msg.lower() or state.get("vision_input") or state.get("gas_input"):
        new_reasoning.append("Input contains sensory data or image keywords. Routing to Perception.")
        next_action = "perception"
    else:
        new_reasoning.append("Input is a generic question. Generating final response directly.")
        next_action = "END"
        
    return {
        "reasoning_trace": current_trace + new_reasoning,
        "next_action": next_action,
        "final_response": f"Direct Planner Response to: {last_msg}" if next_action == "END" else ""
    }

def route_next(state: AgentState) -> str:
    """Conditional routing edge."""
    action = state.get("next_action")
    if action == "perception":
        return "perception"
    elif action == "hygiene":
        return "hygiene"
    elif action == "policy":
        return "policy"
    return END

def create_planner_graph():
    builder = StateGraph(AgentState)
    
    builder.add_node("planner", planner_node)
    builder.add_node("perception", perception_node)
    builder.add_node("hygiene", hygiene_hotspot_agent_stub)
    builder.add_node("policy", policy_rag_agent_stub)
    builder.add_node("routing", routing_governance_agent_stub)
    
    builder.set_entry_point("planner")
    
    # Planner -> Conditional
    builder.add_conditional_edges("planner", route_next, {
        "perception": "perception",
        "hygiene": "hygiene",
        "policy": "policy",
        END: END
    })
    
    # Perception -> Planner (Loops back to plan next step)
    builder.add_edge("perception", "planner")
    
    # Hygiene -> Policy -> Routing
    builder.add_edge("hygiene", "policy")
    builder.add_edge("policy", "routing")
    builder.add_edge("routing", END)
    
    return builder.compile()

graph = create_planner_graph()
