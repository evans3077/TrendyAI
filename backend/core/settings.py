from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Settings:
    # API Keys
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    #OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    #GOOGLE_TREND_API_KEY = os.getenv("GOOGLE_TREND_API_KEY")

    # Project metadata
    PROJECT_NAME = "Trendy AI Video Optimizer"
    VERSION = "1.0.0"
    DESCRIPTION = "AI-powered system for analyzing and optimizing YouTube content performance."

    # Optional settings (add as needed later)
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./trendy.db")
    DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")

settings = Settings()
