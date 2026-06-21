from mcp.server.fastmcp import FastMCP
from .database_tools import (
    query_compliance_norms, read_incidents, update_incident_status,
    fetch_aggregated_metrics, search_nearby_hotspots, upsert_sensor_reading
)

mcp = FastMCP("VerdaTerra Toolbox")

@mcp.tool()
def query_compliance_norms_tool(jurisdiction_id: str, query_text: str, limit: int = 3) -> list:
    return query_compliance_norms(jurisdiction_id, query_text, limit)

@mcp.tool()
def read_incidents_tool(location_id: str, days_back: int) -> list:
    return read_incidents(location_id, days_back)

@mcp.tool()
def update_incident_status_tool(incident_id: str, new_status: str) -> dict:
    return update_incident_status(incident_id, new_status)

@mcp.tool()
def fetch_aggregated_metrics_tool(location_id: str) -> dict:
    return fetch_aggregated_metrics(location_id)

@mcp.tool()
def query_hotspots_tool(lat: float, lng: float, radius_km: float, category: str) -> list:
    return search_nearby_hotspots(lat, lng, radius_km, category)

@mcp.tool()
def write_sensor_reading_tool(sensor_id: str, reading_type: str, value: float) -> dict:
    return upsert_sensor_reading(sensor_id, reading_type, value)

if __name__ == "__main__":
    mcp.run()
