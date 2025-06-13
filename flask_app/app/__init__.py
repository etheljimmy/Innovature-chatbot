from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)

    # Enable CORS for development
    CORS(app)

    # Register blueprints here
    from .routes.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app
