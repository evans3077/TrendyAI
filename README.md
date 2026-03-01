# TrendyAI

TrendyAI is an AI-powered video intelligence platform for creators. It analyzes uploaded videos and channel context to produce actionable recommendations aimed at improving retention, CTR, and discoverability.

---

## Current Repository Status (Reviewed)

This repository already contains a **working backend prototype** with FastAPI endpoints and basic multimodal processing:

- `POST /video/analyze`
  - Upload video
  - Extract audio and frames
  - Transcribe speech
  - Generate summary
  - Save per-job artifacts + JSON output
- `GET /content/analyze?job_path=...`
  - Runs deeper text/visual/audio content analysis
  - Keyword extraction, topic extraction, sentiment, object detection, OCR, visual stats
- `GET /channel/{channel_id}`
  - Pulls YouTube channel metadata and upload list
- `GET /auth/login` and `GET /auth/oauth2callback`
  - OAuth skeleton for YouTube account connection

### What is currently incomplete

- Frontend app is not implemented yet.
- Training, preprocessing, evaluation, and inference scripts are placeholders.
- Queue-based async architecture is not implemented yet (current pipeline is mostly request-bound).
- Database persistence and production job lifecycle are not fully defined.
- MLOps/deployment/monitoring/security baselines need implementation.

---

## Recommended Product Direction

Use a **cloud-first architecture** where GPU workloads are executed on rentable GPU infrastructure (instead of relying on local GPUs).

### GPU recommendation

- Inference/training on cloud GPUs (RunPod, Lambda, Vast.ai, Modal, AWS/GCP/Azure GPU instances).
- Keep API, DB, and queue on normal compute instances.
- Autoscale GPU workers by queue depth and latency SLOs.

---

## Architecture (Target)

1. Client (web/mobile)
2. FastAPI gateway
3. Job queue (Redis + Celery/RQ)
4. CPU + GPU worker pools
5. PostgreSQL (metadata/results) + object storage (artifacts)
6. Trend Pattern Engine (separate crawler and trend context API)
7. Recommendation layer (structured insights)
8. Monitoring + alerting

---

## Full Execution Plan

A detailed implementation roadmap has been created in:

- [`plan.md`](./plan.md)

This includes:
- Current-state technical review
- Missing capabilities
- Phased implementation timeline
- GPU cloud strategy
- Data/API contract guidance
- Production readiness criteria

---

## Quickstart (Prototype Backend)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open:
- `http://localhost:8000/docs`

---

## Next Immediate Steps

1. Introduce async job queue and worker architecture.
2. Add persistent DB models for job lifecycle.
3. Normalize analysis output schema.
4. Implement frontend dashboard scaffold.
5. Add CI testing and deployment pipeline.

