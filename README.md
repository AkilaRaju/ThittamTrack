# ThittamTrack

> Making Tamil Nadu budget information easier to find and understand in Tamil and English.

ThittamTrack is a multilingual research assistant for Tamil Nadu budget publications. It is being built in stages: Week 2 delivers the LLM chat service, streaming, usage accounting and containerized API; Week 3 adds PDF ingestion, multilingual retrieval and source-grounded RAG.

## Week 2 status

- FastAPI `POST /chat` with validated structured JSON responses.
- Tamil/English response-language selection (automatic Tamil-script detection or explicit language).
- Optional source context and citation schema. The API does not invent citations when context is absent.
- `POST /chat/stream` streams provider output as Server-Sent Events (SSE).
- Configurable request timeout, retry with backoff and fallback model.
- Token and estimated-cost logging; `GET /usage` aggregates totals by model.
- Docker Compose with FastAPI and PostgreSQL + pgvector.
- GitHub Actions runs Ruff and pytest.

**Important:** Week 2 does not yet perform PDF retrieval. Until the Week 3 parser and retriever are connected, callers must supply source context themselves. With no context, the system is instructed to report insufficient evidence.

## Requirements

- Python 3.12+
- An OpenAI-compatible Chat Completions API key
- Docker Desktop / Docker Engine for the Compose setup

## Run locally

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
Copy-Item .env.example .env
```

Set `LLM_API_KEY` in `.env`. Keep the real `.env` out of Git.

```powershell
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs

## Run with Docker Compose

```bash
cp .env.example .env
# Set LLM_API_KEY in .env
docker compose up --build
```

On Windows PowerShell, use `Copy-Item .env.example .env` instead of `cp`.

The API is available at http://localhost:8000 and PostgreSQL is exposed on port 5432 for local development. Compose waits for the database health check before starting the API.

## API

### `POST /chat`

Request:

```json
{
  "question": "What is the revenue deficit?",
  "language": "en",
  "context": [
    {
      "document": "Interim Budget 2026-27",
      "page": 12,
      "language": "en",
      "text": "Paste a verified passage here."
    }
  ]
}
```

Response shape:

```json
{
  "answer": "Answer grounded in the supplied passage.",
  "language": "en",
  "citations": [
    {
      "document": "Interim Budget 2026-27",
      "page": 12,
      "quote": "Paste a verified passage here."
    }
  ],
  "confidence": "high",
  "insufficient_evidence": false,
  "model": "gpt-4o-mini"
}
```

### `POST /chat/stream`

Accepts the same request body and returns Server-Sent Events. Events have `type=token` while the model streams, followed by a validated `type=result` event and `[DONE]`.

### `GET /usage`

Returns successful request count, prompt/completion/total tokens, estimated USD cost and per-model totals. Usage is stored in PostgreSQL when `DATABASE_URL` is configured; otherwise an in-memory ledger is used for local development and tests.

### `GET /health`

Lightweight liveness endpoint that does not call the model.

## Configuration

See [`.env.example`](.env.example). The default model names and per-million-token rates are examples for an OpenAI-compatible provider. Change the base URL, model IDs and rates to match the provider actually used. Cost values are estimates based on provider-reported token usage, not billing statements.

## Development checks

```bash
ruff check .
pytest -q
```

## Project roadmap

- **Week 1:** Repository setup, project definition, user questions and dataset inventory.
- **Week 2:** Chat API, structured output, streaming, timeout/retry/fallback, usage tracking, Docker Compose and CI.
- **Week 3:** Tamil/English PDF parsing, page-aware chunking, multilingual embeddings, pgvector indexing, `POST /ask` and retrieval evaluation.
- **Later:** Cross-language recall evaluation, side-by-side Tamil/English citations, budget comparisons and journalist-reviewed fact-checking.

## Dataset

Official source: https://financedept.tn.gov.in/en/budget-speech

The planned dataset covers at least five budget years, Tamil and English budget publications where available, Budget Highlights, Citizen's Guide, Interim and Revised Budget 2026–27 documents, and the Economic Survey of Tamil Nadu. See [DATASET.md](DATASET.md) for the inventory. Document page counts and source URLs must be verified against the downloaded files before reporting dataset coverage.

## Evaluation goals

The planned retrieval evaluation uses 60 questions (30 Tamil and 30 English) and reports Tamil-to-English, English-to-Tamil and same-language Recall@5 separately. The target is 85%+; it is not yet a measured result.

## Live link

Not deployed yet.
