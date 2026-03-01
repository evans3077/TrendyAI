i# Trendy AI Platform - Project Description

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
  - **Process:** Uses YouTube API to fetch channel info; normalizes and stores in `database.py`.  
  - **Outputs:** Channel overview, subscriber growth metrics, recent uploads.  
  - **Automation:** Periodic updates can refresh channel statistics automatically.

- **`video_analyzer/` (Module B)**  
  - **Function:** Analyzes uploaded or scraped videos.  
  - **Inputs:** Video URL or file.  
  - **Process:**  
    - Extracts frames, audio, and metadata.  
    - Feeds to AI models (`models/vision` & `models/audio`) for thumbnail quality, frame OCR, and audio analysis.  
  - **Outputs:** Video scorecards (visual quality, engagement likelihood, speech clarity).  
  - **Automation:** Runs asynchronously for bulk video analysis.

- **`trend_scraper/` (Module C)**  
  - **Function:** Scrapes trending content across platforms.  
  - **Inputs:** Platform endpoints (YouTube, social media), keywords.  
  - **Process:**  
    - Collects trending videos, hashtags, and topics.  
    - Uses NLP modules to classify trends.  
  - **Outputs:** Ranked list of trending topics, emerging tags.  
  - **Automation:** Scheduled scraping every few hours; incremental updates stored in `data/processed`.

- **`metadata_extractor/` (Module D)**  
  - **Function:** Pulls structured metadata from videos.  
  - **Inputs:** Video file or URL.  
  - **Process:**  
    - Extracts captions, titles, tags, descriptions.  
    - Cleans text via preprocessing scripts.  
    - Generates embeddings via NLP models.  
  - **Outputs:** Searchable metadata, semantic embeddings in `data/embeddings`.

- **`audience_tracker/` (Module E)**  
  - **Function:** Monitors audience interaction.  
  - **Inputs:** Video analytics (views, likes, comments).  
  - **Process:** Computes engagement metrics, sentiment analysis, retention curves.  
  - **Outputs:** Interactive dashboards on viewer demographics and behavior.

- **`ai_models/` (Modules F–K)**  
  - **Function:** Core intelligence layer for predictions.  
  - **Modules:**  
    - **F:** NLP for title/tag generation, sentiment, topic classification.  
    - **G:** Vision for thumbnail scoring, OCR on frames, content recognition.  
    - **H:** Audio for speech clarity, emotion, pacing analysis.  
    - **I:** Multimodal fusion combining text, video, audio for performance prediction.  
    - **J:** OCR for analyzing frame content automatically.  
    - **K:** Recommendation embeddings for internal analytics.  
  - **Automation:** Runs on GPU instances; models can operate in parallel to optimize throughput.

- **`recommenders/` (Modules L–P)**  
  - **Function:** Provides actionable recommendations.  
  - **Modules:**  
    - **L:** Title and tag suggestions.  
    - **M:** Thumbnail optimization.  
    - **N:** Publishing time & frequency optimization.  
    - **O:** Trend alignment suggestions.  
    - **P:** Viewer retention recommendations.  
  - **Outputs:** Ranked suggestions for creators; integrated into frontend dashboards.

- **`feedback_loop/` (Module Q)**  
  - **Function:** Continuously refines models using incoming data.  
  - **Process:**  
    - Tracks model predictions vs actual performance.  
    - Retrains AI models periodically using `train_model.py`.  
  - **Automation:** Full closed-loop feedback pipeline for adaptive learning.

#### 1.2 `core/`

Handles essential utilities:

- **`database.py`** – Stores all raw and processed data (MongoDB/PostgreSQL).  
- **`config.py`** – Loads environment variables, API keys, and runtime configurations.  
- **`logger.py`** – Centralized logging for debugging and audit trails.  
- **`auth.py`** – Google/YouTube OAuth, token refresh automation.  

#### 1.3 `main.py`

FastAPI entrypoint exposing all API endpoints to the frontend and external services.

---

### 2. `frontend/`

Provides interactive UI for creators and analysts.

- **`components/`** – Reusable visualizations (graphs, trend cards, video score cards).  
- **`pages/`** –  
  - **Dashboard:** Live metrics and AI-generated recommendations.  
  - **Upload Page:** Upload new videos and track analysis progress.  
  - **Login:** OAuth-based authentication.  
- **`services/`** – Handles API calls to backend modules.  
- **`assets/`** – Icons, logos, thumbnails, and other UI assets.

**Expected User Journey:**  

1. Login via OAuth.  
2. Dashboard shows current channel metrics and trending opportunities.  
3. Upload video → automated analysis → AI-driven recommendations appear.  
4. User adjusts content based on recommendations.  
5. System tracks audience engagement → feeds back to AI models.  

---

### 3. `models/`

AI model storage and organization:

- **`nlp/`** – Title/tag prediction, trend analysis, sentiment scoring.  
- **`vision/`** – Thumbnail evaluation, frame analysis, OCR.  
- **`audio/`** – Voice clarity, emotion, pacing detection.  
- **`fusion/`** – Multimodal combination for engagement prediction.  

**Expected Outputs:** AI-generated insights for each video in near real-time, saved locally and optionally on cloud storage.

---

### 4. `data/`

Central repository for all video and model data:

- **`raw/`** – Original uploaded videos and transcripts.  
- **`processed/`** – Cleaned and structured data ready for AI models.  
- **`embeddings/`** – Vectorized representations for semantic searches, trend similarity, and recommendations.  

**Automation:** New uploads trigger preprocessing automatically.

---

### 5. `scripts/`

Pipeline automation scripts:

- **`preprocess.py`** – Cleans and structures raw video and transcript data.  
- **`train_model.py`** – Trains AI modules; supports GPU acceleration on Vast.ai.  
- **`evaluate.py`** – Validates models’ accuracy, predicts performance metrics.  
- **`inference.py`** – Runs real-time predictions and suggestions.  

**Expected Result:** Seamless AI pipeline from upload → analysis → recommendation → feedback.

---

### 6. `docs/`

Documentation and reference materials:

- **`architecture_diagrams/`** – Visual representation of module interactions and data flow.  
- **`api_docs/`** – Swagger/OpenAPI specifications for backend endpoints.  
- **`model_docs/`** – Notes on model usage, hyperparameters, training datasets, and fine-tuning instructions.

---

### 7. Deployment & Operations

- **Development:** Google Antigravity (or local environment) for UI/backend coding.  
- **Processing:** Vast.ai GPU instances (100–500 GB SSD recommended) for model training and inference.  
- **Storage:** All raw and processed data saved on cloud SSD; embeddings and models stored persistently for fast reload.  
- **Automation:**  
  - Cron or scheduler triggers periodic scraping, analysis, and retraining.  
  - Parallel model execution on GPU to reduce latency.  
  - Feedback loop ensures AI models adapt to live audience data.  
- **Scalability:** Modular architecture allows horizontal scaling (additional GPU nodes for AI-heavy modules).  
- **Security:** OAuth for authentication, SSH/GPU isolation for compute, encrypted storage for sensitive data.

---

### 8. Key Deliverables

- **Automated AI pipelines** for video analysis and recommendation.  
- **Interactive dashboards** with trend, engagement, and performance analytics.  
- **Scalable AI models** optimized for GPU execution.  
- **Persistent storage** for models, embeddings, and processed data.  
- **Closed-loop feedback** improving recommendations over time.  
- **API endpoints** for integration with other platforms or external automation.

---

**Summary:**  
Trendy is a fully automated, AI-driven platform that empowers content creators to optimize video strategy using multimodal analysis. Its modular architecture ensures scalability, GPU acceleration, and parallel processing, making it suitable for real-time insights and adaptive recommendations.
