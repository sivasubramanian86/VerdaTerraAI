import pytest
from verdaterrakai.agents.tools import AlloyDBMCPClient

def test_mcp_local_stubbing_read_incidents():
    # Since LOCAL_DEV_MODE is True by default, this hits python sqlite mock directly
    incidents = AlloyDBMCPClient.read_incidents("loc_bengaluru", 7)
    assert isinstance(incidents, list)

def test_mcp_local_stubbing_metrics():
    metrics = AlloyDBMCPClient.fetch_aggregated_metrics("loc_bengaluru")
    if metrics:
        assert metrics.hygiene_score >= 0
        assert metrics.location_id == "loc_bengaluru"

def test_mcp_local_stubbing_write_sensor():
    res = AlloyDBMCPClient.write_sensor_reading("sen_001", "ammonia_ppm", 10.0)
    assert res["status"] == "success"

def test_mcp_local_stubbing_update_incident():
    res = AlloyDBMCPClient.update_incident_status("inc_test", "resolved")
    assert res["status"] == "success"
    assert res["new_status"] == "resolved"
