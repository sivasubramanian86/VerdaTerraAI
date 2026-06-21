from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from typing_extensions import TypedDict
import operator

# Raw Input Data Structures
class VisionInput(BaseModel):
    image_url: Optional[str] = None
    image_bytes: Optional[bytes] = None

class AudioInput(BaseModel):
    audio_url: Optional[str] = None
    duration_sec: Optional[int] = None

class GasSensorInput(BaseModel):
    ammonia_ppm: float = 0.0
    h2s_ppm: float = 0.0
    voc_index: float = 0.0

class WaterSensorInput(BaseModel):
    ph_level: float = 7.0
    turbidity_ntu: float = 0.0

class VibrationInput(BaseModel):
    vibration_hz: float = 0.0
    structural_anomaly: bool = False

# Normalized Output Data Structure
class PerceivedEnvironmentState(BaseModel):
    visual_anomalies: List[str] = Field(default_factory=list)
    audio_events: List[str] = Field(default_factory=list)
    odor_profile: List[str] = Field(default_factory=list)
    water_quality_issues: List[str] = Field(default_factory=list)
    structural_alerts: List[str] = Field(default_factory=list)
    unified_criticality_score: int = 0  # 0 to 100

def merge_lists(a: List[str], b: List[str]) -> List[str]:
    return (a or []) + (b or [])

# LangGraph Agent State
class AgentState(TypedDict):
    # Observability
    correlation_id: str
    location_id: str
    
    # Multi-turn conversational state
    messages: List[Dict[str, str]]
    
    # Raw sensor inputs (if provided)
    vision_input: Optional[VisionInput]
    audio_input: Optional[AudioInput]
    gas_input: Optional[GasSensorInput]
    water_input: Optional[WaterSensorInput]
    vibration_input: Optional[VibrationInput]
    
    # ReAct / CoT Reasoning
    reasoning_trace: List[str]
    next_action: str  # Controls LangGraph routing
    
    # Synthesized state from Perception Agent
    perceived_state: Optional[PerceivedEnvironmentState]
    
    # Final response
    final_response: str
    
    # Agent outputs
    hygiene_status: Dict[str, Any]
    routing_status: Dict[str, Any]
    policy_status: str

# --- Hygiene & Routing Structures ---
class RemediationAction(BaseModel):
    priority: str
    description: str

class HygieneSnapshot(BaseModel):
    hygiene_score: int
    trend: str
    risk_classification: str
    open_issues_summary: List[str]
    remediation_actions: List[RemediationAction]

class PoCRoutingDecision(BaseModel):
    department: str
    role: str
    escalation_path: Optional[str] = None

class DraftComplaint(BaseModel):
    complaint_body: str
    routing_decision: PoCRoutingDecision
