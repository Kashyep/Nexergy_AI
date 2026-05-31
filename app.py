"""
Nexergy AI — Flask application entry point.
Run with: python app.py
"""
import os

from flask import Flask

from config import Config
from models import db
from routes import register_blueprints


def create_app():
    """Application factory — configures Flask and database."""
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    register_blueprints(app)

    with app.app_context():
        # Create all tables on startup
        db.create_all()

    @app.context_processor
    def inject_globals():
        return {"app_name": "Nexergy AI"}

    return app


app = create_app()


if __name__ == "__main__":
    # Development server
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
