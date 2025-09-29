from .llm_client import LLMClient
from ..utils.json_stream import yield_json_objects
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class PlanGenerator:
    def __init__(self, llm: LLMClient):
        self.llm = llm
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
        logger.info(f"Starting plan generation for goal: {goal}")

        # Example system prompt — refine later
        prompt = f"""
        {self.ANSWER_SYSTEM_PROMPT}\n
        Goal: {goal}\n
        Output JSON frames in steps: reasoning, audience, channel_mix, messages, schedule, final.
        """
        stream = self.llm.stream(prompt)

        try:
            for chunk in stream:
                parts = getattr(chunk.candidates[0].content, "parts", [])
                txt = "".join(getattr(p, "text", "") for p in parts)
                for obj in yield_json_objects(txt):
                    # keep only the keys we show on the UI
                    answers = obj.get("answers") or []
                    schedule = obj.get("schedule") or []
                    frame = {"step": "answers", "payload": {"answers": answers, "schedule": schedule}}
                    logger.debug(f"answers frame: {frame}")
                    yield frame
        except Exception as e:
            logger.error(f"Error during plan generation: {e}")
            yield f'{{"error": "{str(e)}"}}'
