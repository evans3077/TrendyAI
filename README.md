# TrendyAI / AutoInsightAI

Technical design document for building a production-grade multimodal video analysis system.

This README is intentionally engineering-first and follows your original architecture direction: **core analyzer + trend engine + recommendation engine**, with clear subsystem boundaries and pipeline contracts.

---

## 1. System Goal

Build an AI platform that ingests creator videos and channel context, runs multimodal analysis (audio/video/text/metadata), fuses results with trend intelligence, and outputs structured recommendations.

Core flow:

`Upload → Preprocess → Multimodal Feature Extraction → Trend Correlation → Recommendation Generation → Report API`

---

## 2. Core Applications (Top-Level Services)

The system should be split into explicit applications/services, each with a single responsibility.

## 2.1 API Gateway App
**Purpose**
- Public entrypoint for clients.
- Handles auth, request validation, rate limiting, job creation, status retrieval.

**Owns**
- REST/WebSocket contracts.
- Job orchestration API only (not heavy inference).

**Key endpoints (target)**
- `POST /jobs` (create analysis job)
- `GET /jobs/{job_id}` (status)
- `GET /jobs/{job_id}/result` (full analysis)
- `GET /jobs/{job_id}/recommendations`

---

## 2.2 Ingestion & Preprocessing App
**Purpose**
- Normalize uploaded media and build deterministic artifacts.

**Pipeline responsibilities**
1. Validate media format + duration constraints.
2. Store original asset in object storage.
3. Extract audio (`16kHz WAV`).
4. Extract key frames / scene samples.
5. Extract video metadata (duration/fps/resolution).
6. Emit standardized artifact manifest.

**Outputs**
- `artifact_manifest.json`
- `audio.wav`
- `frames/*`
- `metadata.json`

---

## 2.3 Core Multimodal Analyzer App
**Purpose**
Run model inference over text/audio/visual streams.

**Subsystems**
- **ASR subsystem**: transcript + timestamps.
- **NLP subsystem**: summary, keywords, topic clusters, sentiment/emotion.
- **Vision subsystem**: object detection, OCR text, visual quality stats.
- **Temporal subsystem**: hook-phase analysis (0–15s), pacing/motion changes.

**Output contract**
`analysis_v1.json`
- transcript, summary, topics, keywords
- sentiment/emotion profile
- visual detections + OCR
- temporal/hook features
- confidence scores per module

---

## 2.4 Trend Pattern Engine (TPE) App
**Purpose**
Continuously build a machine-readable global trend index.

**Important**
TPE does **not** analyze a user video directly; it provides context to the analyzer/recommender.

**Subsystems**
1. **Crawlers**
   - YouTube trends, Google Trends, Reddit (extendable).
2. **Normalizer**
   - Unify schema across sources.
3. **Pattern Miner**
   - Topic velocity, growth rate, decay, novelty.
4. **Trend Store**
   - Vector + relational features for retrieval.
5. **Trend Context API**
   - Query by niche/category/region/time window.

**Output contract**
`trend_context_v1`
- top active topics
- rising/falling signals
- semantic similarity features
- trend confidence + freshness timestamp

---

## 2.5 Recommendation Engine App
**Purpose**
Transform analysis + trend context into structured improvement actions.

**Input**
- `analysis_v1`
- `trend_context_v1`
- optional channel history signals

**Output contract**
`recommendation_v1.json`
Each recommendation must include:
- `problem`
- `evidence` (timestamps/features)
- `action`
- `expected_effect`
- `priority`
- `confidence`

---

## 2.6 Outcome & Feedback App
**Purpose**
Close the loop between recommendations and real-world post-publish outcomes.

**Responsibilities**
- Collect adoption signals (which recommendation was applied).
- Pull post-publish metrics.
- Attribute uplift to recommendation categories.
- Feed periodic retraining/prompt tuning.

---

## 3. Shared Platform Subsystems

## 3.1 Job Orchestration
- Queue-based workflow (Redis + worker framework).
- Job states: `queued`, `preprocessing`, `analyzing`, `trend_enrichment`, `recommending`, `completed`, `failed`.
- Retry policy and dead-letter queues.

## 3.2 Storage Subsystem
- Object storage for artifacts.
- PostgreSQL for job metadata/results.
- Redis for queue/cache.

## 3.3 Model Serving Subsystem
- Versioned model registry metadata.
- CPU/GPU worker routing.
- Warm pools for large models.

## 3.4 Observability Subsystem
- Structured logs with correlation IDs.
- Metrics: job latency, queue lag, model runtime, failure reason distribution.
- Tracing for stage-level debugging.

## 3.5 Security Subsystem
- OAuth2/JWT auth.
- Signed object URLs.
- Secrets via environment/manager.
- Data retention controls.

---

## 4. End-to-End Pipeline Design

## 4.1 Runtime inference pipeline
1. Client creates job (`POST /jobs`).
2. Ingestion service stores media + builds artifacts.
3. Analyzer service computes multimodal features.
4. TPE service returns trend context.
5. Recommender generates structured output.
6. Result persisted and exposed via API.

## 4.2 Offline training pipeline
1. Data ingestion from curated datasets + anonymized internal outcomes.
2. Feature generation and labeling.
3. Model training/fine-tuning.
4. Evaluation gates.
5. Registry publish + staged rollout.

## 4.3 Continuous improvement pipeline
- Weekly retraining windows.
- Prompt/recommender template updates via A/B results.
- Regression checks before release.

---

## 5. Existing Repository Mapping (Current Code)

Already present in repo:
- FastAPI app wiring in `backend/main.py`.
- Video analyzer endpoint and pipeline under `backend/api/video_analyzer/`.
- Content analyzer module under `backend/api/content_analyzer/`.
- Channel context API in `backend/api/channel_context/`.
- YouTube OAuth skeleton in `backend/core/youtube_auth.py`.

Data artifacts already generated under:
- `data/raw/`
- `data/processed/job_.../`
- `data/processed/analysis/`

---

## 6. Gaps to Implement Next

1. Convert request-bound processing to queue-driven job execution.
2. Introduce stable contracts: `artifact_manifest_v1`, `analysis_v1`, `trend_context_v1`, `recommendation_v1`.
3. Add database schema + migrations for jobs and results.
4. Build dedicated TPE service and API.
5. Add recommendation engine with strict evidence binding.
6. Add test suites for each pipeline stage (unit + integration + smoke).

---

## 7. Cloud GPU Strategy

No local GPU dependency is required.

Recommended runtime split:
- CPU workers: preprocessing, OCR-lite, basic NLP.
- GPU workers: ASR, heavy vision, embedding/ranking models.

Use cloud providers (RunPod/Lambda/Vast/Modal/AWS/GCP/Azure) with autoscaling by queue depth and stage SLA.

---

## 8. Implementation Reference

Detailed phased implementation instructions are in:
- [`plan.md`](./plan.md)

---

## 9. Quickstart (Current Prototype)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

API docs:
- `http://localhost:8000/docs`
