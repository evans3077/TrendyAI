# TrendyAI (AutoInsightAI)

TrendyAI is an AI-powered creator intelligence platform that analyzes uploaded videos, channel context, and internet trend signals to generate practical recommendations for better **CTR**, **retention**, and **discoverability**.

This README is the unified project description that combines:
- your original product/architecture vision,
- the Trend Pattern Engine (TPE) concept,
- and the actual codebase status already implemented in this repository.

---

## 1) Product Vision

### Objective
Build a multimodal analysis system that helps creators answer:
- Is my hook strong enough?
- Is the emotional/audio delivery engaging?
- Do my title/tags/topic match what is currently trending?
- What exact changes should I make before publishing?

### Core Flow
`Upload video → Multimodal analysis pipeline → Trend/context matching → Recommendation generator → Actionable report`

Target experience: creator uploads content and receives a structured report with suggested fixes and expected impact.

---

## 2) Unified System Architecture

### High-level architecture
`Client App → FastAPI Gateway → Queue → CPU/GPU Workers → Storage + DB → Recommendation API → Dashboard`

### Layers
| Layer | Preferred Technology | Purpose |
|---|---|---|
| Frontend | React (Next.js), optional Flutter/React Native later | Upload videos, monitor jobs, view reports |
| API Gateway | FastAPI | REST/WebSocket APIs, auth, validation |
| Queue | Redis + Celery/RQ | Decouple uploads from long-running inference |
| Worker Fleet | Cloud GPU + CPU workers | Run ASR, NLP, vision, ranking, recommendations |
| Object Storage | S3 / MinIO / R2 | Raw uploads + derived artifacts |
| Database | PostgreSQL (+ Redis cache) | Users, jobs, metadata, results, recommendation history |
| Notifications | WebSocket / push | Real-time job completion updates |
| Monitoring | Prometheus + Grafana + logs | Reliability and performance tracking |

---

## 3) Core AI Pipeline (Product Design)

1. **Ingestion**
   - Upload video or connect channel.
2. **Preprocessing**
   - Extract audio (16 kHz WAV), sample frames/scenes, collect metadata.
3. **Feature extraction (multimodal)**
   - Speech-to-text, summarization, sentiment/tone, object/OCR/visual quality features.
4. **Trend correlation**
   - Compare video topics/features with trend index (TPE).
5. **Scoring**
   - Hook quality, clarity, relevance, likely performance indicators.
6. **Recommendation generation**
   - Evidence-based recommendations with confidence and impact hints.
7. **Report output**
   - Persist JSON result + dashboard-ready response.

---

## 4) Model Stack (Target + Practical)

### Planned/target components
- **Thumbnail/visual appeal**: CLIP / vision encoders.
- **Hook effectiveness (0–15s)**: temporal features + ASR context.
- **Audio sentiment/clarity**: ASR + sentiment/emotion signals.
- **Topic & SEO relevance**: embedding similarity + keyword relevance.
- **Performance predictor**: multimodal ranking/classification model.
- **Recommendation model**: LLM prompt engine over structured evidence.

### Currently implemented in repo (prototype)
- Whisper-based transcription.
- BART summarization.
- Keyword extraction (KeyBERT).
- Topic extraction (MiniLM embeddings).
- Sentiment analysis (TextBlob + VADER).
- Object detection (YOLO-NAS via super-gradients).
- OCR extraction (EasyOCR).
- Basic visual metrics (brightness, sharpness, motion).

---

## 5) Trend Pattern Engine (TPE)

TPE is the system that gives TrendyAI internet-wide situational awareness.

### Role
- Continuously ingest trend signals (YouTube, Google Trends, Reddit, and optionally TikTok/IG sources where legal/available).
- Build topic velocity, momentum, and decay features.
- Serve trend context back to analyzer/recommendation services.

### Separation of concerns
- **Core Analyzer**: analyzes the user’s content.
- **TPE**: analyzes the internet trend landscape.
- **Recommendation Layer**: combines both to suggest actions.

### TPE pipeline
`Trend Crawlers → Trend Preprocessor → Pattern Miner → Topic Vector Store → Trend Predictor → Trend Context API`

---

## 6) What the Repository Already Has (Current State)

The backend prototype is present and runnable with FastAPI.

### Existing API modules
- `POST /video/analyze`
  - saves upload,
  - extracts audio,
  - extracts frames,
  - transcribes,
  - summarizes,
  - writes per-job artifacts/JSON.
- `GET /content/analyze?job_path=...`
  - transcript/summary,
  - keywords/topics/sentiment,
  - object detection,
  - OCR,
  - visual feature stats.
- `GET /channel/{channel_id}`
  - YouTube channel details + uploads retrieval.
- `GET /auth/login` and `GET /auth/oauth2callback`
  - YouTube OAuth integration skeleton.

### Data/artifact structure already visible
- Raw uploads in `data/raw/`.
- Processed job outputs under `data/processed/job_.../`.
- Analysis JSON artifacts in `data/processed/analysis/`.

---

## 7) Gaps to Complete the Product

- Frontend app is not implemented yet (`frontend/package.json` currently empty).
- `scripts/` training/inference/preprocess/evaluate files are placeholders.
- Processing is mostly request-bound; queue/worker job orchestration is still needed.
- Persistent DB models and migrations are not yet implemented.
- Production-grade auth, rate limiting, observability, and retention policies are pending.
- Dependency management needs cleanup (split runtime/inference/dev requirements).

---

## 8) GPU Strategy (Cloud-first, No Local GPU Dependency)

You can run this project without local GPU by renting cloud GPUs for heavy workloads.

### Recommended setup
- API, queue, DB on regular cloud compute.
- GPU workers on on-demand/spot instances.
- Object storage for artifacts and model files.

### Provider options
- RunPod, Lambda, Vast.ai, Modal, Replicate,
- or AWS/GCP/Azure GPU instances (L4/A10/A100 class depending on workload).

### Cost/perf approach
1. Start with one GPU worker pool.
2. Autoscale based on queue depth and job age.
3. Add batching and quantization before increasing model size/cost.
4. Track per-job GPU minutes and model-call cost.

---

## 9) Security, Compliance, and Operations (Target)

- OAuth2 + JWT for user auth and channel linking.
- HTTPS in transit + encryption at rest.
- Signed URLs for private artifact access.
- Configurable retention/deletion windows for user video data.
- Structured logging with PII redaction.
- Monitoring + alerting for API latency, queue lag, worker failure rates, and model errors.

---

## 10) Deployment Direction

- Containerized services (API + workers).
- CI/CD via GitHub Actions.
- Kubernetes or managed container platform for scaling.
- Redis for queueing/caching.
- PostgreSQL for relational persistence.
- S3-compatible object storage for media artifacts.

---

## 11) Project Roadmap

A detailed, phase-by-phase implementation roadmap is maintained in:

- [`plan.md`](./plan.md)

This includes:
- architecture stabilization,
- queue/job lifecycle,
- multimodal analyzer hardening,
- TPE rollout,
- recommendation engine design,
- frontend dashboard delivery,
- MLOps + production readiness.

---

## 12) Quickstart (Prototype Backend)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Open API docs at:
- `http://localhost:8000/docs`

---

## 13) Immediate Engineering Priorities

1. Add async job model (`queued`, `processing`, `completed`, `failed`).
2. Move analysis execution to queue workers.
3. Define stable versioned output schema (`analysis_v1`).
4. Add DB models/migrations and artifact manifest tracking.
5. Build frontend MVP (upload, status, report view).
6. Add CI checks (lint, tests, build) and staging deployment.

---

## 14) Summary

TrendyAI combines a **multimodal content analyzer** and a **global trend intelligence engine** to provide creators with concrete, high-impact recommendations.

- The vision and architecture are now fully documented.
- A meaningful backend prototype already exists.
- The remaining work is primarily productization: orchestration, persistence, frontend, and operational hardening.

