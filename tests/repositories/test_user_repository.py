import pytest
from app import db
from app.repositories.user_repository import UserRepository


@pytest.fixture(scope='module')
def app():
    """
    App fixture with a test in-memory database.
    """
    from flask import Flask
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


def test_create_user(app):
    """
    Ensure that we can successfully create a user, only if a user with the same username does not exist.
    """
    with app.app_context():
        assert UserRepository.create_user('test_user', 'password123') is True
        assert UserRepository.create_user('test_user', 'password123') is False


def test_get_user_by_username(app):
    """
    Ensure we can correctly retrieve a user by its username, if it exists.
    Retrieving a non-existing user returns None.
    """
    with app.app_context():
        UserRepository.create_user('test_user', 'password123')
        user = UserRepository.get_user_by_username('test_user')
        assert UserRepository.get_user_by_username('non_existing_user') is None
        assert user is not None
        assert user.username == 'test_user'
