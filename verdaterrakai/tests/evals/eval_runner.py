import json
import sys
from unittest.mock import patch
import os

# Adjust python path if necessary
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from verdaterrakai.agents.sub_agents import hygiene_hotspot_agent_stub, routing_governance_agent_stub
from verdaterrakai.agents.types import PerceivedEnvironmentState

class MockMetrics:
    def __init__(self, open_incidents):
        self.open_incidents = open_incidents

def run_hygiene_evals(cases):
    passed = 0
    for case in cases:
        print(f"Testing {case['id']}: {case['desc']}...")
        
        # Build mocked AgentState
        perceived = PerceivedEnvironmentState(
            unified_criticality_score=case['input_criticality'],
            vision_labels=[],
            water_quality_issues=[],
            vibration_anomalies=[],
            noise_anomalies=[]
        )
        
        state = {
            "perceived_state": perceived
        }
        
        mock_metrics = MockMetrics(case['mock_open_incidents'])
        
        # Patch AlloyDB calls inside the agent
        with patch('verdaterrakai.agents.sub_agents.AlloyDBMCPClient.fetch_aggregated_metrics', return_value=mock_metrics):
            result = hygiene_hotspot_agent_stub(state)
            
        hygiene = result.get('hygiene_status', {})
        score = hygiene.get('hygiene_score')
        risk = hygiene.get('risk_classification')
        
        min_s, max_s = case['expected_score_range']
        if min_s <= score <= max_s and risk == case['expected_risk']:
            print(f"  [PASS] Score: {score}, Risk: {risk}")
            passed += 1
        else:
            print(f"  [FAIL] Expected [{min_s}-{max_s}] '{case['expected_risk']}', got Score {score} '{risk}'")
            
    return passed, len(cases)

def run_routing_evals(cases):
    passed = 0
    for case in cases:
        print(f"Testing {case['id']}: {case['desc']}...")
        
        # Build mocked AgentState
        perceived = PerceivedEnvironmentState(
            unified_criticality_score=0,
            vision_labels=[],
            water_quality_issues=["anomaly"] if case['water_quality_issues'] else [],
            vibration_anomalies=[],
            noise_anomalies=[]
        ) if case['water_quality_issues'] is not None else None
        
        state = {
            "perceived_state": perceived,
            "hygiene_status": {"risk_classification": case['risk_classification']} if case['risk_classification'] is not None else {}
        }
        
        # We need to mock AlloyDBMCPClient.read_incidents and update_incident_status since routing calls them
        with patch('verdaterrakai.agents.sub_agents.AlloyDBMCPClient.read_incidents', return_value=[]), \
             patch('verdaterrakai.agents.sub_agents.AlloyDBMCPClient.update_incident_status', return_value=None):
            result = routing_governance_agent_stub(state)
            
        routing = result.get('routing_status', {}).get('routing_decision', {})
        dept = routing.get('department')
        esc = routing.get('escalation_path')
        
        if dept == case['expected_dept'] and esc == case['expected_escalation']:
            print(f"  [PASS] Dept: {dept}, Escalation: {esc}")
            passed += 1
        else:
            print(f"  [FAIL] Expected {case['expected_dept']}/{case['expected_escalation']}, got {dept}/{esc}")
            
    return passed, len(cases)

def main():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'golden_set.json'), 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Failed to load golden set: {e}")
        sys.exit(1)
        
    print("\n--- Running AI Evaluation Harness ---\n")
    
    print("\n[1] Evaluating Hygiene Scoring Logic...")
    h_passed, h_total = run_hygiene_evals(data.get('hygiene_cases', []))
    
    print("\n[2] Evaluating Routing Governance Logic...")
    r_passed, r_total = run_routing_evals(data.get('routing_cases', []))
    
    total_passed = h_passed + r_passed
    total_cases = h_total + r_total
    
    print("\n--- Eval Summary ---")
    print(f"Total Cases: {total_cases}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_cases - total_passed}")
    print(f"Accuracy: {(total_passed / total_cases) * 100:.1f}%")
    
    if total_passed < total_cases:
        print("\n[!] EVALUATION FAILED. Accuracy must be 100%.")
        sys.exit(1)
    else:
        print("\n[+] EVALUATION PASSED. All agents performed within tolerance.")
        sys.exit(0)

if __name__ == "__main__":
    main()
