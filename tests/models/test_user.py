import pytest
from app.models.user import User
from unittest.mock import patch


# Test data
USERNAME = "testuser"
PASSWORD = "testpassword"


@pytest.fixture
def sample_user():
    return User(username=USERNAME)


def test_user_initialization(sample_user):
    assert sample_user.username == USERNAME


@patch('app.models.user.generate_password_hash')
def test_set_password(mock_generate_password_hash, sample_user):
    mock_generate_password_hash.return_value = "hashedpassword"
    sample_user.set_password(PASSWORD)
    mock_generate_password_hash.assert_called_once_with(PASSWORD)
    assert sample_user.password_hash == "hashedpassword"


def test_check_password(sample_user):
    sample_user.set_password(PASSWORD)
    assert sample_user.check_password(PASSWORD)


def test_user_repr(sample_user):
    str_user = repr(sample_user)
    str_expected = f'User {None} - username: {USERNAME}'
    assert str_user == str_expected


def test_user_eq():
    user1 = User(username='testuser')
    user2 = User(username='testuser2')
    user3 = User(username='testuser')
    assert user1 != user2
    assert user1 == user3
    assert user1 != object()
