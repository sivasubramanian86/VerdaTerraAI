import pytest
from verdaterrakai.agents.types import AgentState, PerceivedEnvironmentState
from verdaterrakai.agents.sub_agents import hygiene_hotspot_agent_stub, routing_governance_agent_stub

def test_hygiene_calculation_logic():
    # Setup state with high criticality perception
    perceived = PerceivedEnvironmentState(unified_criticality_score=75)
    state: AgentState = {
        "perceived_state": perceived,
        "messages": [],
        "vision_input": None,
        "gas_input": None,
        "water_input": None,
        "audio_input": None,
        "vibration_input": None,
        "reasoning_trace": [],
        "next_action": "",
        "final_response": ""
    }
    
    # Run hygiene assessment
    result = hygiene_hotspot_agent_stub(state)
    snapshot = result["hygiene_status"]
    
    # Base 100 - min(75, 40) penalty = 60. 
    # If MCP fetch returns open issues, it will be lower. Assume sqlite returns 1 open issue => 60 - 10 = 50.
    assert snapshot["hygiene_score"] <= 60
    assert "High" in snapshot["risk_classification"] or "Medium" in snapshot["risk_classification"]
    assert len(snapshot["remediation_actions"]) > 0

def test_poc_routing_water_issue():
    # Water issue routes to the Bengaluru jurisdiction-specific water board
    perceived = PerceivedEnvironmentState(
        water_quality_issues=["Abnormal pH: 9.0"]
    )
    state: AgentState = {
        "perceived_state": perceived,
        "hygiene_status": {"risk_classification": "High"},
        "messages": [],
        "vision_input": None,
        "gas_input": None,
        "water_input": None,
        "audio_input": None,
        "vibration_input": None,
        "reasoning_trace": [],
        "next_action": "",
        "final_response": ""
    }
    
    result = routing_governance_agent_stub(state)
    routing = result["routing_status"]["routing_decision"]
    
    assert routing["department"] == "BWSSB"
    assert routing["escalation_path"] == "Zonal Commissioner"

