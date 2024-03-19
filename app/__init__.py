import os
import logging


from os import getenv
from config import TestConfig
from flask import Flask, request
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from logging.handlers import RotatingFileHandler


db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=['1 per second', '50 per hour']
)


def configure_logging(app: Flask) -> None:
    logs_dir = 'logs'
    os.makedirs(logs_dir, exist_ok=True)
    log_file = os.path.join(logs_dir, 'app.log')
    handler = RotatingFileHandler(log_file, maxBytes=1000000, backupCount=3)  # 1 MB limit, keep 3 old log files
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)


def configure_extensions(app: Flask) -> None:
    db.init_app(app)  # Bound db to app
    app.logger.info('db bounded to app')
    migrate.init_app(app, db)
    app.logger.info('alembic bounded to app')
    limiter.init_app(app)
    app.logger.info('limiter bounded to app')
    jwt.init_app(app)
    app.logger.info('jwt manager bounded to app')


def init_database(app: Flask) -> None:
    with app.app_context():
        if getenv("INIT_DATABASE"):
            from app.models.task import Task  # be sure to import all the models before running create_all
            from app.models.user import User
            # db.drop_all()
            db.create_all()
            app.logger.info('db.create_all()')


def register_blueprints(app):
    from app.api import api_bp
    app.register_blueprint(api_bp, url_prefix='')
    app.logger.info('blueprints registered')


def create_app(config=TestConfig) -> Flask:
    """
    Flask factory.

    :return: app
    """
    app = Flask(__name__)
    app.config.from_object(config())
    configure_logging(app)
    configure_extensions(app)
    init_database(app)
    register_blueprints(app)

    @app.before_request
    def log_request_info() -> None:
        app.logger.info('Request: %s %s', request.method, request.url)
        app.logger.info('Request Headers: %s', request.headers)
        app.logger.info('Request Body: %s', request.get_data())

    # Error handler for unhandled exceptions
    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.exception(e)
        return {'message': 'Internal Server Error'}, 500

    return app
