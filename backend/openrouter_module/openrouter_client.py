import time
import logging
import requests
from typing import Dict, Any, Optional, Tuple
from backend.openrouter_module import config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OpenRouterClient")

class OpenRouterClient:
    """
    Object-oriented client for the OpenRouter Chat Completions API.
    Handles communication, error state detection, timeouts, and retries.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or config.OPENROUTER_API_KEY
        self.base_url = config.OPENROUTER_BASE_URL
        
    def check_key_validity(self) -> bool:
        return bool(self.api_key and len(self.api_key) > 10)

    def request_completion(
        self,
        model: str,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 2000
    ) -> Tuple[Optional[str], Optional[str], Optional[Dict[str, Any]]]:
        """
        Executes a completions request to OpenRouter.
        Returns:
            Tuple of (response_text, reasoning_text, error_info_dict)
        """
        if not self.check_key_validity():
            return None, None, {"code": "missing_api_key", "message": "No OpenRouter API key provided."}

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://pathoscope-genomics.ai",
            "X-Title": "PathoScope AI Platform"
        }

        # Build payload
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        # Enable reasoning if model supports thinking tokens
        if "deepseek-r1" in model or "deepseek-v3" in model or "nemotron" in model or "free" in model:
            payload["reasoning"] = {"enabled": True}

        url = f"{self.base_url}/chat/completions"
        backoff = config.INITIAL_BACKOFF
        
        for attempt in range(config.DEFAULT_RETRIES):
            try:
                logger.info(f"OpenRouter attempt {attempt + 1} for model: {model}")
                response = requests.post(url, headers=headers, json=payload, timeout=config.DEFAULT_TIMEOUT)
                
                # Check for HTTP errors
                if response.status_code == 429:
                    logger.warning("Rate limit hit (429). Backing off.")
                    time.sleep(backoff)
                    backoff = min(backoff * 2, config.MAX_BACKOFF)
                    continue
                elif response.status_code == 402:
                    logger.error("Quota exhausted/insufficient credits (402). Skipping model.")
                    return None, None, {"code": "quota_exhausted", "message": response.text}
                elif response.status_code == 400:
                    logger.error(f"Bad request (400) for model {model}. Details: {response.text}")
                    return None, None, {"code": "bad_request", "message": response.text}
                elif response.status_code >= 500:
                    logger.warning(f"Server error ({response.status_code}) on OpenRouter side. Backing off.")
                    time.sleep(backoff)
                    backoff = min(backoff * 2, config.MAX_BACKOFF)
                    continue
                
                response.raise_for_status()
                data = response.json()
                
                # Detect error nested inside 200 OK
                if "error" in data:
                    err_msg = data["error"].get("message", "Unknown OpenRouter error.")
                    err_code = data["error"].get("code", 500)
                    logger.warning(f"OpenRouter internal API error (code: {err_code}): {err_msg}")
                    return None, None, {"code": str(err_code), "message": err_msg}

                # Extract response text
                choice = data.get("choices", [{}])[0]
                message = choice.get("message", {})
                content = message.get("content")
                
                # Extract reasoning
                reasoning = message.get("reasoning") or ""
                reasoning_details = message.get("reasoning_details")
                if reasoning_details and isinstance(reasoning_details, list):
                    reasoning_list = []
                    for rd in reasoning_details:
                        if isinstance(rd, dict) and rd.get("text"):
                            reasoning_list.append(rd["text"])
                    if reasoning_list:
                        reasoning = "\n".join(reasoning_list)
                
                if content:
                    logger.info(f"OpenRouter request successful using model {model}.")
                    return content, reasoning, None
                else:
                    logger.warning("Empty response content received.")
                    
            except requests.exceptions.Timeout as t_err:
                logger.warning(f"Timeout occurred: {str(t_err)}")
                time.sleep(backoff)
                backoff = min(backoff * 2, config.MAX_BACKOFF)
            except requests.exceptions.ConnectionError as c_err:
                logger.error(f"Connection failed: {str(c_err)}")
                time.sleep(backoff)
                backoff = min(backoff * 2, config.MAX_BACKOFF)
            except Exception as ex:
                logger.error(f"Unexpected error during API call: {str(ex)}")
                return None, None, {"code": "unexpected_error", "message": str(ex)}

        return None, None, {"code": "all_retries_failed", "message": "Failed after max retries."}
