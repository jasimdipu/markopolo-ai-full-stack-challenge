import google.generativeai as genai
from ..utils.logger import setup_logger
from typing import Iterable

logger = setup_logger(__name__)

class GeminiClient:
    _instance = None

    def __new__(cls, api_key: str | None, model: str = "gemini-2.5-flash"):
        if cls._instance is None:
            if not api_key:
                raise RuntimeError("GOOGLE_API_KEY is not set")
            genai.configure(api_key=api_key)
            cls._instance = super().__new__(cls)
            cls._instance.model = genai.GenerativeModel(
                model,
                generation_config={
                    "response_mime_type": "application/json",
                    "temperature": 0.2,
                },
            )
            logger.info("Gemini initialized (%s, JSON mode)", model)
        return cls._instance

    def stream_json(self, prompt: str) -> Iterable[str]:
        logger.debug("Gemini.stream_json len=%d", len(prompt))
        for chunk in self.model.generate_content(prompt, stream=True):
            piece = getattr(chunk, "text", "")
            if piece:
                yield piece
