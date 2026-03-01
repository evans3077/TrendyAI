# TrendyAI (AutoInsightAI)

TrendyAI is an AI-powered **creator growth operating system** that helps creators and teams make better videos *before* they publish. It combines multimodal video analysis, channel intelligence, and real-time trend forecasting to deliver concrete actions that improve **CTR, retention, watch time, and conversion**.

> Mission: Give creators measurable business outcomes—not just AI summaries.

---

## 1) Why TrendyAI Will Beat Existing Tools

Most tools in the market do one of three things poorly:
1. show basic analytics after publishing,
2. generate generic advice without evidence,
3. or optimize only one modality (title or thumbnail only).

TrendyAI is designed to be better by default:
- **Pre-publish intelligence**: predict weaknesses before upload.
- **Evidence-linked recommendations**: every suggestion ties to transcript/video/timing/trend signals.
- **Execution-first output**: “what to change, where, why, and expected impact.”
- **Creator ROI focus**: score improvements in expected views/watch time per edit effort.
- **Learning loop**: outcomes from edited videos feed model improvement.

---

## 2) Product Outcomes (Value for Money)

Users should clearly see value from the first week.

### Core promised outcomes
- Faster iteration cycle (idea → edit → publish).
- Better hooks in first 3–15 seconds.
- Better topic-title-thumbnail alignment.
- Higher consistency across uploads.
- Better hit rate on trend-relevant content.

### Value metrics to show customers
- **Predicted retention uplift** from recommended edits.
- **Expected CTR delta** from title/thumbnail suggestions.
- **Trend timing score** (too early, peak, too late).
- **Recommendation adoption rate** and its result over time.
- **Cost-to-impact ratio** per recommendation (time/edit effort vs gain).

---

## 3) End-to-End Product Flow

`Idea/Video Upload → Multimodal Analysis → Trend Context Matching → Recommendation Engine → Edit Checklist → Post-publish Feedback Loop`

### Creator-facing experience
1. Upload video (or connect channel).
2. Receive a ranked set of improvements (hook, pacing, title/metadata, visual clarity, emotional delivery, trend fit).
3. Apply edits with timestamped guidance.
4. Track outcomes against baseline after publish.

---

## 4) Unified Architecture

`Client App → FastAPI API Layer → Queue → CPU/GPU Workers → Storage + DB → Recommendation Service → Dashboard`

| Layer | Technology (target) | Purpose |
|---|---|---|
| Frontend | Next.js web app (mobile-ready API) | Upload, reports, experiments, history |
| API | FastAPI | Auth, contracts, orchestration, status |
| Queue | Redis + Celery/RQ | Async jobs + retries |
| Workers | CPU + cloud GPU pools | Transcription, vision, ranking, inference |
| Storage | S3/MinIO/R2 | Video/audio/frames/artifacts |
| DB | PostgreSQL (+ Redis cache) | Jobs, users, metrics, recommendations |
| Trend Engine | Crawler + feature store + serving API | Trend momentum + context |
| Observability | Prometheus/Grafana + logs + traces | Reliability/cost/performance |

---

## 5) AI/ML Capability Stack

### Multimodal Analyzer
- Speech-to-text and semantic segmentation.
- Long-form summarization and chapter-level extraction.
- Sentiment and delivery-energy profiling.
- Object/OCR scene signal extraction.
- Visual quality and pacing analysis.

### Trend Pattern Engine (TPE)
- Crawls trend sources (YouTube, Google Trends, Reddit; optional additional legal sources).
- Builds trend velocity, momentum, novelty, and decay features.
- Provides trend context APIs by niche, geo, and time horizon.

### Recommendation Engine
- Converts signals into structured actions:
  - problem,
  - evidence,
  - recommended change,
  - expected impact,
  - confidence.
- Prioritizes actions by expected outcome per effort.

---

## 6) Current Repository State (Reality Check)

The backend prototype already includes:
- `POST /video/analyze`: upload, audio extraction, frame extraction, transcription, summarization, artifacts.
- `GET /content/analyze`: transcript/summary, keywords/topics/sentiment, object detection, OCR, visual stats.
- `GET /channel/{channel_id}`: YouTube channel + uploads context.
- `GET /auth/login`, `GET /auth/oauth2callback`: YouTube OAuth skeleton.

Data outputs already exist under:
- `data/raw/`
- `data/processed/job_.../`
- `data/processed/analysis/`

---

## 7) What Must Improve to Become Market-Leading

1. **User-facing product quality**
   - Build polished dashboard and guided edit workflow.
   - Add recommendation explainability and confidence.
2. **System reliability**
   - Move to queue-driven async architecture.
   - Add robust retries, idempotency, and job state lifecycle.
3. **Decision quality**
   - Add rigorous offline/online evaluation for recommendations.
   - Introduce A/B testing framework for recommendation templates.
4. **Business value visibility**
   - Expose ROI dashboards per creator/team.
   - Link recommendation adoption to post-publish outcomes.
5. **Enterprise readiness**
   - Multi-tenant access control, audit logs, data retention policies.

---

## 8) Cloud GPU Strategy (No Local GPU Dependency)

TrendyAI is designed to run with rentable GPUs online.

### Practical setup
- API/DB/queue on general compute.
- GPU inference on autoscaled pools.
- Model/artifact storage in object storage.

### Providers
- RunPod, Lambda, Vast.ai, Modal, Replicate,
- AWS/GCP/Azure GPU instances.

### Cost governance
- Per-job GPU cost telemetry.
- Autoscale by queue lag and SLA targets.
- Use batching + quantization before scaling spend.

---

## 9) Security and Trust

- OAuth2 + JWT authentication.
- Encryption in transit and at rest.
- Signed URLs for private artifacts.
- Configurable content retention/deletion windows.
- PII-aware logging and redaction.
- Compliance-ready architecture path (SOC2-friendly controls).

---

## 10) Competitive Moat Strategy

To become “far better than market,” TrendyAI needs moats beyond raw model quality:
- **Outcome graph**: proprietary mapping of edit-type → performance-lift by niche.
- **Creator memory**: long-term understanding of each channel’s voice and winning patterns.
- **Trend + personalization fusion**: recommendations based on global trends *and* creator identity.
- **Speed moat**: fast turnaround even for long videos.
- **Trust moat**: transparent, evidence-backed recommendations.

---

## 11) Roadmap and Execution Plan

Full implementation instructions and phases are in:
- [`plan.md`](./plan.md)

---

## 12) Quickstart (Current Prototype)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

API docs:
- `http://localhost:8000/docs`

---

## 13) Immediate Priorities

1. Implement async job system (`queued`, `processing`, `completed`, `failed`).
2. Add PostgreSQL models + migrations for jobs/results/recommendations.
3. Introduce stable versioned result schema (`analysis_v1`, `recommendation_v1`).
4. Ship web dashboard MVP (upload, status, report, history).
5. Add eval suite measuring recommendation quality and business impact.
6. Stand up cloud deployment with cost + reliability monitoring.

