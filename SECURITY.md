# VerdaTerraAI Secure AI Posture

## Threat Model

VerdaTerraAI handles civic reports, sensor payloads, agent reasoning, and public-facing hygiene summaries. The main risks are:

- PII leakage from citizen text, uploaded images, phone numbers, Aadhaar-like identifiers, or precise addresses.
- Prompt injection that attempts to override policy, routing, or public health decisions.
- Geospatial privacy exposure from exact latitude/longitude in public endpoints.
- Secret exposure through local `.env` files, service-account JSON, generated databases, logs, or demo snippets.
- Overly broad cloud IAM when moving from hackathon prototype to production deployment.

## Implemented Controls

### Environment-Based Secrets

Runtime API keys are read from settings/environment (`API_KEY`). The repository includes `.env.example` with placeholders only, and the root `.gitignore` excludes `.env*`, key files, service-account JSON, generated local databases, caches, and build outputs.

### Hard-Abort Guardrails

`verdaterrakai/src/verdaterrakai/agents/guardrails.py` blocks known prompt-injection and PII patterns before the planner continues. Security violations return an escalation path rather than attempting an LLM-generated workaround.

### Logging Redaction

`redact_for_log` scrubs phone/Aadhaar-like identifiers and replaces them with `[REDACTED_PII]` before structured logs are emitted. Logs should contain correlation IDs, event names, and operational metadata, not full request bodies.

### Public API Sanitization

`sanitize_for_public` strips exact coordinates and private inspector IDs from public response objects. Public APIs should expose aggregated or rounded civic data only.

### CI Secret Scanning

`.github/workflows/security_audit.yml` runs gitleaks on push and pull request. Local pre-flight scanning is documented in `README.md` and `AI_EVALUATION.md`.

## Data Classification

| Class | Examples | Handling |
|---|---|---|
| Public | Aggregated heatmaps, ward-level trend summaries, generic odor indexes | Safe for dashboards and public APIs after sanitization |
| Internal | Establishment records, non-critical incidents, routing metadata | Authenticated operator access only |
| Sensitive | Live hygiene scores, inspection SOPs, detailed compliance notes | Restricted service access; avoid public exposure |
| Highly Sensitive | Aadhaar-like IDs, phone numbers, exact home coordinates, API keys | Redact, block, or store only in approved secret/privacy systems |

## Production Cloud Guidance

- Store production secrets in Google Secret Manager or an equivalent managed secret store.
- Prefer workload identity or managed service identity over downloadable service-account keys.
- Keep the public frontend unauthenticated only if needed; protect agent and MCP services with service-to-service IAM.
- Use least-privilege IAM roles such as Cloud Run Invoker and Secret Manager Secret Accessor instead of Editor/Owner.
- Enable Cloud Audit Logs for sensitive data systems and route security findings to the incident process.
- For internal Cloud Run services, use `--no-allow-unauthenticated`.

## Required Pre-Push Checks

```bash
rg -n "sk-|AIza|AKIA|ghp_|ghs_|xox[baprs]-|-----BEGIN .*PRIVATE KEY|mongodb\+srv://|postgresql://[^\s]+:[^\s]+@|mysql://[^\s]+:[^\s]+@" -g "!venv/**" -g "!node_modules/**" -g "!**/__pycache__/**" -g "!**/.pytest_cache/**"

cd verdaterrakai
make lint
make test
make eval
```

## Future Work

- Replace regex-only PII detection with Google Cloud DLP for semantic redaction.
- Add formal RBAC using Cloud Identity/Firebase Auth or an enterprise identity provider.
- Expand adversarial prompt and jailbreak evals in `verdaterrakai/tests/evals`.
- Add CSP/CORS hardening once final frontend/backend deployment domains are known.
