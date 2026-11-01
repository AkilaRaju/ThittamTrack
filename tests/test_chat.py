import json

import pytest

from app.schemas import ChatRequest, ChatResponse


@pytest.mark.asyncio
async def test_chat_returns_structured_json(client, monkeypatch):
    from app import main

    async def fake_chat(payload, settings):
        return ChatResponse(
            answer="Evidence is not available yet.",
            language="en",
            citations=[],
            confidence="low",
            insufficient_evidence=True,
            model="test-model",
        )

    monkeypatch.setattr(main, "chat_completion", fake_chat)
    response = client.post("/chat", json={"question": "What is the school education allocation?"})

    assert response.status_code == 200
    body = response.json()
    assert body["language"] == "en"
    assert body["citations"] == []
    assert body["insufficient_evidence"] is True
    assert body["model"] == "test-model"


def test_chat_rejects_empty_question(client):
    response = client.post("/chat", json={"question": ""})
    assert response.status_code == 422


def test_usage_endpoint_returns_cost_summary(client):
    response = client.get("/usage")
    assert response.status_code == 200
    body = response.json()
    assert body["requests"] >= 0
    assert body["estimated_cost_usd"] >= 0
    assert "by_model" in body


def test_auto_language_detects_tamil():
    from app.llm import _language

    assert _language(ChatRequest(question="பள்ளிக் கல்விக்கு எவ்வளவு நிதி?")) == "ta"


def test_response_json_parser_rejects_invalid_shape():
    from app.llm import _parse_response

    with pytest.raises((ValueError, json.JSONDecodeError)):
        _parse_response('{"answer": 123}', "test-model")
