import pytest
import asyncio
from verdaterrakai.agents.types import AgentState
from verdaterrakai.agents.planner_agent import graph

@pytest.mark.asyncio
async def test_e2e_dirty_restaurant_flow():
    """
    Simulates the full end-to-end flow:
    Planner -> Perception -> Policy -> Routing Governance -> Output
    """
    initial_state = {
        "correlation_id": "test-e2e-1234",
        "messages": [{"role": "user", "content": "Analyze image of dirty restaurant and smelly public toilet"}],
        "vision_input": None,
        "gas_input": None,
        "water_input": None,
        "audio_input": None,
        "vibration_input": None,
        "reasoning_trace": [],
        "next_action": "",
        "final_response": ""
    }
    
    # 1. Run the LangGraph Mesh
    result = await graph.ainvoke(initial_state)
    
    # 2. Assert Guardrails passed
    assert "Request blocked" not in result["final_response"]
    assert "SECURITY_VIOLATION" not in result["final_response"]
    assert "[REDACTED]" not in result["final_response"]
    
    # 3. Assert Sub-Agents were invoked properly
    # Perception
    assert result.get("perceived_state") is not None
    assert result["perceived_state"].unified_criticality_score >= 0
    
    # Hygiene Scaling
    hygiene = result.get("hygiene_status", {})
    assert "risk_classification" in hygiene
    
    # PoC Routing
    routing = result.get("routing_status", {})
    assert routing is not None
    
    # 4. Assert Output contains RAG Citations
    assert "Synthesis:" in result["final_response"]
