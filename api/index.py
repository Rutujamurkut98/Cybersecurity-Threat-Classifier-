"""Vercel entrypoint for serving the Flask app."""

from app.app import app

# Vercel Python runtime looks for a module-level `app` object.
