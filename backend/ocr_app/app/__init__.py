from flask import Flask

from .routes import ticket_bp


def create_app():
    """Factory para crear la aplicación Flask."""
    app = Flask(__name__)

    app.register_blueprint(ticket_bp, url_prefix="/api")

    return app
