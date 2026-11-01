"""ThittamTrack FastAPI application."""

import json
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import StreamingResponse

from app.config import get_settings
from app.db import close_database, get_usage_summary, open_database
from app.llm import chat_completion, stream_completion
from app.schemas import ChatRequest, ChatResponse, UsageSummary

SettingsDep = Depends(get_settings)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    await open_database(settings.database_url)
    yield
    await close_database()


app = FastAPI(title="ThittamTrack API", version="0.2.0", lifespan=lifespan)


@app.get("/health")
async def health(settings=SettingsDep) -> dict:
    """Liveness check; does not call the LLM."""
    return {"status": "ok", "app": settings.app_name, "environment": settings.environment}


@app.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest, settings=SettingsDep) -> ChatResponse:
    """Generate a structured answer. Context is optional until the Week 3 RAG pipeline."""
    try:
        return await chat_completion(payload, settings)
    except RuntimeError as exc:
        message = str(exc)
        status = 503 if "not configured" in message else 502
        raise HTTPException(status_code=status, detail=message) from exc


@app.post("/chat/stream")
async def chat_stream(payload: ChatRequest, settings=SettingsDep) -> StreamingResponse:
    """Stream model output as Server-Sent Events (SSE)."""

    async def events() -> AsyncIterator[str]:
        try:
            async for event in stream_completion(payload, settings):
                yield f"data: {json.dumps(event, ensure_ascii=False)}\\n\\n"
            yield "data: [DONE]\\n\\n"
        except Exception as exc:
            safe_message = str(exc).replace("\\n", " ")[:500]
            yield f"data: {json.dumps({'type': 'error', 'message': safe_message})}\\n\\n"

    return StreamingResponse(
        events(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.get("/usage", response_model=UsageSummary)
async def usage() -> dict:
    """Return aggregate token and estimated-cost usage."""
    return await get_usage_summary()
