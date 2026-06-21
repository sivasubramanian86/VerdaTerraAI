from typing import Dict, Any
from .state import IncidentState

def hygiene_node(state: IncidentState) -> Dict[str, Any]:
    """Hygiene & Hotspot Agent: Synthesizes final score"""
    v_score = state.get("visual_score", 100)
    o_score = state.get("olfactory_score", 100)
    
    avg_score = (v_score + o_score) / 2
    print(f"[Hygiene Agent] Synthesizing score. V:{v_score}, O:{o_score} -> Avg:{avg_score}")
    
    if avg_score < 30:
        criticality = "Critical"
    elif avg_score < 60:
        criticality = "High"
    elif avg_score < 80:
        criticality = "Medium"
    else:
        criticality = "Low"
        
    return {"criticality_level": criticality}
