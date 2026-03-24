import json
from pathlib import Path
from typing import Dict, List


class JsonKnowledgeService:
    def __init__(self, file_path: str) -> None:
        self.file_path = Path(file_path)

    def get_articles(self) -> List[Dict]:
        if not self.file_path.exists():
            return []
        with self.file_path.open('r', encoding='utf-8') as f:
            payload = json.load(f)
        return payload.get('articles', [])

    def find_relevant(self, query: str, limit: int = 3) -> List[Dict]:
        query_tokens = {token.lower() for token in query.split() if token.strip()}
        scored: List[Dict] = []
        for article in self.get_articles():
            text = f"{article.get('title', '')} {article.get('content', '')}".lower()
            score = sum(1 for token in query_tokens if token in text)
            if score > 0:
                scored.append({'score': score, 'article': article})

        scored.sort(key=lambda item: item['score'], reverse=True)
        return [item['article'] for item in scored[:limit]]
