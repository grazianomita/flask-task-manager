import pytest

from unittest.mock import patch, Mock
from flask_jwt_extended import create_access_token


@pytest.fixture
def task():
    mock_task = Mock()
    mock_task.id = 1
    mock_task.name = 'Task 1'
    mock_task.priority = 1
    mock_task.created_at = None
    mock_task.updated_at = None
    return mock_task


@pytest.fixture
def json_task():
    return {
        'id': 1,
        'name': 'Task 1',
        'priority': 1,
        'created_at': None,
        'updated_at': None
    }

@pytest.mark.parametrize("existing_task, status_code", [
    (True, 200),
    (False, 404)
])
@patch('app.api.resources.task.TaskRepository')
def test_get_task_by_id(mock_task_repo, existing_task, status_code, task, json_task, client):
    mock_task_repo.get_task_by_id.return_value = task if existing_task else None
    access_token = create_access_token(identity='test_user')
    response = client.get(f'/api/tasks/{task.id}', headers={'Authorization': f'Bearer {access_token}'})
    mock_task_repo.get_task_by_id.assert_called_once_with(task.id)
    if existing_task:
        assert response.status_code == 200
        assert response.json == json_task
    else:
        assert response.status_code == 404
        assert 'not found' in response.json['message']



@patch('app.api.resources.task.TaskRepository')
def test_post_task(mock_task_repo, task, json_task, client):
    access_token = create_access_token(identity='test_user')
    mock_task_repo.create_task.return_value = task
    response = client.post(
        '/api/tasks',
        json={'name': task.name, 'priority': task.priority},
        headers={'Authorization': f'Bearer {access_token}'}
    )
    mock_task_repo.create_task.assert_called_once_with(task.name, task.priority)
    assert response.status_code == 201
    assert response.json == json_task


@pytest.mark.parametrize("existing_task, status_code, message", [
    (True, 200, 'updated'),
    (False, 404, 'not found')
])
@patch('app.api.resources.task.TaskRepository')
def test_put_task(mock_task_repo, existing_task, status_code, message, task, json_task, client):
    access_token = create_access_token(identity='test_user')
    mock_task_repo.update_task_by_id.return_value = task if existing_task else None
    response = client.put(
        f'/api/tasks/{task.id}',
        json={'name': task.name, 'priority': task.priority},
        headers={'Authorization': f'Bearer {access_token}'}
    )
    mock_task_repo.update_task_by_id.assert_called_with(task.id, task.name, task.priority)
    assert response.status_code == status_code
    assert message in response.json['message']



@pytest.mark.parametrize("existing_task, status_code, message", [
    (True, 204, ''),
    (False, 404, 'not found')
])
@patch('app.api.resources.task.TaskRepository')
def test_delete_task(mock_task_repo, existing_task, status_code, message, client):
    mock_task_repo.delete_task_by_id.return_value = existing_task
    access_token = create_access_token(identity='test_user')
    response = client.delete(
        '/api/tasks/1',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    mock_task_repo.delete_task_by_id.assert_called_with(1)
    assert response.status_code == status_code
    print(response.data)
    if existing_task:
        assert response.data.decode('utf-8') == message
    else:
        assert message in response.json['message']


@patch('app.api.resources.task.TaskRepository')
def test_get_all_tasks(mock_task_repo, client):
    mock_task_repo.get_all_tasks.return_value = []
    access_token = create_access_token(identity='test_user')
    response = client.get(
        '/api/tasks',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    assert response.status_code == 200
    assert response.json == []


@patch('app.api.resources.task.TaskRepository')
def test_delete_all_tasks(mock_task_repo, client):
    mock_task_repo.delete_all_tasks.return_value = None
    access_token = create_access_token(identity='test_user')
    response = client.delete(
        '/api/tasks',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    assert response.status_code == 204
