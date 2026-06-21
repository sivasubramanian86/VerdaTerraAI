import pytest
from verdaterrakai.agents.types import (
    VisionInput, GasSensorInput, WaterSensorInput, AgentState
)
from verdaterrakai.agents.perception_agent import perception_node
from verdaterrakai.agents.planner_agent import planner_node, graph

def test_perception_normalization():
    state: AgentState = {
        "vision_input": VisionInput(image_url="http://test.com/img.jpg"),
        "gas_input": GasSensorInput(ammonia_ppm=25.0, h2s_ppm=2.0, voc_index=0.0),
        "water_input": WaterSensorInput(ph_level=9.0, turbidity_ntu=2.0),
        "messages": [],
        "audio_input": None,
        "vibration_input": None,
        "reasoning_trace": [],
        "next_action": "",
        "perceived_state": None,
        "final_response": ""
    }
    
    result = perception_node(state)
    perceived = result["perceived_state"]
    
    assert "Simulated: Detected unsegregated waste" in perceived.visual_anomalies
    assert "High Ammonia Level" in perceived.odor_profile
    assert "Abnormal pH: 9.0" in perceived.water_quality_issues
    assert perceived.unified_criticality_score == 75
    assert len(result["reasoning_trace"]) == 1
    assert "Analyzed 5 modalities" in result["reasoning_trace"][0]

@pytest.mark.asyncio
async def test_planner_routing_to_perception():
    state: AgentState = {
        "messages": [{"role": "user", "content": "Analyze this image."}],
        "vision_input": None,
        "gas_input": None,
        "water_input": None,
        "audio_input": None,
        "vibration_input": None,
        "reasoning_trace": [],
        "next_action": "",
        "perceived_state": None,
        "final_response": ""
    }
    
    result = await planner_node(state)
    assert result["next_action"] == "perception"
    assert "image keywords" in result["reasoning_trace"][0]

@pytest.mark.asyncio
async def test_planner_routing_direct_response():
    state: AgentState = {
        "messages": [{"role": "user", "content": "Hello!"}],
        "vision_input": None,
        "gas_input": None,
        "water_input": None,
        "audio_input": None,
        "vibration_input": None,
        "reasoning_trace": [],
        "next_action": "",
        "perceived_state": None,
        "final_response": ""
    }
    
    result = await planner_node(state)
    assert result["next_action"] == "END"
    assert "generic question" in result["reasoning_trace"][0]
