# VerdaTerraAI

VerdaTerraAI is a multi-sensory environmental intelligence platform for civic hygiene operations. It combines citizen reports, visual signals, smell/water sensor payloads, policy retrieval, and governance routing into an ADK-style Python agent mesh that can triage incidents for hotels, public toilets, garbage points, and ward-level command centers.

The project is designed for the Gen AI APAC 2026 hackathon problem space: make civic environmental monitoring more proactive, explainable, privacy-aware, and operationally useful for Indian cities while keeping the architecture extensible to other jurisdictions.

## What It Does

- Accepts active reports and passive sensor events through FastAPI services.
- Uses a planner/perception/hygiene/policy/routing agent mesh under `verdaterrakai/src/verdaterrakai/agents`.
- Routes incidents with location-aware jurisdiction adapters and MCP-style database tools.
- Produces multilingual civic campaign content for establishments and citizens.
- Protects sensitive civic data with prompt-injection blocking, PII redaction, and public response sanitization.
- Includes a React/Vite dashboard for command-center and inspector workflows.

## Architecture

```text
Citizen / Sensor / Inspector
        |
        v
FastAPI ingress + VerdaTerraAI Agent API
        |
        v
Planner Agent -> Perception Agent -> Hygiene/Policy/Water/Smell Agents
        |
        v
Routing Governance + Civic Campaign Agent
        |
        v
MCP Toolbox / AlloyDB-compatible data layer / dashboard
```

Key paths:

- `verdaterrakai/src/verdaterrakai/app/main.py` - primary agent API.
- `verdaterrakai/src/verdaterrakai/agents/` - typed agent mesh, guardrails, and tools.
- `mcp_toolbox/` - MCP-compatible database and ULB integration tools.
- `database/` - local schema and seed data for development.
- `verdaterra-ui/` - React dashboard.
- `verdaterrakai/tests/` - unit, API, integration, E2E, and AI evaluation tests.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 19, Vite, ESLint |
| API | FastAPI, Uvicorn, Pydantic Settings |
| Agent mesh | Python ADK-style graph, typed sub-agents, MCP tool interfaces |
| Data | Local SQLite seed data for development, AlloyDB AI target, BigQuery export plan |
| Security | API-key protected routes, PII redaction, public payload sanitization, gitleaks CI |
| Testing | pytest, FastAPI TestClient, golden-set AI eval runner, frontend lint/build |

## Local Setup

```bash
cd verdaterrakai
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev,test]"
copy ..\.env.example .env
make test
make eval
make run
```

The API runs on `http://localhost:8080` by default. Protected v1 routes require `X-API-Key`; set `API_KEY` in `.env` or your deployment secret manager.

For the UI:

```bash
cd verdaterra-ui
npm install
npm run lint
npm run build
npm run dev
```

## API Highlights

- `GET /health` - health probe.
- `GET /ready` - readiness probe.
- `POST /chat` - invokes the agent mesh.
- `POST /campaign` - generates localized civic campaign content.
- `POST /api/v1/incidents/submit` - submits incident/sensor payloads.
- `GET /api/v1/locations/{location_id}/hotspots` - returns sanitized hotspots.
- `GET /api/v1/locations/{location_id}/metrics` - returns aggregated hygiene metrics.
- `GET /api/v1/locations/{location_id}/hygiene` - returns hygiene snapshot data.

## Evaluation Checklist

This repository is organized to satisfy the Gemini `ai-evaluator-100`, security, QA, frontend accessibility, VCS, and hackathon demo criteria:

- Code quality: typed Pydantic contracts, small agent modules, Makefile targets for `test`, `eval`, `lint`, and `format`.
- Accessibility: dashboard workflows use semantic form controls, visible labels, accessible image alt text, keyboard-friendly native inputs, and reduced-motion-aware CSS.
- Security: no real secrets are committed; `.env*`, key files, service-account JSON, local databases, virtualenvs, and generated caches are ignored.
- Privacy: guardrails redact Aadhaar/phone-like PII, hard-abort prompt-injection attempts, and remove exact coordinates from public API payloads.
- Testing: `pytest` coverage spans API, core logic, localization, caching, routing, MCP integration, E2E flows, and policy RAG.
- AI evaluation: `verdaterrakai/tests/evals/eval_runner.py` validates hygiene scoring and routing decisions against `golden_set.json`.
- CI hygiene: `.github/workflows/security_audit.yml` runs gitleaks on pushes and pull requests.
- Problem alignment: the demo scenarios cover multi-sensory public-toilet risk, restaurant waste routing, security recovery, multilingual campaign output, and future BigQuery analytics.

## Pre-Submission Commands

```bash
# Secret scan, excluding generated and dependency folders
rg -n "sk-|AIza|AKIA|ghp_|ghs_|xox[baprs]-|-----BEGIN .*PRIVATE KEY|mongodb\+srv://|postgresql://[^\s]+:[^\s]+@|mysql://[^\s]+:[^\s]+@" -g "!venv/**" -g "!node_modules/**" -g "!**/__pycache__/**" -g "!**/.pytest_cache/**"

# Backend quality gates
cd verdaterrakai
make lint
make test
make eval

# Frontend quality gates
cd ../verdaterra-ui
npm run lint
npm run build
```

## Security

See `SECURITY.md` for the threat model, implemented controls, and disclosure guidance. Runtime secrets should be supplied through `.env` for local development and Secret Manager or equivalent cloud-managed secrets for deployment; do not commit real API keys, service account files, databases, or generated reports.

## Demo

Use `DEMO.md` for the four-minute judge walkthrough. It includes fallback CLI calls, but all credentials are placeholders and should be replaced with local/deployment secrets at runtime.

## Future Analytics

AlloyDB AI serves as the operational datastore and RAG vector engine for the live agent mesh. The v2 analytics plan exports incident facts and hygiene snapshots into BigQuery so government stakeholders can run ward-level Looker Studio dashboards without slowing down real-time operations.

See `verdaterrakai/src/verdaterrakai/analytics/bq_export.py` for the draft schema and ETL outline.
