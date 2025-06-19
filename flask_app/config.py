import os
import logging

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_FILE = os.environ.get('LOG_FILE', 'flask_app.log')
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

def setup_logging(app):
    log_level = getattr(logging, app.config.get('LOG_LEVEL', 'INFO').upper(), logging.INFO)
    logging.basicConfig(
        filename=app.config.get('LOG_FILE', 'flask_app.log'),
        level=log_level,
        format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )
    app.logger.setLevel(log_level)
    app.logger.info('Logging is set up.')
