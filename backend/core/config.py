from dotenv import load_dotenv
import os

# Load from .env file
load_dotenv()

class Settings:
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    #OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

settings = Settings()
