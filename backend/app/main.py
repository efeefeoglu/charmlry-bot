from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.app.chains.chat_chain import ChatChain, collect_sources
from backend.app.config.settings import get_settings
from backend.app.schemas.chat import ChatRequest, ChatResponse, SourceItem
from backend.app.services.custom_api_service import CustomApiService
from backend.app.services.knowledge_service import JsonKnowledgeService
from backend.app.services.shopify_service import ShopifyLookupService

settings = get_settings()
app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

knowledge_service = JsonKnowledgeService('backend/app/data/knowledge.json')
shopify_service = ShopifyLookupService()
custom_api_service = CustomApiService()



project_root = Path(__file__).resolve().parents[2]
frontend_dir = project_root / 'frontend'
if frontend_dir.exists():
    app.mount('/frontend', StaticFiles(directory=frontend_dir), name='frontend')

@app.get('/health')
def health() -> dict:
    return {'status': 'ok'}


@app.post('/chat', response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    if not payload.messages:
        return ChatResponse(
            reply='Please send at least one message.',
            sources=[],
            meta={'model': settings.gemini_model},
        )

    latest_user_message = next((m.content for m in reversed(payload.messages) if m.role == 'user'), '')
    knowledge_snippets = knowledge_service.find_relevant(latest_user_message, limit=3)

    shopify_hint = shopify_service.lookup(latest_user_message)
    custom_hint = custom_api_service.lookup(latest_user_message)

    chain = ChatChain(model_name=settings.gemini_model, google_api_key=settings.google_api_key)
    reply = chain.run(
        history=payload.messages,
        page_context=payload.page_context.model_dump(),
        knowledge_snippets=knowledge_snippets,
        shopify_hint=shopify_hint,
        custom_hint=custom_hint,
    )

    sources = [
        SourceItem(source_type=s[0], source_id=s[1], title=s[2])
        for s in collect_sources(knowledge_snippets)
    ]

    return ChatResponse(reply=reply, sources=sources, meta={'model': settings.gemini_model})
