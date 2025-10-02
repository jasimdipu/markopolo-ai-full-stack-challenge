import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")))
from server.rtcrm.services.llm_base import BaseLLM
from server.rtcrm.services.llm_gemini import GeminiClient
from server.rtcrm.services.llm_openai import OpenAIClient
from server.rtcrm.utils.logger import setup_logger

logger = setup_logger(__name__)

def llm_from_env() -> BaseLLM:
    provider = (os.getenv("MODEL_PROVIDER") or "openai").lower()
    if provider == "gemini":
        logger.info("Using Gemini provider")
        return GeminiClient(api_key=os.getenv("GOOGLE_API_KEY"), model=os.getenv("GEMINI_MODEL", "gemini-1.5-flash"))

    logger.info("Using OpenAI provider")
    return OpenAIClient(api_key=os.getenv("OPENAI_API_KEY"), model=os.getenv("OPENAI_MODEL","gpt-4o-mini"))
