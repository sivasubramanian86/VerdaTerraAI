import asyncio
import logging
from verdaterrakai.app.main import app
from fastapi.testclient import TestClient

# Configure logging to see the guardrails in action
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = TestClient(app)
from verdaterrakai.config.settings import settings
API_KEY = settings.api_key
HEADERS = {"X-API-Key": API_KEY}

def run_scenario_1_toilet():
    print("\n=== SCENARIO 1: The Multi-Sensory Public Toilet ===")
    payload = {
        "location_id": "loc_bengaluru_ward_15",
        "description": "Visually clean, but smells toxic.",
        "sensor_payload": {"ammonia_ppm": 65, "voc_ppm": 120}
    }
    response = client.post("/api/v1/incidents/submit", json=payload, headers=HEADERS)
    print(f"Submit Status: {response.status_code}")
    print(f"Submit Response: {response.json()}")
    assert response.status_code == 200

    # Fetch metrics to see if it impacted the hygiene snapshot
    res_metrics = client.get("/api/v1/locations/loc_bengaluru_ward_15/metrics", headers=HEADERS)
    print(f"Metrics Fetched: {res_metrics.json()}")
    assert res_metrics.status_code == 200

def run_scenario_2_restaurant():
    print("\n=== SCENARIO 2: Delhi Unhygienic Restaurant (Routing Adapter) ===")
    # To test routing and localization, we hit the campaign endpoint 
    # (Assume the incident was already submitted)
    payload = {
        "issue_description": "Overflowing commercial garbage bin behind restaurant in Delhi.",
        "audience": "Restaurant Manager",
        "locale": "hi-IN"
    }
    response = client.post("/campaign", json=payload)  # Note: Campaign endpoint currently doesn't require API key in main.py, but we test it.
    print(f"Campaign Status: {response.status_code}")
    print(f"Campaign Output: {response.json().get('campaign', {}).get('checklist', [])}")
    assert response.status_code == 200

def run_scenario_3_guardrail():
    print("\n=== SCENARIO 3: PII Security Guardrail ===")
    payload = {
        "message": "My Aadhaar is 1234 5678 9012 and the street is dirty."
    }
    # Calling the ADK chat mesh directly
    response = client.post("/chat", json=payload)
    print(f"Chat Response: {response.json()['response']}")
    assert response.status_code == 200
    assert "Security Violation" in response.json()["response"]

if __name__ == "__main__":
    print("Starting VerdaTerraAI E2E Demo Test Suite...")
    run_scenario_1_toilet()
    run_scenario_2_restaurant()
    run_scenario_3_guardrail()
    print("\nOK: All E2E Demo Scenarios Passed!")

