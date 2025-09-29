from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
import json
from ..services.llm_client import LLMClient
from ..services.plan_generator import PlanGenerator
from ..utils.logger import setup_logger
import os

router = APIRouter()
logger = setup_logger(__name__)

llm_client = LLMClient(api_key="AIzaSyD0U_t1MreZb_Iwgl2uZUQw8cg8P-yoTQE")
plan_gen = PlanGenerator(llm_client)


@router.post("/plan")
async def plan_endpoint(req: Request):
    goal = (await req.json()).get("goal", "")

    def gen():
        for frame in plan_gen.stream_plan(goal):
            yield "data: " + json.dumps(frame) + "\n\n"

    return StreamingResponse(gen(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "Connection": "keep-alive"})
