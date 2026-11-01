"""PostgreSQL usage persistence with an in-memory fallback for local tests."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import asyncpg

_pool: asyncpg.Pool | None = None
_memory_usage: list[dict[str, Any]] = []


async def open_database(database_url: str) -> None:
    global _pool
    if not database_url:
        return
    _pool = await asyncpg.create_pool(database_url, min_size=1, max_size=5)
    async with _pool.acquire() as connection:
        await connection.execute("CREATE EXTENSION IF NOT EXISTS vector")
        await connection.execute(
            """
            CREATE TABLE IF NOT EXISTS llm_usage (
                id BIGSERIAL PRIMARY KEY,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                model TEXT NOT NULL,
                prompt_tokens INTEGER NOT NULL DEFAULT 0,
                completion_tokens INTEGER NOT NULL DEFAULT 0,
                total_tokens INTEGER NOT NULL DEFAULT 0,
                estimated_cost_usd DOUBLE PRECISION NOT NULL DEFAULT 0,
                request_status TEXT NOT NULL DEFAULT 'success'
            )
            """
        )


async def close_database() -> None:
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None


async def record_usage(
    *,
    model: str,
    prompt_tokens: int,
    completion_tokens: int,
    estimated_cost_usd: float,
    request_status: str = "success",
) -> None:
    row = {
        "created_at": datetime.now(UTC),
        "model": model,
        "prompt_tokens": max(0, prompt_tokens),
        "completion_tokens": max(0, completion_tokens),
        "total_tokens": max(0, prompt_tokens) + max(0, completion_tokens),
        "estimated_cost_usd": max(0.0, estimated_cost_usd),
        "request_status": request_status,
    }
    if _pool is None:
        _memory_usage.append(row)
        return
    async with _pool.acquire() as connection:
        await connection.execute(
            """
            INSERT INTO llm_usage
                (model, prompt_tokens, completion_tokens, total_tokens,
                 estimated_cost_usd, request_status)
            VALUES ($1, $2, $3, $4, $5, $6)
            """,
            row["model"],
            row["prompt_tokens"],
            row["completion_tokens"],
            row["total_tokens"],
            row["estimated_cost_usd"],
            row["request_status"],
        )


async def get_usage_summary() -> dict[str, Any]:
    if _pool is None:
        rows = _memory_usage
    else:
        async with _pool.acquire() as connection:
            rows = await connection.fetch(
                """
                SELECT model, prompt_tokens, completion_tokens, total_tokens,
                       estimated_cost_usd
                FROM llm_usage
                WHERE request_status = 'success'
                """
            )

    summary: dict[str, Any] = {
        "requests": len(rows),
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
        "estimated_cost_usd": 0.0,
        "by_model": {},
    }
    for row in rows:
        model = row["model"]
        bucket = summary["by_model"].setdefault(
            model,
            {
                "requests": 0,
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
                "estimated_cost_usd": 0.0,
            },
        )
        for key in ("prompt_tokens", "completion_tokens", "total_tokens"):
            value = int(row[key] or 0)
            summary[key] += value
            bucket[key] += value
        cost = float(row["estimated_cost_usd"] or 0.0)
        summary["estimated_cost_usd"] += cost
        bucket["estimated_cost_usd"] += cost
        bucket["requests"] += 1

    summary["estimated_cost_usd"] = round(summary["estimated_cost_usd"], 8)
    for bucket in summary["by_model"].values():
        bucket["estimated_cost_usd"] = round(bucket["estimated_cost_usd"], 8)
    return summary
