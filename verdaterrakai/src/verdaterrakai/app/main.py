from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from typing import Optional
import uuid
from verdaterrakai.utils.logger import setup_logger

logger = setup_logger(__name__)
from pydantic import BaseModel
from verdaterrakai.config.settings import settings
from verdaterrakai.agents.planner_agent import graph
from verdaterrakai.agents.civic_campaign_agent import generate_campaign_node, CampaignContent

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == settings.api_key:
        return api_key_header
    raise HTTPException(status_code=403, detail="Could not validate API Key")

app = FastAPI(
    title="VerdaTerraAI Agent API",
    description="ADK Python Agent for VerdaTerraAI",
    version="0.1.0"
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    status: str

class CampaignRequest(BaseModel):
    issue_description: str
    audience: str
    locale: str = "en-IN"

class CampaignResponse(BaseModel):
    status: str
    campaign: CampaignContent

class IncidentSubmissionRequest(BaseModel):
    location_id: str
    description: str
    image_base64: Optional[str] = None
    sensor_payload: Optional[dict] = None


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "environment": settings.environment,
        "project": settings.google_cloud_project
    }

@app.get("/ready")
def readiness_check():
    return {"status": "ready"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Simple HTTP entrypoint compatible with Cloud Run.
    Invokes the ADK LangGraph agent mesh.
    """
    try:
        # Initialize state with the input message
        corr_id = str(uuid.uuid4())
        logger.info("Received chat request", extra={"correlation_id": corr_id, "event_type": "REQUEST_START"})
        
        initial_state = {
            "correlation_id": corr_id,
            "location_id": "loc_bengaluru",  # Default for chat, can be parameterized
            "messages": [{"role": "user", "content": request.message}],
            "perception_status": "",
            "smell_status": "",
            "water_status": "",
            "hygiene_status": "",
            "policy_status": "",
            "impact_status": "",
            "routing_status": "",
            "final_response": ""
        }
        
        # Invoke the LangGraph ADK mesh asynchronously
        result = await graph.ainvoke(initial_state)
        
        return ChatResponse(
            response=result.get("final_response", "No response generated."),
            status="success"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/campaign", response_model=CampaignResponse)
async def campaign_endpoint(request: CampaignRequest):
    try:
        result = generate_campaign_node(request.issue_description, request.audience, request.locale)
        return CampaignResponse(status="success", campaign=result["campaign"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/locations/{location_id}/hotspots", dependencies=[Depends(get_api_key)])
async def get_v1_hotspots(location_id: str, lat: float = 12.9716, lon: float = 77.5946, radius_km: float = 5.0, issue_type: str = "smell"):
    try:
        from verdaterrakai.agents.tools import AlloyDBMCPClient
        from verdaterrakai.agents.guardrails import sanitize_for_public
        hotspots = AlloyDBMCPClient.query_hotspots(lat, lon, radius_km, issue_type)
        hotspots_dict = [h.model_dump() for h in hotspots]
        sanitized = sanitize_for_public({"hotspots": hotspots_dict})
        return {"status": "success", "hotspots": sanitized["hotspots"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/locations/{location_id}/metrics", dependencies=[Depends(get_api_key)])
async def get_v1_metrics(location_id: str):
    try:
        from verdaterrakai.agents.tools import AlloyDBMCPClient
        metrics = AlloyDBMCPClient.fetch_aggregated_metrics(location_id)
        if not metrics:
            return {"status": "success", "metrics": None}
        return {"status": "success", "metrics": {
            "hygiene_score": metrics.hygiene_score,
            "open_incidents": metrics.open_incidents,
            "odor_index": 42  # Stub
        }}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/incidents/submit", dependencies=[Depends(get_api_key)])
async def submit_incident(request: IncidentSubmissionRequest):
    try:
        from verdaterrakai.agents.tools import AlloyDBMCPClient
        # In reality, trigger ADK graph for triage. We'll just mock DB write here.
        AlloyDBMCPClient.write_sensor_reading("ext_sensor_1", "civic_report", 1.0)
        return {"status": "success", "message": "Incident submitted for analysis"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/locations/{location_id}/hygiene", dependencies=[Depends(get_api_key)])
async def get_v1_hygiene(location_id: str):
    # Reusing metrics logic for hackathon to serve hygiene snapshot
    return await get_v1_metrics(location_id)


