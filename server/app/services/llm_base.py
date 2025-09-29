from typing import Iterable, Protocol

class BaseLLM(Protocol):
    def stream_json(self, prompt: str) -> Iterable[str]:
        ...
