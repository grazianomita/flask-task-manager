import pytest

from unittest.mock import patch, Mock
from flask_jwt_extended import create_access_token, create_refresh_token


@pytest.mark.parametrize("username, password, status_code, message", [
    ('testuser', 'TestPassword123#', 201, 'successfully'),
    ('testuser', 'TestPassword123', 400, 'symbol'),
    ('testuser', 'TestPassword#', 400, 'digit'),
    ('testuser', 'test', 400, '8 characters long'),
    ('testuser', 'testtesttest', 400, 'uppercase'),
    ('testuser', 'TESTTESTTEST', 400, 'lowercase'),
])
def test_user_registration(username, password, status_code, message, client):
    """Test user registration endpoint."""
    response = client.post('/api/register', json={'username': username, 'password': password})
    duplicated_user_response = client.post('/api/register', json={'username': username, 'password': 'TestPassword123#'})
    assert response.status_code == status_code
    assert message in response.json['message']
    assert duplicated_user_response.status_code == 400
    assert 'already exists' in duplicated_user_response.json['message']


@patch('app.repositories.user_repository.UserRepository.get_user_by_username')
def test_user_login_success(mock_get_user_by_username, client):
    """
    Ensure users that specify a valid password can login.
    """
    mock_user = Mock()
    mock_user.username = 'testuser'
    mock_user.check_password.return_value = True
    mock_get_user_by_username.return_value = mock_user
    response = client.post('/api/login', json={'username': 'testuser', 'password': 'TestPassword123#'})
    mock_get_user_by_username.assert_called_with('testuser')
    assert response.status_code == 200
    assert 'access_token' in response.json
    assert 'refresh_token' in response.json


@pytest.mark.parametrize("user_exists", [True, False])
@patch('app.repositories.user_repository.UserRepository.get_user_by_username')
def test_user_login_failed(mock_get_user_by_username, user_exists, client):
    """
    Ensure that a proper error message is raised when the user does not exist or the provided password is wrong.
    """
    if user_exists:
        mock_user = Mock()
        mock_user.username = 'testuser'
        mock_user.check_password.return_value = False
    else:
        mock_user = None
    mock_get_user_by_username.return_value = mock_user
    response = client.post('/api/login', json={'username': 'testuser', 'password': 'TestPassword123#'})
    mock_get_user_by_username.assert_called_with('testuser')
    assert response.status_code == 401
    assert 'invalid' in response.json['message']


@patch('app.api.resources.user.get_jwt_identity')
def test_token_refresh_success(mock_get_jwt_identity, client):
    jwt_refresh_token = create_refresh_token(identity='test_user')
    mock_get_jwt_identity.return_value = 'test_user'
    response = client.post('/api/refresh', headers={'Authorization': f'Bearer {jwt_refresh_token}'})
    mock_get_jwt_identity.assert_called_once_with()
    assert response.status_code == 200
    assert 'access_token' in response.json