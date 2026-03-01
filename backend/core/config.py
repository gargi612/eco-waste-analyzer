import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Waste Analyzer API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Supabase config
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "https://your-project-url.supabase.co")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "your-supabase-anon-key")
    
    # ML Model Config
    MODEL_WEIGHTS_PATH: str = os.getenv("MODEL_WEIGHTS_PATH", "../ml-model/weights/best_model.pth")
    MODEL_CLASSES_PATH: str = os.getenv("MODEL_CLASSES_PATH", "../ml-model/weights/classes.pt")

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
