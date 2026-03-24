from typing import Dict, List, Tuple

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from backend.app.prompts.chat_prompt import SYSTEM_PROMPT
from backend.app.schemas.chat import ChatMessage


class ChatChain:
    def __init__(self, model_name: str, google_api_key: str) -> None:
        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=google_api_key,
            temperature=0.2,
        )

    def build_messages(
        self,
        history: List[ChatMessage],
        page_context: Dict,
        knowledge_snippets: List[Dict],
        shopify_hint: Dict,
        custom_hint: Dict,
    ) -> List:
        context_lines = [
            f"Page URL: {page_context.get('url', '')}",
            f"Page title: {page_context.get('title', '')}",
        ]

        if knowledge_snippets:
            context_lines.append('Knowledge snippets:')
            for item in knowledge_snippets:
                context_lines.append(f"- {item.get('title', '')}: {item.get('content', '')}")

        context_lines.append(f"Shopify service status: {shopify_hint.get('note', '')}")
        context_lines.append(f"Custom API status: {custom_hint.get('note', '')}")

        messages = [SystemMessage(content=SYSTEM_PROMPT), SystemMessage(content='\n'.join(context_lines))]

        for message in history:
            if message.role == 'assistant':
                messages.append(AIMessage(content=message.content))
            elif message.role == 'user':
                messages.append(HumanMessage(content=message.content))

        return messages

    def run(
        self,
        history: List[ChatMessage],
        page_context: Dict,
        knowledge_snippets: List[Dict],
        shopify_hint: Dict,
        custom_hint: Dict,
    ) -> str:
        messages = self.build_messages(history, page_context, knowledge_snippets, shopify_hint, custom_hint)
        response = self.llm.invoke(messages)
        return response.content if isinstance(response.content, str) else str(response.content)


def collect_sources(knowledge_snippets: List[Dict]) -> List[Tuple[str, str, str]]:
    result = []
    for item in knowledge_snippets:
        result.append(('json_knowledge', str(item.get('id', 'unknown')), item.get('title', 'Untitled')))
    return result
