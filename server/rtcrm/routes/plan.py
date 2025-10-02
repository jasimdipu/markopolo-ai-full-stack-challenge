# server/rtcrm/routes/plan.py
import os, json, asyncio, time, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")))
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import StreamingResponse
from starlette import status
from starlette.requests import ClientDisconnect
from sqlalchemy.orm import Session as DBSession

from server.rtcrm.utils.logger import setup_logger
from server.rtcrm.database.db import get_db
from server.rtcrm.database.repos import create_session, log_query, save_plan
from server.rtcrm.services.llm_client import LLMClient
from server.rtcrm.services.plan_generator import PlanGenerator

router = APIRouter()
logger = setup_logger(__name__)

_llm = None
_planner = None
def get_planner() -> PlanGenerator:
    global _llm, _planner
    if _llm is None:
        _llm = LLMClient()
    if _planner is None:
        _planner = PlanGenerator(_llm)
    return _planner

@router.post("/plan")
async def plan_endpoint(request: Request, db: DBSession = Depends(get_db)):
    # ---- safe defaults so exception logging never breaks ----
    goal = ""
    ext_user = ""
    q_id = None

    # ---- parse body robustly (tolerate empty/aborted clients) ----
    try:
        try:
            body = await request.json()
        except ClientDisconnect:
            logger.warning("Client disconnected before sending body")
            body = {}
        except Exception:
            raw = await request.body()
            try:
                body = json.loads(raw.decode("utf-8")) if raw else {}
            except Exception:
                body = {}
        goal = (body.get("goal") or "").strip()
        ext_user = (body.get("ext_user") or body.get("user_id") or "").strip()
    except Exception as e:
        logger.exception("Failed to parse request body: %s", e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request body")

    if not goal:
        # Don’t try to stream with no goal; return 400 so FE can retry
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing 'goal'")

    logger.info("/plan goal=%s ext_user=%s", goal, ext_user)

    # ---- create session + query; capture primary key BEFORE commit ----
    try:
        sess = create_session(db, ext_user)
        q = log_query(db, sess.id, goal)
        db.flush()                       # PK gets assigned
        q_id = getattr(q, "id", None)    # capture while bound
        if q_id is None:
            raise RuntimeError("query id missing after flush")
        db.commit()
    except Exception as e:
        logger.exception("DB init error (session/query): %s", e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable")

    async def gen():
        accumulated = {"answers": [], "schedule": []}
        last = time.time()
        try:
            for frame in get_planner().stream_plan(goal):
                if frame.get("step") == "answers":
                    payload = frame.get("payload") or {}
                    # stream payload only
                    yield ("data: " + json.dumps(payload, separators=(",", ":")) + "\n\n").encode("utf-8")
                    last = time.time()
                    # accumulate for persistence
                    if payload.get("answers"):  accumulated["answers"]  = payload["answers"]
                    if payload.get("schedule"): accumulated["schedule"] = payload["schedule"]
                await asyncio.sleep(0)
            # persist final using q_id (not q.id)
            try:
                provider = os.getenv("MODEL_PROVIDER", "gemini")
                save_plan(db, q_id, accumulated, provider)
                db.commit()
            except Exception as e:
                logger.exception("DB save_plan error: %s", e)
            yield b"event: done\ndata: {}\n\n"
        except Exception as e:
            logger.exception("Streaming error: %s", e)
            yield ("data: " + json.dumps({"error":"internal","message":str(e)}) + "\n\n").encode("utf-8")
            yield b"event: done\ndata: {}\n\n"

    return StreamingResponse(gen(), media_type="text/event-stream", headers={"Cache-Control":"no-cache"})
