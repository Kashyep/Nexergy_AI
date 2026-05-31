"""
Application configuration for Nexergy AI.
Uses SQLite database stored as database.db in the project root.
"""
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Flask configuration settings."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "nexergy-ai-dev-secret-key-change-in-production")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
