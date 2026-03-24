from typing import Dict


class CustomApiService:
    """Placeholder for future custom API integration."""

    def lookup(self, user_query: str) -> Dict:
        return {
            'enabled': False,
            'note': 'Custom API endpoint integration is not enabled in MVP.',
            'query': user_query,
        }
