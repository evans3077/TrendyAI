# Trendy AI Platform - Project Description

Trendy is an AI-powered platform designed to analyze, optimize, and predict trends in video content. The system integrates automated AI pipelines, multimodal analysis, and intelligent recommendations to maximize content performance insights. It leverages GPU acceleration (e.g., Vast.ai) for heavy AI computations while providing a responsive frontend dashboard for actionable analytics.

---

## Directory & Subsystem Overview

### 1. `backend/`

The backend handles all AI computations, API logic, and data orchestration. It is modular to support scalable AI pipelines.

#### 1.1 `api/`

Contains all endpoint modules. Each module encapsulates a functional unit of the Trendy system:

- **`channel_context/` (Module A)**  
  - **Function:** Retrieves YouTube channel metadata, subscription stats, and historical video data.  
  - **Inputs:** Channel ID, OAuth credentials.  
  - **Process:** Uses YouTube API to fetch channel info; normalizes and stores in persistence layer.  
  - **Outputs:** Channel overview, subscriber growth metrics, recent uploads.  
  - **Automation:** Periodic updates can refresh channel statistics automatically.

- **`video_analyzer/` (Module B)**  
  - **Function:** Analyzes uploaded or scraped videos.  
  - **Inputs:** Video URL or file.  
  - **Process:**  
    - Extracts frames, audio, and metadata.  
    - Feeds artifacts to AI models for frame OCR, object signals, transcript, and summary.  
  - **Outputs:** Video scorecards (visual quality, engagement likelihood, speech clarity).  
  - **Automation:** Runs asynchronously for bulk video analysis (target architecture).

- **`trend_scraper/` (Module C, planned)**  
  - **Function:** Scrapes trending content across platforms.  
  - **Inputs:** Platform endpoints (YouTube, social media), keywords.  
  - **Process:**  
    - Collects trending videos, hashtags, and topics.  
    - Uses NLP modules to classify trends.  
  - **Outputs:** Ranked list of trending topics, emerging tags.  
  - **Automation:** Scheduled scraping every few hours; incremental updates stored in `data/processed`.

- **`metadata_extractor/` (Module D, planned)**  
  - **Function:** Pulls structured metadata from videos.  
  - **Inputs:** Video file or URL.  
  - **Process:**  
    - Extracts captions, titles, tags, descriptions.  
    - Cleans text via preprocessing scripts.  
    - Generates embeddings via NLP models.  
  - **Outputs:** Searchable metadata and semantic vectors.

- **`audience_tracker/` (Module E, planned)**  
  - **Function:** Monitors audience interaction.  
  - **Inputs:** Video analytics (views, likes, comments).  
  - **Process:** Computes engagement metrics, sentiment analysis, retention curves.  
  - **Outputs:** Interactive dashboards on viewer behavior.

- **`ai_models/` (Modules F–K, planned package)**  
  - **Function:** Core intelligence layer for predictions.  
  - **Modules:**  
    - **F:** NLP for title/tag generation, sentiment, topic classification.  
    - **G:** Vision for thumbnail scoring, OCR on frames, content recognition.  
    - **H:** Audio for speech clarity, emotion, pacing analysis.  
    - **I:** Multimodal fusion combining text, video, audio for performance prediction.  
    - **J:** OCR specialization for frame-level text extraction.  
    - **K:** Recommendation embeddings and retrieval signals.  
  - **Automation:** Runs on GPU instances; modules operate in parallel to optimize throughput.

- **`recommenders/` (Modules L–P, planned package)**  
  - **Function:** Provides actionable recommendations.  
  - **Modules:**  
    - **L:** Title and tag suggestions.  
    - **M:** Thumbnail optimization.  
    - **N:** Publishing time & frequency optimization.  
    - **O:** Trend alignment suggestions.  
    - **P:** Viewer retention recommendations.  
  - **Outputs:** Ranked suggestions for creators; integrated into frontend dashboards.

- **`feedback_loop/` (Module Q, planned)**  
  - **Function:** Continuously refines models using incoming data.  
  - **Process:**  
    - Tracks model predictions vs actual performance.  
    - Retrains AI models periodically using `scripts/train_model.py`.  
  - **Automation:** Closed-loop feedback pipeline for adaptive learning.

#### 1.2 `core/`

Handles essential utilities:

- **`database.py`** – Stores raw and processed data (PostgreSQL and/or document storage).  
- **`config.py`** – Loads environment variables, API keys, and runtime configurations.  
- **`logger.py`** – Centralized logging for debugging and audit trails.  
- **`auth.py` / `youtube_auth.py`** – Google/YouTube OAuth and token workflows.  

#### 1.3 `main.py`

FastAPI entrypoint exposing API endpoints to frontend and external services.

---

### 2. `frontend/`

Provides interactive UI for creators and analysts.

- **`components/`** – Reusable visualizations (graphs, trend cards, video score cards).  
- **`pages/`** – Dashboard, upload, authentication, and report views.  
- **`services/`** – API client calls to backend modules.  
- **`assets/`** – Icons, logos, thumbnails, and UI assets.

**Expected User Journey:**  
1. Login via OAuth.  
2. Dashboard shows channel metrics and trend opportunities.  
3. Upload video → automated analysis → AI recommendations.  
4. User adjusts content based on recommendations.  
5. System tracks outcomes and feeds back to AI models.  

---

### 3. `models/` (planned)

AI model storage and organization:

- **`nlp/`** – Title/tag prediction, trend analysis, sentiment scoring.  
- **`vision/`** – Thumbnail evaluation, frame analysis, OCR.  
- **`audio/`** – Voice clarity, emotion, pacing detection.  
- **`fusion/`** – Multimodal combination for engagement prediction.  

**Expected Outputs:** AI-generated insights for each video in near real-time, saved locally and optionally in cloud object storage.

---

### 4. `data/`

Central repository for all video and model data:

- **`raw/`** – Original uploaded videos and source artifacts.  
- **`processed/`** – Cleaned and structured data for AI modules.  
- **`embeddings/` (planned)** – Vectorized representations for semantic search and trend similarity.

**Automation:** New uploads trigger preprocessing automatically.

---

### 5. `scripts/`

Pipeline automation scripts:

- **`preprocess.py`** – Cleans and structures raw video/transcript data.  
- **`train_model.py`** – Trains AI modules with GPU acceleration.  
- **`evaluate.py`** – Validates model quality and performance metrics.  
- **`inference.py`** – Runs inference and recommendation generation.

**Expected Result:** Seamless pipeline from upload → analysis → recommendation → feedback.

---

### 6. `docs/` (planned)

Documentation and references:

- **`architecture_diagrams/`** – Visual module interactions and data flow.  
- **`api_docs/`** – OpenAPI and endpoint references.  
- **`model_docs/`** – Model usage, datasets, hyperparameters, and tuning notes.

---

### 7. Deployment & Operations

- **Development:** local/containerized development environment for frontend/backend coding.  
- **Processing:** Vast.ai GPU instances (or equivalent) for training/inference.  
- **Storage:** Raw/processed artifacts on cloud SSD/object storage; models/embeddings persisted for fast reload.  
- **Automation:** scheduler/cron for scraping, analysis, and retraining workflows.  
- **Scalability:** modular services support horizontal scaling and parallel GPU workers.  
- **Security:** OAuth authentication, isolated GPU workers, encrypted storage for sensitive data.

---

### 8. Key Deliverables

- Automated AI pipelines for video analysis and recommendations.  
- Interactive dashboard for trend, engagement, and performance analytics.  
- Scalable AI modules optimized for GPU execution.  
- Persistent storage for models, embeddings, and processed data.  
- Closed-loop feedback improving recommendations over time.  
- API endpoints for integration with external tools.

---

## Current Implementation Snapshot

Already present in this repository:
- FastAPI backend with `channel_context`, `video_analyzer`, and `content_analyzer` routes.
- YouTube OAuth skeleton.
- Existing artifacts under `data/raw` and `data/processed` from previous runs.

Planned subsystems listed above are the target blueprint and should be implemented incrementally.
