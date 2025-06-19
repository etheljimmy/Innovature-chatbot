from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import setup_logging
db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)

    # CORS for develP
    CORS(app)
    setup_logging(app)
    from .routes.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    # error 
    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(f"Unhandled Exception: {e}", exc_info=True)
        return {"error": "Internal server error"}, 500

    return app
