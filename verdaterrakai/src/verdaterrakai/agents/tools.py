import sys
import os
import logging
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from verdaterrakai.config.settings import settings
from verdaterrakai.app.caching import cached

logger = logging.getLogger(__name__)

# Add workspace root to import python stubs directly when in local dev mode
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")))
try:
    from mcp_toolbox import database_tools
except ImportError:
    database_tools = None

# --- Typed Contracts ---
class IncidentRecord(BaseModel):
    incident_id: str
    category: str
    severity: str
    status: str

class AggregatedMetrics(BaseModel):
    location_id: str
    hygiene_score: int
    open_incidents: int

class HotspotRecord(BaseModel):
    location_name: str
    active_critical_incidents: int

class AlloyDBMCPClient:
    """
    Robust ADK Wrapper for the AlloyDB MCP Toolbox.
    Supports LOCAL_DEV_MODE to directly invoke python stubs without network overhead.
    """
    
    @staticmethod
    def _execute(tool_name: str, **kwargs) -> Any:
        logger.info(f"Invoking MCP Tool: {tool_name} with {kwargs}")
        
        if settings.local_dev_mode and database_tools:
            # Bypass MCP network transport and hit local stubs
            func = getattr(database_tools, tool_name.replace("_tool", ""), None)
            if not func:
                raise ValueError(f"Stub {tool_name} not found in database_tools.")
            return func(**kwargs)
        else:
            # Production: Use official MCP Client (httpx/websockets to FastMCP server)
            # This block represents the live ADK transport integration.
            logger.warning(f"Production MCP call to {tool_name} is mocked for Hackathon.")
            return {"status": "mocked", "note": "Requires live MCP server connection."}

    @classmethod
    def read_incidents(cls, location_id: str, days_back: int = 7) -> List[IncidentRecord]:
        try:
            res = cls._execute("read_incidents", location_id=location_id, days_back=days_back)
            return [IncidentRecord(**r) for r in res]
        except Exception as e:
            logger.error(f"Error in read_incidents: {e}")
            return []

    @classmethod
    def write_sensor_reading(cls, sensor_id: str, reading_type: str, value: float) -> Dict:
        try:
            return cls._execute("upsert_sensor_reading", sensor_id=sensor_id, reading_type=reading_type, value=value)
        except Exception as e:
            logger.error(f"Error in write_sensor_reading: {e}")
            return {"status": "error", "error": str(e)}

    @classmethod
    def update_incident_status(cls, incident_id: str, new_status: str) -> Dict:
        try:
            return cls._execute("update_incident_status", incident_id=incident_id, new_status=new_status)
        except Exception as e:
            logger.error(f"Error in update_incident_status: {e}")
            return {"status": "error"}

    @classmethod
    @cached(ttl_seconds=900)  # 15 minutes cache for hygiene snapshots
    def fetch_aggregated_metrics(cls, location_id: str) -> Optional[AggregatedMetrics]:
        try:
            res = cls._execute("fetch_aggregated_metrics", location_id=location_id)
            return AggregatedMetrics(**res)
        except Exception as e:
            logger.error(f"Error in fetch_aggregated_metrics: {e}")
            return None

    @classmethod
    def query_hotspots(cls, lat: float, lng: float, radius_km: float, category: str) -> List[HotspotRecord]:
        try:
            res = cls._execute("search_nearby_hotspots", lat=lat, lng=lng, radius_km=radius_km, category=category)
            return [HotspotRecord(**r) for r in res]
        except Exception as e:
            logger.error(f"Error in query_hotspots: {e}")
            return []

class PolicyRAGTool:
    """Wrapper specifically for RAG operations, integrated into the same MCP layer."""
    
    @staticmethod
    @cached(ttl_seconds=86400)  # 24 hours cache for RAG
    def search_policies(jurisdiction_id: str, query_text: str, limit: int = 3) -> dict:
        try:
            results = AlloyDBMCPClient._execute("query_compliance_norms", jurisdiction_id=jurisdiction_id, query_text=query_text, limit=limit)
            snippets = [f"Title: {r['title']}\nRule: {r['content']}\n" for r in results]
            return {
                "status": "success",
                "citations": [r['title'] for r in results],
                "combined_text": "\n---\n".join(snippets)
            }
        except Exception as e:
            logger.error(f"RAG Error: {e}")
            return {"status": "error"}
