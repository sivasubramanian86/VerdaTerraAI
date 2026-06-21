from typing import TypedDict, Optional, List, Dict, Any

class IncidentState(TypedDict):
    # Inputs
    facility_id: str
    facility_type: str
    location: str # e.g., 'Bengaluru, Karnataka'
    image_url: Optional[str]
    sensor_payload: Optional[Dict[str, Any]]
    
    # Modality Outputs
    visual_score: Optional[int]
    visual_anomalies: Optional[List[str]]
    olfactory_score: Optional[int]
    olfactory_flags: Optional[List[str]]
    water_score: Optional[int] # Stubbed
    
    # Synthesis
    criticality_level: Optional[str] # Low, Med, High, Critical
    
    # Policy
    compliance_report: Optional[str]
    
    # Routing
    incident_id: Optional[str]
    draft_notification: Optional[str]
    dispatch_status: Optional[str]
