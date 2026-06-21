def dispatch_remediation_task(incident_id: str, ulb_ward_id: str, action_plan: str) -> dict:
    print(f"[ULB STUB] Dispatching task for incident {incident_id} to ward {ulb_ward_id}")
    print(f"[ULB STUB] Action plan: {action_plan}")
    return {"ulb_ticket_id": f"ULB-{incident_id[-6:].upper()}", "assigned_team": "Rapid Response Unit A"}
