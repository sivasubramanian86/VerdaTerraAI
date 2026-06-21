from fastapi import APIRouter, UploadFile, File, Form
from typing import Optional
from pydantic import BaseModel
from backend.agents.orchestrator import graph
from backend.agents.state import IncidentState

router = APIRouter()

class ActiveTriggerResponse(BaseModel):
    incident_id: str
    status: str

@router.post("/report", response_model=ActiveTriggerResponse)
async def report_incident(
    facility_id: str = Form(...),
    facility_type: str = Form(...),
    location: str = Form(...),
    image: Optional[UploadFile] = File(None)
):
    """
    Active copilot trigger: staff or inspector uploads a photo or report.
    """
    # In a real app, upload image to GCS and get URL.
    image_url = f"gs://verdaterra-images/{image.filename}" if image else None
    
    initial_state: IncidentState = {
        "facility_id": facility_id,
        "facility_type": facility_type,
        "location": location,
        "image_url": image_url,
        "sensor_payload": None,
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
    
    return ActiveTriggerResponse(
        incident_id=result.get("incident_id", "unknown"),
        status=result.get("dispatch_status", "Failed")
    )
