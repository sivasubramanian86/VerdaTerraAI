from typing import Dict, Any
import uuid
from .state import IncidentState

def routing_node(state: IncidentState) -> Dict[str, Any]:
    """Routing & Governance Agent: Drafts notifications and dispatches."""
    print("[Routing Agent] Drafting notifications and dispatching...")
    
    incident_id = f"inc_{uuid.uuid4().hex[:8]}"
    draft = f"URGENT: Hygiene incident logged for {state.get('facility_id')}. Criticality: {state.get('criticality_level')}"
    
    return {
        "incident_id": incident_id,
        "draft_notification": draft,
        "dispatch_status": "Dispatched to ULB API (Mock)"
    }
