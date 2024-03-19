from dotenv import load_dotenv

load_dotenv()

import pytest

from app import create_app, db, limiter
from config import TestConfig


@pytest.fixture(scope='module')
def app():
    """
    App fixture with a test in-memory database.
    """
    app = create_app(TestConfig)
    limiter.enabled = False  # disable rate limiter, otherwise API tests will fail with 429 TOO MANY REQUESTS error
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """
    Create a test client for the Flask app.
    """
    with app.test_client() as client:
        yield client
