# Shopify Chatbot MVP (FastAPI + LangChain + Gemini)

Simple, production-minded Shopify chatbot MVP with:
- **Shopify integration** via script embed
- **Backend**: FastAPI
- **LLM**: LangChain + `gemini-flash-lite-latest`
- **Frontend**: vanilla JS widget
- **No DB**, no server-side sessions, each browser session starts fresh (history in `sessionStorage`)
- **Non-streaming** full-text response

## Project structure

- `backend/app/main.py` - FastAPI app and `/chat` endpoint
- `backend/app/config` - settings/env parsing
- `backend/app/schemas` - request/response models
- `backend/app/services` - JSON knowledge + placeholders for Shopify/custom API
- `backend/app/chains` - LangChain orchestration
- `frontend/widget` - embeddable widget JS/CSS
- `frontend/test-page` - standalone local test page
- `docs/shopify-embed-snippet.liquid` - Shopify embed example
- `docs/nginx.conf.example` - production reverse proxy example

## API contract

`POST /chat`

Request:
```json
{
  "messages": [{"role": "user", "content": "Hi"}],
  "page_context": {"url": "https://example.com", "title": "Example"}
}
```

Response:
```json
{
  "reply": "Hello",
  "sources": [],
  "meta": {"model": "gemini-flash-lite-latest"}
}
```

## Local development

### 1) Backend

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2) Frontend test page

You can open the test page in either of these ways:
- From FastAPI (after starting backend): `http://127.0.0.1:8000/frontend/test-page/index.html`
- Or by serving repository root with a static server: `frontend/test-page/index.html`

Static server example:
```bash
python -m http.server 5500
# then open http://127.0.0.1:5500/frontend/test-page/index.html
```

## Production notes

- Run FastAPI app with process manager (systemd/supervisor).
- Put Nginx in front using `docs/nginx.conf.example`.
- Upload widget JS/CSS to Shopify theme assets and include snippet from `docs/shopify-embed-snippet.liquid`.

## Extendability

Current architecture already separates data sources:
- JSON knowledge service (implemented)
- Shopify API lookup service (placeholder)
- Custom API service (placeholder)

You can replace placeholder service methods with real API clients later without changing `/chat` contract.
