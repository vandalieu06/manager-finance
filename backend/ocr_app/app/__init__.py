from flask import Flask


def create_app():
    """Factory para crear la aplicación Flask."""
    app = Flask(__name__)

    from .routes import ticket_bp

    app.register_blueprint(ticket_bp, url_prefix='/api')

    return app
