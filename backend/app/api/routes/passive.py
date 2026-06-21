from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
from backend.agents.orchestrator import graph
from backend.agents.state import IncidentState

router = APIRouter()

class SensorPayload(BaseModel):
    facility_id: str
    facility_type: str
    location: str
    telemetry: Dict[str, Any]

@router.post("/webhook")
async def passive_webhook(payload: SensorPayload):
    """
    Passive ingestion of sensor events.
    """
    initial_state: IncidentState = {
        "facility_id": payload.facility_id,
        "facility_type": payload.facility_type,
        "location": payload.location,
        "image_url": None,
        "sensor_payload": payload.telemetry,
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
    
    # Run the ADK graph
    result = graph.invoke(initial_state)
    
    return {
        "incident_id": result.get("incident_id"),
        "criticality": result.get("criticality_level")
    }
