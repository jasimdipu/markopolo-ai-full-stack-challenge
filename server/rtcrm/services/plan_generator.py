from .llm_client import LLMClient
from ..utils.json_stream import yield_json_objects
from ..utils.logger import setup_logger
from ..services.llm_factory import llm_from_env

logger = setup_logger(__name__)


class PlanGenerator:
    def __init__(self, llm: LLMClient):
        self.llm = llm or LLMClient()
        self.ANSWER_SYSTEM_PROMPT = """
                                    You are a campaign planner. Output ONLY JSON, no prose, matching:
                                        {
                                          "answers": [
                                            {"channel": "email|sms|whatsapp|ads", "message": "string", "cta":"string?"}
                                          ],
                                          "schedule": [{"segment":"string","window":"HH:MM-HH:MM"}]
                                        }
                                    """

    def stream_plan(self, goal: str):
        # ... (your prompt prep)
        stream = self.llm.stream_json(self.ANSWER_SYSTEM_PROMPT)
        buf = ""
        for piece in stream:
            buf += piece
            # parse JSON objects from buf (your existing yield_json_objects)
            for obj in yield_json_objects(buf):
                answers = obj.get("answers") or []
                schedule = obj.get("schedule") or []
                yield {"step": "answers", "payload": {"answers": answers, "schedule": schedule}}
