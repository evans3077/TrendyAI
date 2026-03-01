# Trendy AI Platform - Engineering Implementation Plan

This plan implements the subsystem blueprint in the README using explicit modules (A–Q) and production pipeline stages.

---

## 1) Design Process (Senior Engineering Workflow)

1. **Define contract first** for each stage (input schema, output schema, failure states).
2. **Build as independent subsystem** with clear interface.
3. **Add deterministic tests** (unit + integration + regression).
4. **Deploy behind queue orchestration** (no heavy work in API request path).
5. **Instrument** latency, error rate, and quality drift metrics.

---

## 2) Target Modules and Delivery Order

### Phase A-B Foundation (existing -> harden)
- **A: Channel Context (`api/channel_context`)**
- **B: Video Analyzer (`api/video_analyzer`)**

### Phase C-E Data Intelligence (new)
- **C: Trend Scraper**
- **D: Metadata Extractor**
- **E: Audience Tracker**

### Phase F-K Model Layer (new package)
- **F: NLP Models**
- **G: Vision Models**
- **H: Audio Models**
- **I: Multimodal Fusion**
- **J: OCR Model Runtime**
- **K: Embedding/Ranking Layer**

### Phase L-P Recommendation Layer (new package)
- **L: Title/Tag Recommender**
- **M: Thumbnail Recommender**
- **N: Publishing Time Optimizer**
- **O: Trend Alignment Recommender**
- **P: Retention Recommender**

### Phase Q Learning Layer (new)
- **Q: Feedback Loop + Retraining Orchestrator**

---

## 3) Core Apps and Pipelines

## 3.1 Runtime Pipeline (online)
1. `POST /jobs` creates job.
2. Preprocess media artifacts.
3. Run module B + F/G/H/J.
4. Run module C for trend context.
5. Run module I/K fusion.
6. Generate recommendations L–P.
7. Save results and notify frontend.

## 3.2 Scheduled Pipeline (offline)
- Trend scraping refresh (C).
- Metadata indexing refresh (D).
- Audience metric sync (E).
- Model training/evaluation cycle (F–K + Q).

## 3.3 Feedback Pipeline
- Collect adopted recommendations.
- Compare predicted vs actual outcomes.
- Feed correction signals into Q retraining jobs.

---

## 4) Required Data Contracts

## Contract 1: `artifact_manifest_v1`
- `job_id`, source URI, audio URI, frame URIs, metadata URI, checksums, timestamps.

## Contract 2: `analysis_v1`
- transcript, summary, keywords/topics, sentiment, visual detections, OCR, timing/hook features, confidences.

## Contract 3: `trend_context_v1`
- trending topics, momentum, novelty, niche/region context, freshness/confidence.

## Contract 4: `recommendation_v1`
- recommendation id, module source (L/M/N/O/P), evidence refs, action text, priority, confidence.

## Contract 5: `feedback_event_v1`
- recommendation id, applied/not applied, publish timestamp, outcome deltas.

---

## 5) Infrastructure Plan

- **API Layer:** FastAPI service.
- **Queue:** Redis + worker runner (Celery/RQ).
- **DB:** PostgreSQL for jobs/results/feedback.
- **Object Store:** S3/MinIO for artifacts.
- **GPU Compute:** Vast.ai worker pool for heavy modules.
- **Monitoring:** centralized logs + metrics dashboard.

---

## 6) 12-Week Delivery Timeline

### Weeks 1-2
- Add `POST /jobs`, async queue, job lifecycle states.
- Harden existing A/B modules and file contracts.

### Weeks 3-4
- Implement C (trend scraper) and D (metadata extractor).
- Add normalized trend store schema.

### Weeks 5-6
- Implement F/G/H/J core model wrappers and inference interfaces.
- Introduce I fusion output contract.

### Weeks 7-8
- Implement L/M/O recommenders first (highest impact).
- Add recommendation ranking pipeline using K embeddings.

### Weeks 9-10
- Implement N/P recommenders and E audience tracker.
- Start Q feedback-loop event collection.

### Weeks 11-12
- Automate retraining with Q.
- Finalize dashboards, observability, and production hardening.

---

## 7) Testing and Validation Strategy

- **Unit tests:** utilities, schema validation, text/audio/vision helpers.
- **Integration tests:** full job flow from ingestion to recommendation.
- **Regression tests:** fixed sample videos to detect drift.
- **Operational tests:** queue backpressure, worker crash recovery, storage failures.

Acceptance gate: no module promoted without contract compliance and integration pass.

---

## 8) Risks and Mitigations

1. **Long inference latency** → chunking, batching, async workers, GPU autoscaling.
2. **Model inconsistency across modules** → contract versioning + fusion normalization.
3. **Trend noise quality** → source weighting + freshness scoring + dedupe.
4. **Feedback sparsity** → explicit frontend UX prompts to capture adoption events.

---

## 9) Immediate Next Tasks (Action List)

1. Implement queue-backed `POST /jobs` and status endpoints.
2. Create contracts package and schema validators.
3. Build module C scaffold (`backend/api/trend_scraper/`).
4. Build module D scaffold (`backend/api/metadata_extractor/`).
5. Split model wrapper package for F–K.
6. Create recommender package skeleton L–P.
7. Define feedback event schema and ingestion endpoint for Q.
