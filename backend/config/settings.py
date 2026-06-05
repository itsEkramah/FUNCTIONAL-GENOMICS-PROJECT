import os
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Construct absolute path to the backend/.env file
config_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(config_dir)
dotenv_path = os.path.join(backend_dir, ".env")

# Load environment variables from the specific .env location
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)

class Settings(BaseModel):
    """
    Application settings loaded from environment variables or .env file.
    API keys and secrets are never hardcoded.
    """
    openai_api_key: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY", "").strip().strip("'\""))
    gemini_api_key: str = Field(default_factory=lambda: os.getenv("GEMINI_API_KEY", "").strip().strip("'\""))
    database_url: str = Field(default_factory=lambda: os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/pathoscope_ai").strip().strip("'\""))
    redis_url: str = Field(default_factory=lambda: os.getenv("REDIS_URL", "redis://localhost:6379/0").strip().strip("'\""))
    log_level: str = Field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO").strip())

    @property
    def is_openai_available(self) -> bool:
        return len(self.openai_api_key) > 0

    @property
    def is_gemini_available(self) -> bool:
        return len(self.gemini_api_key) > 0

# Instantiate global settings object
settings = Settings()
