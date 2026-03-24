"""Deployment entrypoint shim for platforms that auto-detect `api/main.py`."""

from backend.app.main import app

__all__ = ['app']
