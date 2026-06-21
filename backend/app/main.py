from fastapi import FastAPI
from .api.routes import active, passive

app = FastAPI(title="VerdaTerraAI Ingress API", version="1.0.0")

app.include_router(active.router, prefix="/api/active", tags=["Active Triggers"])
app.include_router(passive.router, prefix="/api/passive", tags=["Passive Triggers"])

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}
