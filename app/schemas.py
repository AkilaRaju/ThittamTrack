"""Validated API contracts for ThittamTrack chat and usage reporting."""

from typing import Literal

from pydantic import BaseModel, Field


class SourceContext(BaseModel):
    document: str = Field(min_length=1, max_length=300)
    page: int | None = Field(default=None, ge=1)
    language: Literal["ta", "en", "unknown"] = "unknown"
    text: str = Field(min_length=1, max_length=12000)


class ChatRequest(BaseModel):
    question: str = Field(min_length=2, max_length=4000)
    language: Literal["ta", "en", "auto"] = "auto"
    context: list[SourceContext] = Field(default_factory=list, max_length=20)


class Citation(BaseModel):
    document: str
    page: int | None = None
    quote: str = ""


class ChatResponse(BaseModel):
    answer: str
    language: Literal["ta", "en"]
    citations: list[Citation] = Field(default_factory=list)
    confidence: Literal["high", "medium", "low"]
    insufficient_evidence: bool = False
    model: str | None = None


class UsageSummary(BaseModel):
    requests: int
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    estimated_cost_usd: float
    by_model: dict[str, dict[str, float | int]]
