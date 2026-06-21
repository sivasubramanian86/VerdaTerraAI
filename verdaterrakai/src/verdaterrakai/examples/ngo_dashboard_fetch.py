"""Fetch ward-level dashboard data from a local or deployed VerdaTerraAI API."""

import os

import requests

API_KEY = os.getenv("API_KEY", "replace-with-local-demo-key")
BASE_URL = os.getenv("VERDATERRA_API_URL", "http://localhost:8080")
HEADERS = {"X-API-Key": API_KEY}


def fetch_ward_data(location_id: str) -> None:
    """Print metrics and hotspot data for a ward dashboard."""
    print(f"Fetching NGO Dashboard data for: {location_id}...")

    metrics_response = requests.get(
        f"{BASE_URL}/api/v1/locations/{location_id}/metrics",
        headers=HEADERS,
        timeout=10,
    )
    if metrics_response.status_code == 200:
        print("Metrics:", metrics_response.json())
    else:
        print("Error fetching metrics:", metrics_response.status_code, metrics_response.text)

    hotspots_response = requests.get(
        f"{BASE_URL}/api/v1/locations/{location_id}/hotspots?lat=12.97&lon=77.59",
        headers=HEADERS,
        timeout=10,
    )
    if hotspots_response.status_code == 200:
        print("Top Hotspots:", hotspots_response.json())
    else:
        print("Error fetching hotspots:", hotspots_response.status_code, hotspots_response.text)


if __name__ == "__main__":
    fetch_ward_data("loc_bengaluru_ward_15")
