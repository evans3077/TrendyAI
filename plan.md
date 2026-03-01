# TrendyAI Project Implementation Plan

## 1) Project Goal
Build a production-ready **AI video intelligence platform** that:
- Ingests creator videos and channel context.
- Performs multimodal analysis (audio, visual, text, metadata, trend context).
- Produces actionable recommendations to improve CTR, retention, and discoverability.
- Scales via cloud GPU workers (no dependency on local GPUs).

---

## 2) Current-State Review (What Already Exists)

### Backend foundations in place
- FastAPI app with route wiring in `backend/main.py`.
- Modules for:
  - Video analysis pipeline (`/video/analyze`): upload, audio extraction, frame extraction, transcription, summarization, metadata.
  - Content analysis pipeline (`/content/analyze`): transcript/summary generation, keywords/topics/sentiment, object detection, OCR, visual metrics.
  - Channel context retrieval (`/channel/{channel_id}`): YouTube Data API integration.
  - YouTube OAuth skeleton (`/auth/login`, `/auth/oauth2callback`).

### Data outputs already present
- Processed job folders in `data/processed/...` with transcripts, summaries, frames, and analysis JSON artifacts.

### Gaps identified
- No real frontend implementation yet (`frontend/package.json` is empty).
- Training/inference scripts are placeholders (`scripts/*.py` empty).
- Several production concerns are missing: queueing, background workers, persistent DB schema, storage abstraction, auth hardening, model lifecycle, observability, and CI/CD.
- Dependency setup is heavy and inconsistent in `backend/requirements.txt` (duplicates, mixed optional/runtime deps).
- Some code-level issues likely to fail at runtime (e.g., mismatched transcription call signature, path coupling assumptions, no job state machine).

---

## 3) Target Architecture

## 3.1 Logical Architecture
1. **Client apps** (web first, mobile-ready API).
2. **API service** (FastAPI): request validation, auth, job creation, status retrieval.
3. **Job queue** (Redis + RQ/Celery): decouple upload from inference.
4. **Worker pools**:
   - CPU workers: preprocessing, OCR, lightweight NLP.
   - GPU workers: Whisper large-v3, CLIP/vision encoders, ranking models.
5. **Storage**:
   - Object storage (S3/R2/MinIO) for video/audio/frame artifacts.
   - PostgreSQL for users, jobs, outputs, and recommendation history.
   - Redis for queue/cache.
6. **Trend Pattern Engine (TPE)**: independent trend crawler + feature service.
7. **Recommendation service**: prompt templates + structured scoring output.
8. **Observability**: logs, metrics, tracing, alerts.

## 3.2 Cloud GPU Strategy (No local GPU required)
Use on-demand GPU providers for inference/training:
- **Inference options**: RunPod, Lambda, Vast.ai, Modal, Replicate (provider choice by cost/latency).
- **Managed cloud**: AWS EC2 g5/g6, GCP L4/A100, Azure NC series.
- **Recommended initial setup**:
  - API + queue + DB on standard cloud VMs/managed services.
  - GPU workers as autoscaled spot/on-demand nodes.
  - Model artifacts in object storage + version metadata in DB.

---

## 4) Implementation Phases

## Phase 0 — Repo Stabilization (Week 1)
- Reorganize code layout and naming consistency.
- Split dependencies into:
  - `requirements/base.txt`
  - `requirements/inference.txt`
  - `requirements/dev.txt`
- Add `.env.example` and centralized config validation.
- Add strict linting/formatting (ruff, black, isort) and type checks (mypy optional).
- Add test harness with `pytest` and smoke tests for APIs.

**Exit criteria**
- App starts reliably in clean environment.
- `pytest` and lint pass in CI.

## Phase 1 — Job-Oriented Processing Backbone (Week 1–2)
- Introduce `Job` model and lifecycle (`queued`, `processing`, `completed`, `failed`).
- Replace inline processing endpoint with async workflow:
  1) upload -> create job
  2) enqueue job
  3) worker executes pipeline
  4) persist outputs + status
- Abstract local filesystem paths behind storage service.
- Add job status/result endpoints.

**Exit criteria**
- Long videos do not block API request lifecycle.
- Multiple concurrent jobs can run safely.

## Phase 2 — Core Multimodal Analyzer v1 (Week 2–4)
- Harden existing modules:
  - Whisper transcription chunking strategy.
  - Summarization chunk-map-reduce for long transcripts.
  - Frame sampling strategy tied to duration and scene changes.
  - OCR/object detection confidence thresholding + deduplication.
- Normalize analysis output into stable schema (`analysis_v1`).
- Add quality scoring and recommendation placeholders.

**Exit criteria**
- Deterministic JSON output schema for every completed job.
- Baseline metric report available per job.

## Phase 3 — Trend Pattern Engine (TPE) v1 (Week 4–6)
- Build daily crawler jobs for:
  - YouTube trends (official API)
  - Google Trends
  - Reddit topic velocity
- Build trend feature store (topic, growth rate, momentum, decay).
- Expose internal API: `GET /trends/context?category=...&region=...`.
- Link analyzer outputs to trend similarity scoring.

**Exit criteria**
- Recommendations include trend-aware context and confidence.

## Phase 4 — Recommendation Engine v1 (Week 6–7)
- Define recommendation schema:
  - problem
  - evidence
  - action
  - expected impact
  - confidence
- Build prompt templates using structured analysis + trend context.
- Add safeguards against unsupported claims.

**Exit criteria**
- Every recommendation is evidence-backed and machine-parseable.

## Phase 5 — Frontend Dashboard v1 (Week 6–8)
- Implement React dashboard modules:
  - Upload manager
  - Job status + progress
  - Report view (scores, highlights, recommendations)
  - Historical comparisons
- Add auth flow and user-specific project views.

**Exit criteria**
- End-to-end flow from upload to insights in browser.

## Phase 6 — MLOps + CI/CD + Production Readiness (Week 8–10)
- CI: lint, test, build, deploy.
- CD: staging then production with rollback.
- Monitoring: Prometheus/Grafana + structured logs.
- Security hardening: OAuth/JWT, secret management, rate limiting, signed URLs.
- Data retention controls and compliance defaults.

**Exit criteria**
- Production environment with SLO dashboards and alerting.

---

## 5) Workstreams and Ownership

- **Platform/API**: FastAPI architecture, auth, contracts, DB models.
- **ML/Inference**: transcript, vision, scoring models, optimization.
- **Trend Intelligence**: crawlers, feature engineering, forecasting.
- **Frontend**: UX, upload/report workflows.
- **DevOps/MLOps**: infra, CI/CD, observability, cost controls.

---

## 6) Data & API Contracts (Initial)

## 6.1 Core Entities
- User
- ChannelConnection
- AnalysisJob
- Artifact
- AnalysisResult
- Recommendation
- TrendSnapshot

## 6.2 Required Endpoints (v1)
- `POST /jobs` (upload + create)
- `GET /jobs/{id}` (status)
- `GET /jobs/{id}/result` (analysis)
- `GET /jobs/{id}/recommendations`
- `GET /channel/{channel_id}`
- `GET /trends/context`

---

## 7) GPU Cost/Performance Plan

- Start with **single GPU worker pool** (L4 or A10 class).
- Use autoscaling by queue depth and job age.
- Prefer spot/preemptible where retry-safe.
- Implement per-job cost telemetry (GPU minutes + model calls).
- Optimize in this order:
  1) batching
  2) precision/quantization
  3) model distillation
  4) caching repeated features

---

## 8) Definition of Done (Project-Level)

1. Upload-to-insight flow works reliably for short and long videos.
2. Analysis output schema is stable and versioned.
3. Recommendations are trend-aware and evidence-grounded.
4. Frontend dashboard supports upload, status, and full report display.
5. Cloud deployment supports autoscaling GPU inference.
6. CI/CD, monitoring, and security baselines are active.

---

## 9) Immediate Next Sprint Backlog (Actionable)

1. Implement job queue + worker process abstraction.
2. Add DB models + migrations for job/result lifecycle.
3. Refactor current analysis pipeline into independently testable steps.
4. Normalize file paths and artifact manifest format.
5. Replace monolithic requirements file with layered dependency files.
6. Build first frontend scaffold and connect to `/jobs` APIs.
7. Add smoke tests for `/video/analyze`, `/content/analyze`, `/channel/{id}`.

