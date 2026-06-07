import logging
from typing import Dict, Any, Optional, Tuple, List
from backend.openrouter_module.openrouter_client import OpenRouterClient
from backend.openrouter_module import config

logger = logging.getLogger("FallbackManager")

class ModelFallbackManager:
    """
    Manages fallback logic. Iterates through prioritized list of models
    until a successful completion is returned, logging execution statistics.
    """
    def __init__(self, client: Optional[OpenRouterClient] = None, models_list: Optional[List[str]] = None):
        self.client = client or OpenRouterClient()
        self.models = models_list or config.PRIORITY_MODELS

    def generate_completion_with_fallback(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 2000
    ) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Loops through the models in priority order.
        Returns:
            Tuple of (response_content, reasoning_details, successful_model_name)
        """
        logger.info(f"Initiating OpenRouter fallback chain across {len(self.models)} models.")
        
        last_error = None
        for model in self.models:
            logger.info(f"Targeting prioritized model: {model}")
            content, reasoning, err = self.client.request_completion(
                model=model,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            if err:
                logger.warning(f"Model '{model}' failed with code '{err['code']}': {err['message'][:150]}")
                last_error = err
                continue  # Switch immediately to the next model in sequence
            
            if content:
                logger.info(f"SUCCESS: Completed request using model '{model}'.")
                return content, reasoning, model
            else:
                logger.warning(f"Model '{model}' returned empty content with no direct error code.")
                
        logger.critical("All models in the OpenRouter fallback chain failed.")
        return None, None, None
