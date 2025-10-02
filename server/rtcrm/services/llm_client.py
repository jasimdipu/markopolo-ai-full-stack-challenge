import os
from typing import Iterable, Optional

from ..utils.logger import setup_logger
logger = setup_logger(__name__)

# Optional imports (lazy fail with clear logs)
try:
    import google.generativeai as genai
except Exception as e:
    genai = None
    logger.debug(f"google-generativeai import issue: {e}")

try:
    from openai import OpenAI
except Exception as e:
    OpenAI = None  # type: ignore
    logger.debug(f"openai sdk import issue: {e}")


class LLMClient:
    """
    One class, two providers (Gemini/OpenAI), chosen by env:
      MODEL_PROVIDER = "gemini" | "openai"    (default: gemini)
      GEMINI_MODEL   = "gemini-1.5-flash"     (or your choice)
      OPENAI_MODEL   = "gpt-4o-mini"          (or your choice)
    Stream API is unified: stream_json(prompt) -> yields text chunks (JSON).
    """
    _instance: Optional["LLMClient"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_provider()
        return cls._instance

    # ---------- provider init ----------
    def _init_provider(self) -> None:
        provider = (os.getenv("MODEL_PROVIDER") or "gemini").lower()
        self.provider = provider

        if provider == "openai":
            self._init_openai()
        else:
            # default to gemini
            self._init_gemini()

    def _init_gemini(self) -> None:
        api_key = os.getenv("GOOGLE_API_KEY")
        model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY is not set")
        if genai is None:
            raise RuntimeError("google-generativeai package is missing")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name,
            generation_config={
                "response_mime_type": "application/json",  # force JSON
                "temperature": 0.5,
            },
        )
        logger.info(f"LLMClient initialized: provider=gemini model={model_name}")

    def _init_openai(self) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")
        if OpenAI is None:
            raise RuntimeError("openai package is missing")

        # single shared client
        self._oa_client = OpenAI(api_key=api_key)
        self._oa_model = model_name
        logger.info(f"LLMClient initialized: provider=openai model={model_name}")

    # ---------- unified streaming ----------
    def stream_json(self, prompt: str) -> Iterable[str]:
        """
        Yields text chunks that together form a JSON object.
        """
        logger.debug(f"LLM stream start provider={self.provider} len={len(prompt)}")

        if self.provider == "openai":
            # Chat Completions (stream) with JSON mode
            stream = self._oa_client.chat.completions.create(
                model=self._oa_model,
                stream=True,
                response_format={"type": "json_object"},
                temperature=0.2,
                messages=[
                    {"role": "system", "content": "Return ONLY valid JSON (no markdown)."},
                    {"role": "user", "content": prompt},
                ],
            )
            for chunk in stream:
                try:
                    delta = chunk.choices[0].delta
                    piece = getattr(delta, "content", None)
                    if piece:
                        yield piece
                except Exception:
                    continue
        else:
            # Gemini streaming
            for chunk in self.model.generate_content(prompt, stream=True):
                piece = getattr(chunk, "text", "")
                if piece:
                    yield piece
