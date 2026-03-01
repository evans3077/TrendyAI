# TrendyAI Market-Leading Execution Plan

This plan focuses on one outcome: **deliver materially better ROI for creators than competing tools**.

---

## 1) North Star, Positioning, and Success Criteria

## 1.1 North Star
Maximize creator growth outcomes per unit of production effort.

## 1.2 Positioning
TrendyAI is not just analytics and not just AI writing. It is a **decision engine + execution system** for video performance.

## 1.3 Success criteria (what “better than market” means)
- Time-to-actionable-report: < 5 min for standard videos.
- Recommendation adoption rate: > 35%.
- Measured uplift among adopters:
  - +8–15% retention in first 30 seconds,
  - +5–12% CTR improvement,
  - +10% watch-time growth over baseline.
- User retention: weekly active creators with recurring usage > 50%.

---

## 2) Product Strategy: Value for Money

## 2.1 Product tiers
- **Starter**: single creator, core analysis.
- **Pro**: trend intelligence + deeper recommendations + A/B guidance.
- **Team/Agency**: multi-seat, workflow controls, benchmark analytics.

## 2.2 Value framework for each recommendation
Every recommendation should include:
1. what is wrong,
2. where it appears (timestamp/asset),
3. what to change,
4. confidence,
5. expected impact range,
6. effort estimate.

## 2.3 ROI surfaces in product
- “If you apply top 3 edits, expected uplift = X.”
- historical before/after improvements.
- cost-impact leaderboard (highest return edits first).

---

## 3) Current-State Assessment (Repo)

## What exists
- FastAPI backend wiring.
- Video analysis endpoint pipeline.
- Content analysis endpoint pipeline.
- YouTube channel context + OAuth skeleton.
- Artifact outputs in local data folders.

## Key shortcomings
- No production job queue/state machine.
- No robust persistence models/migrations.
- No frontend app.
- No recommendation efficacy evaluation loop.
- Placeholder training/inference scripts.

---

## 4) Target Architecture (Production)

`Web App/API Clients → FastAPI → Redis Queue → CPU/GPU Workers → Postgres + Object Storage → Recommendation API → Analytics`

### Core services
1. **API Service**: auth, contracts, job orchestration.
2. **Ingestion Service**: upload validation, storage, metadata.
3. **Inference Workers**:
   - CPU workers for lightweight analysis,
   - GPU workers for ASR/vision/ranking.
4. **Trend Pattern Engine (TPE)**:
   - crawler jobs,
   - trend feature store,
   - trend context serving.
5. **Recommendation Service**:
   - structured generation,
   - confidence and impact scoring,
   - policy guardrails.
6. **Outcome Measurement Service**:
   - recommendation adoption,
   - post-publish uplift attribution.

---

## 5) Phased Delivery Plan

## Phase 0 — Stabilize Foundations (Week 1)
- Dependency cleanup into layered requirements.
- Config management with `.env.example` + validation.
- Linting/testing baseline.
- Basic API contract tests.

**Exit criteria**
- Clean install + reproducible app startup.
- CI executes lint + tests on every PR.

## Phase 1 — Job Backbone and Reliability (Week 1–2)
- Implement `AnalysisJob` lifecycle and queue worker processing.
- Add retries, idempotency keys, and dead-letter handling.
- Add progress events + status endpoints.

**Exit criteria**
- Upload API is non-blocking.
- Failure recovery works without data corruption.

## Phase 2 — Recommendation Quality Core (Week 2–4)
- Versioned output schemas (`analysis_v1`, `recommendation_v1`).
- Evidence-binding for all recommendations.
- Priority ranking by expected impact/effort.
- Human-readable + machine-readable recommendation formats.

**Exit criteria**
- 100% recommendations contain evidence and confidence.
- Internal reviewers rate > 80% recommendations as actionable.

## Phase 3 — Trend Pattern Engine v1 (Week 4–6)
- Build daily trend crawlers and normalization jobs.
- Add topic momentum/novelty/decay features.
- Integrate trend context scoring into recommendation ranking.

**Exit criteria**
- Every report includes trend-fit section with confidence.

## Phase 4 — Frontend MVP to Product v1 (Week 5–8)
- Dashboard: upload, progress, report, recommendation checklist.
- Edit workflow: assign/track completed suggestions.
- Historical insights: compare uploads and outcomes.

**Exit criteria**
- Users can run full workflow without API docs.

## Phase 5 — Outcome Intelligence (Week 8–10)
- Connect to post-publish metrics.
- Build uplift attribution per adopted recommendation.
- Add creator-specific learning loop (what works for this channel).

**Exit criteria**
- Product can prove measured value to paying users.

## Phase 6 — Scale, Security, and Enterprise Readiness (Week 10–12)
- Multi-tenant controls and RBAC.
- Audit logs and policy controls.
- SLO-based autoscaling and on-call alerts.
- Cost optimization program for GPU workloads.

**Exit criteria**
- Stable production operations with clear SLOs and cost KPIs.

---

## 6) ML and Evaluation Strategy

## 6.1 Evaluation layers
1. **Component quality**: ASR WER, OCR precision, topic relevance.
2. **Recommendation quality**: actionability score, evidence adequacy.
3. **Business impact**: CTR/retention/watch-time uplift.

## 6.2 Offline + online loop
- Offline benchmark datasets for repeatable regressions.
- Online A/B testing of recommendation templates and prioritization.
- Continuous model/prompt tuning from outcome signals.

## 6.3 Guardrails
- Avoid unsupported claims.
- Confidence-calibrated outputs.
- Fallback recommendations when evidence is weak.

---

## 7) Cloud GPU, Cost, and Performance Plan

## 7.1 Infrastructure principle
No hard dependency on local GPUs; use rentable cloud GPU pools.

## 7.2 Initial setup
- Start with L4/A10 class GPU pool for inference.
- Route CPU-compatible jobs away from GPU.
- Autoscale workers by queue length + response SLA.

## 7.3 Cost optimization order
1. Workload routing (CPU vs GPU).
2. Batching and async pipelines.
3. Quantization/distillation.
4. Caching repeated computations.
5. Provider optimization (spot/preemptible where safe).

---

## 8) Go-to-Market Product Features That Increase Perceived Value

1. **Action checklist mode**: one-click “apply this first.”
2. **What changed?** diff view between video versions.
3. **Niche benchmark panels** vs competitor channels.
4. **Trend timing alerts** (“publish now”, “wait”, “pivot angle”).
5. **Agency workspace** for multi-client operations.
6. **Weekly growth reports** auto-generated from outcomes.

---

## 9) Execution Governance

## 9.1 Weekly operating cadence
- Mon: roadmap + model quality review.
- Wed: reliability/performance/cost review.
- Fri: user outcome and adoption review.

## 9.2 Decision dashboard
Track these every week:
- report latency,
- recommendation adoption,
- measured uplift,
- GPU cost per report,
- system failure rate,
- user retention.

## 9.3 Stop-doing rules
- Do not ship features without measurable outcome hypothesis.
- Do not increase model cost unless uplift justifies it.
- Do not release recommendations without evidence linkage.

---

## 10) Next Sprint (Immediate Action Items)

1. Implement async queue + `AnalysisJob` lifecycle.
2. Add DB schema + migrations for users/jobs/results/recommendations.
3. Refactor pipeline into composable steps with explicit contracts.
4. Implement recommendation schema with evidence/impact/effort fields.
5. Build dashboard MVP (upload, status, report, checklist).
6. Add baseline evaluation suite and weekly scorecard.

