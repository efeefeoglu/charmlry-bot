"""Deployment entrypoint shim for platforms that auto-detect `main.py`."""

from backend.app.main import app

__all__ = ['app']
