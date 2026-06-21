from typing import Dict, Any
from .state import IncidentState

def perception_node(state: IncidentState) -> Dict[str, Any]:
    """
    Perception Agent (Sight & Audio)
    Uses Vertex AI Vision to evaluate image. For hackathon, we simulate.
    """
    image_url = state.get("image_url")
    if not image_url:
        return {"visual_score": 100, "visual_anomalies": []}
    
    print(f"[Perception Agent] Analyzing image at {image_url}")
    return {
        "visual_score": 40,
        "visual_anomalies": ["Bin overflow detected", "Visible filth on floor"]
    }
