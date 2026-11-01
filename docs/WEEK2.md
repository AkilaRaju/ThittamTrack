# Week 2 implementation notes

## Scope

Week 2 implements the LLM service layer and operational foundation. It intentionally does not implement document retrieval; that is scheduled for Week 3.

## Request flow

1. FastAPI validates the incoming `ChatRequest`.
2. The service builds a bilingual, evidence-aware prompt.
3. The configured primary model is called through an OpenAI-compatible Chat Completions API.
4. Failed requests are retried with exponential backoff, then the fallback model is tried.
5. The returned JSON is validated against `ChatResponse`.
6. Provider-reported token counts are used to estimate cost and record a usage row.

## Endpoints

- `GET /health`: liveness.
- `POST /chat`: structured chat response.
- `POST /chat/stream`: SSE token events followed by a validated result event.
- `GET /usage`: aggregate token and cost totals.

## Cost accounting

Cost is calculated as:

`(prompt_tokens * input_rate + completion_tokens * output_rate) / 1,000,000`

The configured rates are illustrative defaults and must be updated to the selected provider's current pricing. Usage records are persisted to PostgreSQL when configured. A process-local in-memory ledger is used only when no database URL is configured.

## Local verification

```bash
pip install -r requirements-dev.txt
ruff check .
pytest -q
docker compose config
```

Then set `LLM_API_KEY` in `.env` and run `docker compose up --build`. Check `/docs`, `/health`, `/chat`, `/chat/stream` and `/usage`.

## Limitations

- The LLM endpoint must implement the OpenAI Chat Completions API, JSON response mode and streaming SSE.
- Streaming usage is recorded only if the provider sends the final usage event (`stream_options.include_usage`).
- Cost is an estimate, not a provider invoice.
- Without Week 3 retrieval, answers are only grounded when the caller supplies verified context.
