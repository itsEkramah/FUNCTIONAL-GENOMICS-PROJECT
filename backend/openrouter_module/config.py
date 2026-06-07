import os
from typing import List

# OpenRouter configuration options
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Priority ordered list of fallback models
PRIORITY_MODELS = [
    "deepseek/deepseek-r1-0528",
    "deepseek/deepseek-v3.2",
    "nvidia/nemotron-3-super-120b-a12b:free",
    "openrouter/free"
]

# HTTP Settings
DEFAULT_TIMEOUT = 45 # seconds
DEFAULT_RETRIES = 3
INITIAL_BACKOFF = 2.0 # seconds
MAX_BACKOFF = 16.0 # seconds
