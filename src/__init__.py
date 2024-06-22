from flask import Flask

# Routes
from .routes import WebhookRoute


app = Flask(__name__)

def init_app(config):
    # Configuration
    app.config.from_object(config)

    # Blueprints
    app.register_blueprint(WebhookRoute.main)
    
    return app

