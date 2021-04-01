from flask import Flask
from server.views import search_bp

from .extensions import db


def create_app(config='server.config'):
    """Create Flask Application

    Args:
        config (str, optional): Application configuration. Defaults to 'server.config'.

    Returns:
        flask.Flask: Flask application
    """
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    app.register_blueprint(search_bp)

    with app.app_context():
        db.create_all()

    return app
