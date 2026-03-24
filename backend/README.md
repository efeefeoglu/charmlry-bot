# Backend (FastAPI)

## Run

```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints
- `GET /health`
- `POST /chat`

## Notes
- Stateless server: no DB, no persisted sessions.
- Frontend sends full message history each request.
