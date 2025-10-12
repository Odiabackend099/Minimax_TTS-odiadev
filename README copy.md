# OdeaDev‑AI‑TTS

Python FastAPI service that wraps MiniMax T2A API under your brand. Includes key scaffolding, auth utilities, and tests.

## Quick start
```bash
pip install -r requirements.txt
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

## Structure
- `src/` – app, DB, models, schemas, auth
- `tests/` – unittest
- `.env.example` – fill in `MINIMAX_API_KEY`, `MINIMAX_GROUP_ID`, `DATABASE_URL`
- `planning.md` – phases, tech reqs, test criteria

## Next
- Add auth middleware to validate your client API keys
- Implement `/v1/tts` calling MiniMax T2A v2 with streaming
- Usage metering + quotas per plan
- Admin endpoints for keys/voices/rate limits
