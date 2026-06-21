from typing import Dict, Any
from .types import (
    AgentState, VisionInput, AudioInput, GasSensorInput, 
    WaterSensorInput, VibrationInput, PerceivedEnvironmentState
)
from .tools import AlloyDBMCPClient

# --- Sense Stubs ---

def analyze_sight(vision: VisionInput) -> list[str]:
    """TODO: Interface to Gemini Vision / Vertex AI Vision"""
    anomalies = []
    if vision and (vision.image_url or vision.image_bytes):
        anomalies.append("Simulated: Detected unsegregated waste")
    return anomalies

def analyze_hearing(audio: AudioInput) -> list[str]:
    """TODO: Interface to ASR / Audio Classification"""
    events = []
    if audio and audio.audio_url:
        events.append("Simulated: Detected running water sound")
    return events

def analyze_smell(gas: GasSensorInput) -> list[str]:
    """TODO: Gas sensor classification model"""
    profile = []
    if gas:
        if gas.ammonia_ppm > 20:
            profile.append("High Ammonia Level")
        if gas.h2s_ppm > 5:
            profile.append("Hazardous H2S Level")
    return profile

def analyze_taste(water: WaterSensorInput) -> list[str]:
    """TODO: Water quality threshold logic"""
    issues = []
    if water:
        if water.ph_level < 6.5 or water.ph_level > 8.5:
            issues.append(f"Abnormal pH: {water.ph_level}")
        if water.turbidity_ntu > 5.0:
            issues.append("High Turbidity")
    return issues

def analyze_touch(vibration: VibrationInput) -> list[str]:
    """TODO: Anomaly detection hooks for infra sensors"""
    alerts = []
    if vibration and vibration.structural_anomaly:
        alerts.append("Structural vibration anomaly detected")
    return alerts

# --- Main Perception Node ---

def perception_node(state: AgentState) -> Dict[str, Any]:
    """
    Normalizes inputs from all 5 sensory modalities into a single PerceivedEnvironmentState.
    """
    v_anomalies = analyze_sight(state.get("vision_input"))
    a_events = analyze_hearing(state.get("audio_input"))
    gas_in = state.get("gas_input")
    s_profile = analyze_smell(gas_in)
    w_issues = analyze_taste(state.get("water_input"))
    
    if gas_in:
        # Synchronously write the telemetry via MCP wrapper
        AlloyDBMCPClient.write_sensor_reading("sen_001", "ammonia_ppm", gas_in.ammonia_ppm)
    t_alerts = analyze_touch(state.get("vibration_input"))
    
    # Simple deterministic criticality weighting for the stub
    score = (len(v_anomalies) * 20) + (len(a_events) * 10) + (len(s_profile) * 30) + (len(w_issues) * 25) + (len(t_alerts) * 40)
    score = min(score, 100)
    
    normalized_state = PerceivedEnvironmentState(
        visual_anomalies=v_anomalies,
        audio_events=a_events,
        odor_profile=s_profile,
        water_quality_issues=w_issues,
        structural_alerts=t_alerts,
        unified_criticality_score=score
    )
    
    current_trace = state.get("reasoning_trace", [])
    
    # Return updates to LangGraph state
    return {
        "perceived_state": normalized_state,
        "reasoning_trace": current_trace + ["[Perception] Analyzed 5 modalities and normalized state."]
    }
