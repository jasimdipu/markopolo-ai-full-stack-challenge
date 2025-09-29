from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
import json, asyncio, time
from ..services.llm_client import LLMClient
from ..services.plan_generator import PlanGenerator
from ..utils.logger import setup_logger
import os

router = APIRouter()
logger = setup_logger(__name__)


def get_planner() -> PlanGenerator:
    return PlanGenerator(LLMClient())


@router.post("/plan")
async def plan_endpoint(request: Request):
    body = await request.json()
    goal = (body.get("goal") or "").strip()
    logger.info("/plan goal=%s", goal)

    async def gen():
        last = time.time()
        try:
            for frame in get_planner().stream_plan(goal):
                # yield BYTES, SSE frame with double newline
                data = ("data: " + json.dumps(frame, separators=(",", ":")) + "\n\n").encode("utf-8")
                yield data
                last = time.time()
                await asyncio.sleep(0)  # let loop breathe
        finally:
            # graceful tail event so clients (and curl) know we're done
            yield b"event: done\ndata: {}\n\n"

    return StreamingResponse(
        gen(),
        status_code=200,
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            # Do NOT set "Connection: keep-alive" — let server manage it
        },
    )
