from flask import Flask
from server.views import search_bp


def create_app(config='server.config'):
    """Create Flask Application

    Args:
        config (str, optional): Application configuration. Defaults to 'server.config'.

    Returns:
        flask.Flask: Flask application
    """
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(search_bp)

    return app
