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
- `frontend/test-page` - standalone test page
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

## Production notes

- Deploy FastAPI app to Vercel using `api/main.py` as the entrypoint.
- Configure runtime environment variables from `.env.example`.
- Upload widget JS/CSS to Shopify theme assets and include snippet from `docs/shopify-embed-snippet.liquid`.

## Extendability

Current architecture already separates data sources:
- JSON knowledge service (implemented)
- Shopify API lookup service (placeholder)
- Custom API service (placeholder)

You can replace placeholder service methods with real API clients later without changing `/chat` contract.
