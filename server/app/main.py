import asyncio
import json
import os
from datetime import datetime, timezone

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse

app = FastAPI(title="RTCRM FastAPI")

# CORS (relax for MVP; tighten in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # set to your web origin later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
async def healthz():
    return JSONResponse({"ok": True, "time": datetime.now(timezone.utc).isoformat()})

def sse_event(event: str, data: dict) -> bytes:
    # SSE event with NDJSON data
    return (f"event: {event}\n" f"data: {json.dumps(data, separators=(',',':'))}\n\n").encode("utf-8")

@app.get("/stream-demo")
async def stream_demo():
    async def gen():
        # Note: Cloud Run requires periodic data to keep connection alive.
        # Frame 1
        yield sse_event("frame", {"step":"reasoning","payload":{"hello":"world","kpis":["CVR","AOV"]}})
        await asyncio.sleep(0.4)
        # Frame 2
        yield sse_event("frame", {"step":"audience","payload":{"segments":[{"name":"HighIntentCartAbandoners","size":13842}]}})
        await asyncio.sleep(0.4)
        # Final
        yield sse_event("final", {"artifact":{"version":"0.0.1","channels":["email","sms","whatsapp","ads"]}})

    return StreamingResponse(gen(), media_type="text/event-stream", headers={
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
    })
