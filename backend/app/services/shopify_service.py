from typing import Dict


class ShopifyLookupService:
    """Placeholder for future authenticated Shopify API requests."""

    def lookup(self, user_query: str) -> Dict:
        return {
            'enabled': False,
            'note': 'Shopify API lookup is not enabled in MVP.',
            'query': user_query,
        }
