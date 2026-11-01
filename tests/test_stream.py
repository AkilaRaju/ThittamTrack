def test_stream_endpoint_uses_sse(client, monkeypatch):
    from app import main

    async def fake_stream(payload, settings):
        yield {"type": "token", "text": '{"answer":'}
        yield {"type": "result", "data": {"answer": "Hello"}}

    monkeypatch.setattr(main, "stream_completion", fake_stream)
    response = client.post("/chat/stream", json={"question": "Hello ThittamTrack"})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/event-stream")
    assert '"type": "token"' in response.text
    assert "[DONE]" in response.text
