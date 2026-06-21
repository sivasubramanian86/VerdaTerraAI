from typing import Dict, Any
from .types import AgentState
from .tools import PolicyRAGTool, AlloyDBMCPClient

from .types import HygieneSnapshot, RemediationAction, PoCRoutingDecision, DraftComplaint
from .guardrails import check_pii_leakage
from verdaterrakai.utils.logger import setup_logger

logger = setup_logger(__name__)

def hygiene_hotspot_agent_stub(state: AgentState) -> Dict[str, Any]:
    """
    Computes a deterministic Hygiene Score based on live sensor data
    and historical incidents via MCP Toolbox.
    """
    perceived = state.get("perceived_state")
    metrics = AlloyDBMCPClient.fetch_aggregated_metrics("loc_bengaluru")
    
    base_score = 100
    issues = []
    remediations = []
    
    if perceived:
        # Penalize score based on perceived anomaly severity (max penalty 40)
        penalty = min(perceived.unified_criticality_score, 40)
        base_score -= penalty
        if penalty > 0:
            issues.append(f"Live sensor anomalies detected (criticality {perceived.unified_criticality_score})")
            remediations.append(RemediationAction(priority="High", description="Investigate immediate sensor anomalies."))
            
    if metrics:
        # Penalize score based on open historical incidents (10 points each)
        base_score -= min(metrics.open_incidents * 10, 50)
        if metrics.open_incidents > 0:
            issues.append(f"{metrics.open_incidents} unresolved historical incidents.")
            remediations.append(RemediationAction(priority="Medium", description="Resolve pending historical complaints."))
            
    hygiene_score = max(0, base_score)
    
    if hygiene_score < 50:
        risk = "High"
    elif hygiene_score <= 80:
        risk = "Medium"
    else:
        risk = "Low"
        
    snapshot = HygieneSnapshot(
        hygiene_score=hygiene_score,
        trend="Declining" if metrics and metrics.open_incidents > 2 else "Improving",
        risk_classification=risk,
        open_issues_summary=issues,
        remediation_actions=remediations
    )
    return {"hygiene_status": snapshot.model_dump()}

def impact_simulation_agent_stub(state: AgentState) -> Dict[str, Any]:
    """
    Queries PostGIS spatial mock for nearby incident blast radius.
    """
    hotspots = AlloyDBMCPClient.query_hotspots(12.9716, 77.5946, 5.0, "smell")
    return {"impact_status": f"Found {len(hotspots)} critical hotspots nearby."}

def routing_governance_agent_stub(state: AgentState) -> Dict[str, Any]:
    """
    Routes complaints to the correct civic department and formulates a draft complaint.
    """
    from verdaterrakai.config.jurisdictions import JurisdictionRegistry
    perceived = state.get("perceived_state")
    loc_id = state.get("location_id", "loc_bengaluru")
    jurisdiction = JurisdictionRegistry.get_jurisdiction(loc_id)
    overrides = jurisdiction.routing_overrides if jurisdiction else {}
    
    dept = overrides.get("SWM Dept", "SWM Dept")
    role = "Waste Inspector"
    path = None
    
    if perceived and perceived.water_quality_issues:
        dept = overrides.get("Water Board", "Water Board")
        role = "Water Quality Engineer"
    
    # Check escalation
    hygiene_dict = state.get("hygiene_status", {})
    if hygiene_dict.get("risk_classification") == "High":
        path = "Zonal Commissioner"
        
    decision = PoCRoutingDecision(department=dept, role=role, escalation_path=path)
    draft = DraftComplaint(
        complaint_body=f"Automated complaint routed to {dept}. Immediate action requested.",
        routing_decision=decision
    )
    
    # Update incident in DB simulating auto-dispatch
    incidents = AlloyDBMCPClient.read_incidents("loc_bengaluru", 1)
    if incidents:
        AlloyDBMCPClient.update_incident_status(incidents[0].incident_id, "dispatched")
        
    return {"routing_status": draft.model_dump()}

def policy_rag_agent_stub(state: AgentState) -> Dict[str, Any]:
    current_trace = state.get("reasoning_trace", [])
    messages = state.get("messages", [])
    query = messages[-1]["content"] if messages else "Check compliance"
    from verdaterrakai.config.jurisdictions import JurisdictionRegistry
    loc_id = state.get("location_id", "loc_bengaluru")
    jurisdiction = JurisdictionRegistry.get_jurisdiction(loc_id)
    packs = jurisdiction.policy_packs if jurisdiction else ["national_swachh_bharat"]
    
    # In a real implementation we would pass the packs list. 
    # For the mock tool we just pass loc_id and we'll log it.
    rag_result = PolicyRAGTool.search_policies(jurisdiction_id=loc_id, query_text=query)
    context_text = rag_result.get("combined_text", "")
    citations = rag_result.get("citations", [])
    
    synthesis = ""
    checklist = []
    if "ammonia" in query.lower() and "Swachh Bharat" in context_text:
        synthesis = "Violation Detected: Ammonia levels do not meet Swachh Bharat Norms."
        checklist = ["[ ] Clean facility immediately", "[ ] Test Ammonia levels < 50 ppm", "[ ] Log closure if threshold exceeded"]
    elif "segregate" in query.lower() and "BBMP" in context_text:
        synthesis = "Violation Detected: Kitchen waste > 50kg must be source segregated per BBMP."
        checklist = ["[ ] Enforce source segregation"]
    elif ("cover" in query.lower() or "open trash" in query.lower()) and "FSSAI" in context_text:
        synthesis = "Violation Detected: All commercial bins must be covered per FSSAI."
        checklist = ["[ ] Procure covers for all kitchen bins"]
    else:
        synthesis = "No specific violations found in local RAG corpus."
        checklist = ["[ ] Maintain SOPs"]

    final_output = f"Synthesis: {synthesis}\nCitations: {', '.join(citations)}\n\nRemediation SOP:\n" + "\n".join(checklist)
    
    is_pii, reason = check_pii_leakage(final_output)
    if is_pii:
        corr_id = state.get("correlation_id", "unknown")
        logger.warning(f"SECURITY_VIOLATION: {reason}", extra={"correlation_id": corr_id})
        final_output = "[REDACTED] Policy output contained sensitive data and was blocked."
    return {
        "policy_status": "complete",
        "final_response": final_output,
        "reasoning_trace": current_trace + [f"[Policy RAG] Retrieved {len(citations)} rules and generated SOP."]
    }
