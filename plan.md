# TrendyAI Engineering Plan

A subsystem-first implementation plan aligned with the original AutoInsightAI design.

---

## 1. Engineering Design Process (How We Build)

Use this design process for every major feature/model update.

## Step 1 — Problem Definition
- Define exactly which pipeline stage is being improved.
- Define required input/output schema updates.
- Define success metrics and failure modes.

## Step 2 — System Contract Design
- Write or update data contracts first:
  - `artifact_manifest_v1`
  - `analysis_v1`
  - `trend_context_v1`
  - `recommendation_v1`
- Add backward compatibility/version policy.

## Step 3 — Subsystem Implementation
- Implement behind clear interfaces.
- Keep model logic isolated from API logic.
- Ensure each stage is independently testable.

## Step 4 — Evaluation & Validation
- Unit tests for deterministic utilities.
- Integration tests for stage-to-stage contract compatibility.
- Golden sample regression tests for inference outputs.

## Step 5 — Release & Observability
- Stage rollout with metrics dashboards.
- Monitor latency, error rates, and output-quality drift.

---

## 2. Target System Blueprint

## 2.1 Core Apps
1. API Gateway
2. Ingestion & Preprocessing
3. Core Multimodal Analyzer
4. Trend Pattern Engine (TPE)
5. Recommendation Engine
6. Outcome & Feedback Service

## 2.2 Shared Subsystems
- Job queue/orchestrator
- Object storage + DB
- Model serving/runtime router
- Monitoring/tracing/logging
- Auth/security controls

---

## 3. Pipeline Contracts (Must-Have)

## 3.1 artifact_manifest_v1
Contains deterministic pointers to all artifacts produced by preprocessing.

Required fields:
- job_id
- source_video_uri
- audio_uri
- frame_uris
- metadata_uri
- checksums
- created_at

## 3.2 analysis_v1
Contains model outputs from audio/text/visual/temporal analyzers.

Required sections:
- transcript + timestamps
- summary
- keywords/topics
- sentiment/emotion
- visual detections + OCR
- hook/pacing features
- module-level confidence

## 3.3 trend_context_v1
Contains trend features used during recommendation.

Required sections:
- trending_topics
- momentum_scores
- novelty_index
- niche_context
- freshness/confidence

## 3.4 recommendation_v1
Contains actionable outputs.

Required sections:
- recommendation_id
- problem
- evidence_refs
- action
- expected_effect
- priority
- confidence

---

## 4. Detailed Subsystem Plan

## 4.1 API Gateway
- Add job-centric APIs.
- Add idempotency keys and request validation.
- Add WebSocket/SSE for progress updates.

## 4.2 Ingestion/Preprocessing
- Standardize FFmpeg/media pipeline.
- Deterministic frame sampling policy.
- Artifact manifest generation + checksum validation.

## 4.3 Core Analyzer
- ASR chunking for long content.
- Long-text summarization strategy.
- NLP features (topics/keywords/sentiment).
- Vision features (objects/OCR/visual quality).
- Temporal features (hook window).

## 4.4 TPE
- Build daily crawlers and normalizer.
- Implement topic vectorization and momentum scoring.
- Serve trend context by niche/region/time.

## 4.5 Recommendation Engine
- Build rules + model hybrid recommendation stack.
- Strict evidence binding and confidence calibration.
- Priority ranking by expected impact.

## 4.6 Outcome Service
- Track recommendation adoption.
- Correlate adopted actions with post-publish metrics.
- Produce training signals for future tuning.

---

## 5. Phase-by-Phase Delivery

## Phase 0 — Repository & Runtime Stabilization (Week 1)
- Dependency segmentation (`base/inference/dev`).
- Centralized config validation.
- Baseline CI (lint + tests).

**Exit criteria**
- Fresh setup works reliably.
- CI gates active.

## Phase 1 — Job Orchestrator & Contracts (Week 1–2)
- Queue integration and state machine.
- Implement `artifact_manifest_v1`.
- Add job/result DB models.

**Exit criteria**
- Async processing works with retries.

## Phase 2 — Analyzer Hardening (Week 2–4)
- Refactor analyzer into independent stage modules.
- Implement `analysis_v1` with confidence fields.
- Add integration tests with golden samples.

**Exit criteria**
- Stable deterministic outputs across test media set.

## Phase 3 — TPE Buildout (Week 4–6)
- Crawler jobs + normalization.
- Trend scoring and context API.
- Implement `trend_context_v1`.

**Exit criteria**
- Analyzer can request and consume trend context per job.

## Phase 4 — Recommendation Engine (Week 6–8)
- Implement recommendation generation contract.
- Implement `recommendation_v1`.
- Add policy checks for unsupported recommendations.

**Exit criteria**
- All recommendations are evidence-backed and structured.

## Phase 5 — Feedback Loop + Evaluation (Week 8–10)
- Build adoption/outcome instrumentation.
- Add periodic evaluation reports.
- Create retraining/prompt tuning hooks.

**Exit criteria**
- Closed-loop learning operational.

## Phase 6 — Production Operations (Week 10–12)
- Autoscaling and capacity policies.
- SLO dashboard + alerts.
- Security hardening and retention automation.

**Exit criteria**
- Production-ready reliability and operational visibility.

---

## 6. Testing Strategy (Engineering)

## 6.1 Unit Tests
- Media utilities
- Schema validators
- Text/feature utility functions

## 6.2 Integration Tests
- End-to-end from job creation to result retrieval.
- Contract validation between each stage output/input.

## 6.3 Regression Tests
- Golden media dataset.
- Compare output drift by schema + key score deltas.

## 6.4 Operational Tests
- Queue backpressure behavior.
- Worker crash/retry recovery.
- Storage failure fallback behavior.

---

## 7. MLOps and Model Lifecycle

- Model version metadata in DB.
- Promotion flow: dev -> staging -> prod.
- Shadow runs for new models before full rollout.
- Drift monitoring on transcription/topic/recommendation quality.

---

## 8. Infrastructure Plan

## 8.1 Compute Split
- CPU nodes: preprocessing and lightweight analysis.
- GPU nodes: heavy ASR/vision/embedding inference.

## 8.2 Cloud Runtime
- Run in containerized services.
- Queue-driven autoscaling.
- Object storage for artifacts.

## 8.3 Cost Controls
- Stage-level timing and resource metrics.
- Route jobs to minimum required compute tier.
- Batch compatible inference workloads.

---

## 9. Immediate Engineering Tasks

1. Implement `POST /jobs` + async queue processing.
2. Add DB schema and migrations for jobs/artifacts/results.
3. Build and enforce schema validation for v1 contracts.
4. Refactor current analyzer code into stage modules.
5. Implement first TPE crawler + trend context endpoint.
6. Implement first structured recommendation engine.
7. Add integration tests across full pipeline.

