import os
import google.generativeai as genai
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class LLMClient:
    _instance = None

    def __new__(cls, api_key: str | None):
        if cls._instance is None:
            if not api_key:
                raise RuntimeError("GOOGLE_API_KEY is not set")
            genai.configure(api_key=api_key)
            cls._instance = super().__new__(cls)
            cls._instance.model = genai.GenerativeModel(
                "gemini-1.5-flash",
                generation_config={
                    "response_mime_type": "application/json",  # force JSON
                    "temperature": 0.2,
                },
            )
            logger.info("LLMClient initialized (gemini-1.5-flash, JSON mode)")
        return cls._instance

    def stream_json(self, prompt: str):
        logger.debug("LLM.stream_json start (len=%d)", len(prompt))
        # returns a streaming iterator; each chunk can have .text
        return self.model.generate_content(prompt, stream=True)
