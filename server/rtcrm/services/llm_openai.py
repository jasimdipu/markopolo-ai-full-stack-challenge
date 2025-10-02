import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")))
from typing import Iterable
from openai import OpenAI
from server.rtcrm.utils.logger import (setup_logger)

logger = setup_logger(__name__)

SYSTEM_JSON_GUARD = (
    "Return ONLY valid JSON (no markdown, no prose). "
    "If unsure, return an empty JSON object {}."
)

class OpenAIClient:
    _client = None

    def __init__(self, api_key: str | None, model: str = "gpt-4o-mini"):
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")
        if OpenAIClient._client is None:
            OpenAIClient._client = OpenAI(api_key=api_key)
        self.client = OpenAIClient._client
        self.model = model
        logger.info("OpenAI initialized (%s)", model)

    def stream_json(self, prompt: str) -> Iterable[str]:
        """
        Streams JSON text chunks from Chat Completions.
        We request JSON mode; if model ignores it, we still parse via our extractor.
        """
        logger.debug("OpenAI.stream_json len=%d", len(prompt))
        # response_format is supported by modern models; harmless if ignored.
        stream = self.client.chat.completions.create(
            model=self.model,
            stream=True,
            response_format={"type": "json_object"},
            temperature=0.5,
            messages=[
                {"role": "system", "content": SYSTEM_JSON_GUARD},
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
