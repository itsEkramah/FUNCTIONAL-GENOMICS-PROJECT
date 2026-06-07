import os
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# ============================================================
# HARDCODED API KEYS (active keys provided directly)
# ============================================================
_HARDCODED_OPENAI_KEY = ""
_HARDCODED_GEMINI_KEY = ""
_HARDCODED_OPENROUTER_KEY = ""

# Construct absolute path to the backend/.env file
config_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(config_dir)
dotenv_path = os.path.join(backend_dir, ".env")

# Load environment variables from the specific .env location
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path, override=False)


def _resolve_openai_key() -> str:
    env_key = os.getenv("OPENAI_API_KEY", "").strip().strip("'\"")
    if env_key and env_key.startswith("sk-") and len(env_key) > 20:
        return env_key
    return _HARDCODED_OPENAI_KEY


def _resolve_gemini_key() -> str:
    env_key = os.getenv("GEMINI_API_KEY", "").strip().strip("'\"")
    if env_key:
        return env_key
    if _HARDCODED_GEMINI_KEY:
        return _HARDCODED_GEMINI_KEY
    return ""


def _resolve_openrouter_key() -> str:
    env_key = os.getenv("OPENROUTER_API_KEY", "").strip().strip("'\"")
    if env_key and len(env_key) > 10:
        return env_key
    return _HARDCODED_OPENROUTER_KEY


class Settings(BaseModel):
    """
    Application settings with hardcoded API keys.
    Fallback chain: OpenAI -> Gemini (multi-model) -> OpenRouter -> Offline
    """
    openai_api_key: str = Field(default_factory=_resolve_openai_key)
    gemini_api_key: str = Field(default_factory=_resolve_gemini_key)
    openrouter_api_key: str = Field(default_factory=_resolve_openrouter_key)
    database_url: str = Field(default_factory=lambda: os.getenv("DATABASE_URL", "sqlite:///pathoscope.db").strip().strip("'\""))
    redis_url: str = Field(default_factory=lambda: os.getenv("REDIS_URL", "").strip().strip("'\""))
    log_level: str = Field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO").strip())
    ncbi_email: str = Field(default_factory=lambda: os.getenv("NCBI_EMAIL", "pathoscope@genomics.ai").strip())

    @property
    def is_openai_available(self) -> bool:
        return bool(self.openai_api_key and self.openai_api_key.startswith("sk-") and len(self.openai_api_key) > 20)

    @property
    def is_gemini_available(self) -> bool:
        return bool(self.gemini_api_key)

    @property
    def is_openrouter_available(self) -> bool:
        return bool(self.openrouter_api_key and len(self.openrouter_api_key) > 10)

# Instantiate global settings object
settings = Settings()
