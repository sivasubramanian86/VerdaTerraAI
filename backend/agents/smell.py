from typing import Dict, Any
from .state import IncidentState

def smell_node(state: IncidentState) -> Dict[str, Any]:
    """
    Smell Agent (E-Nose)
    Evaluates gas sensor telemetry.
    """
    payload = state.get("sensor_payload", {})
    if not payload:
        return {"olfactory_score": 100, "olfactory_flags": []}
        
    print(f"[Smell Agent] Analyzing sensor payload: {payload}")
    
    ammonia = payload.get("ammonia_ppm", 0)
    flags = []
    score = 100
    
    if ammonia > 50:
        flags.append("Critical Ammonia Level (>50ppm)")
        score = 10
    elif ammonia > 20:
        flags.append("High Ammonia Level")
        score = 60
        
    return {
        "olfactory_score": score,
        "olfactory_flags": flags
    }
