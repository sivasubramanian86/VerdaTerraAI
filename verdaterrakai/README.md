# VerdaTerraAI ADK Agent

This is the ADK Python Starter project for VerdaTerraAI.

## Local Development

```bash
# Install dependencies
pip install -e ".[dev,test]"

# Run tests
make test

# Run API
make run
```

## Cloud Run Deployment

```bash
# Deploy using Google Cloud CLI
gcloud run deploy verdaterraai-agent \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars=GOOGLE_CLOUD_PROJECT=your-project-id
```

## Extending the RAG Corpus

To onboard new cities or jurisdictions to VerdaTerraAI:
1. Provide your local compliance guidelines (PDF/HTML) to the `Policy & Knowledge` engine.
2. Ensure documents are chunked (e.g. 1000 tokens) and embedded using Vertex AI `text-embedding-gecko`.
3. Insert the vectors into the AlloyDB `compliance_policies` table, strictly tagging them with the target `location_id` (e.g. `loc_delhi`).
4. The `PolicyRAGTool` will automatically apply the `location_id` metadata filter before performing semantic vector searches, ensuring hybrid retrieval correctly enforces local laws without hallucination.

## Deploying MCP Toolbox on Cloud Run

For production, the FastMCP server must be deployed to Cloud Run alongside the ADK Agent.

**Option A: Independent Internal Service (Recommended)**
1. Containerize the `mcp_toolbox` directory.
2. Deploy it to Cloud Run with `--ingress internal` to ensure it is not publicly accessible.
3. Configure the ADK Agent's Cloud Run environment variable `MCP_SERVER_URL` to point to the internal Cloud Run URL.

**Option B: Sidecar Deployment**
1. Use Cloud Run multi-container deployment.
2. Define both the ADK Agent container and the FastMCP container in the `service.yaml`.
3. The ADK Agent connects via `localhost:8080` (or whichever port the sidecar exposes).

## SRE Runbook & Deployment

**1. Production Deployment (Cloud Run)**
```bash
gcloud run deploy verdaterrakai \
  --source . \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-env-vars=ENVIRONMENT=production,MCP_SERVER_URL=http://internal-mcp-url \
  --set-secrets=API_KEY=my-secret-key:latest
```

**2. Rollback Procedure**
If a deployment fails the guardrail checks or health probes, instantly revert traffic to the previous revision:
```bash
gcloud run services update-traffic verdaterrakai --to-revisions=verdaterrakai-00001-abc=100
```

**3. City Adapter Onboarding**
To onboard a new city (e.g., Chennai):
- Insert city boundary polygons into AlloyDB PostGIS.
- Append local compliance rules to the `compliance_policies` RAG table tagged with `loc_chennai`.
- Update `localization.py` with specific dialect system prompts if necessary.
