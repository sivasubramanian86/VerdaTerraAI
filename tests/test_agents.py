import pytest
from backend.agents.orchestrator import graph
from backend.agents.state import IncidentState

def test_graph_compiles():
    # Just checking if the graph builds without error
    assert graph is not None

def test_full_graph_invocation():
    initial_state: IncidentState = {
        "facility_id": "fac_001",
        "facility_type": "hotel_kitchen",
        "location": "Bengaluru",
        "image_url": "mock_url",
        "sensor_payload": {"ammonia_ppm": 60},
        "visual_score": None,
        "visual_anomalies": None,
        "olfactory_score": None,
        "olfactory_flags": None,
        "water_score": None,
        "criticality_level": None,
        "compliance_report": None,
        "incident_id": None,
        "draft_notification": None,
        "dispatch_status": None
    }
    
    result = graph.invoke(initial_state)
    
    assert "visual_score" in result
    assert "olfactory_score" in result
    assert result["criticality_level"] == "Critical"
    assert "incident_id" in result
