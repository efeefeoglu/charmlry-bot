# Backend (FastAPI)

## Endpoints
- `GET /health`
- `POST /chat`

## Notes
- Stateless server: no DB, no persisted sessions.
- Frontend sends full message history each request.
- `api/main.py` and `main.py` are deployment entrypoint shims.
