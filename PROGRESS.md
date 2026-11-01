# Progress

Commit after every class. Tag every Friday: `git tag week-N && git push origin week-N`.

## Week 1
- [x] Repository created and project defined
- [x] README and project questions added
- [x] FastAPI /health endpoint
- [x] Dataset inventory started
- [ ] 50+ verified PDF pages collected and sample files checked in
- [x] Week 1 tag exists

## Week 2
- [x] POST /chat calls an OpenAI-compatible LLM and returns validated structured JSON
- [x] Tamil/English language handling and evidence-aware citation schema
- [x] POST /chat/stream streams Server-Sent Events
- [x] Configurable timeouts, retries with backoff and fallback model
- [x] Token and estimated-cost logging
- [x] GET /usage aggregates totals by model
- [x] Docker Compose (API + PostgreSQL/pgvector)
- [x] GitHub Actions CI runs Ruff and pytest
- [ ] CI result verified on GitHub Actions
- [ ] Docker Compose smoke-tested locally with a real provider key
- [ ] Week 2 tag pushed after validation

## Week 3 (planned)
- [ ] Parser keeps page numbers and headings
- [ ] 500+ pages chunked, embedded and stored in pgvector
- [ ] POST /ask answers with [document, page] citations
- [ ] docs/EVAL_v0.md with 10 questions scored
- [ ] Tag week-3 pushed

## Daily log
| Date | What I did today | Commit |
|---|---|---|
| 2026-11-01 | Implemented Week 2 API, streaming, usage accounting, Compose and CI | pending |
