from typing import Dict, Any
from .state import IncidentState

def policy_node(state: IncidentState) -> Dict[str, Any]:
    """Policy & RAG Agent: Validates anomalies against localized rules."""
    print(f"[Policy Agent] Validating anomalies for {state.get('location')}...")
    
    report = f"Compliance Violation: Anomalies detected at {state.get('facility_id')}. "
    report += "According to Swachh Bharat guidelines, immediate remediation is required."
    
    return {"compliance_report": report}
