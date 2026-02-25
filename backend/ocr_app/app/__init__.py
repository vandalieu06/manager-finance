import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask


def create_app():
    """Factory para crear la aplicación Flask."""
    app = Flask(__name__)

    from .routes import ticket_bp

    app.register_blueprint(ticket_bp, url_prefix='/api')

    return app
