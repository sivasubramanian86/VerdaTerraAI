import json
import os
import pytest
from verdaterrakai.agents.sub_agents import policy_rag_agent_stub
from verdaterrakai.agents.types import AgentState

DATASET_PATH = os.path.join(os.path.dirname(__file__), "eval_dataset.json")

def load_eval_data():
    with open(DATASET_PATH, "r") as f:
        return json.load(f)

@pytest.mark.parametrize("test_case", load_eval_data())
def test_policy_agent_evaluation(test_case):
    query = test_case["query"]
    
    # Setup mock Agent State
    state: AgentState = {
        "messages": [{"role": "user", "content": query}],
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
    
    # Run the Agent
    result = policy_rag_agent_stub(state)
    
    final_output = result["final_response"]
    
    # Evaluate expected phrases in the synthesized SOP
    assert test_case["expected_keyword"] in final_output, f"Missing citation for: {test_case['expected_keyword']}"
    assert test_case["expected_checklist_item"] in final_output, "Missing required checklist item"
