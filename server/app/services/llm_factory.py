import os
from .llm_base import BaseLLM
from .llm_gemini import GeminiClient
from .llm_openai import OpenAIClient
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

def llm_from_env() -> BaseLLM:
    provider = (os.getenv("MODEL_PROVIDER") or "openai").lower()
    if provider == "gemini":
        logger.info("Using Gemini provider")
        return GeminiClient(api_key=os.getenv("GOOGLE_API_KEY"), model=os.getenv("GEMINI_MODEL", "gemini-1.5-flash"))

    logger.info("Using OpenAI provider")
    return OpenAIClient(api_key=os.getenv("OPENAI_API_KEY"), model=os.getenv("OPENAI_MODEL","gpt-4o-mini"))
