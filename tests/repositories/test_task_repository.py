import pytest
from app import db
from app.repositories.task_repository import TaskRepository
from app.models.task import Task

TASK1_NAME = 'Task1'
TASK2_NAME = 'Task2'
TASK1_PRIORITY = 1
TASK2_PRIORITY = 3


@pytest.fixture
def task1():
    return Task(name=TASK1_NAME, priority=TASK1_PRIORITY)


@pytest.fixture
def task2():
    return Task(name=TASK2_NAME, priority=TASK2_PRIORITY)


@pytest.fixture
def app(task1, task2):
    from flask import Flask
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
        db.session.add_all([task1, task2])
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.mark.parametrize("id, name, priority", [
    (1, TASK1_NAME, TASK1_PRIORITY),
    (2, TASK2_NAME, TASK2_PRIORITY)
])
def test_get_task_by_id(id, name, priority, app):
    with app.app_context():
        task = TaskRepository.get_task_by_id(id)
        retrieved_task = Task.query.filter_by(name=name, priority=priority).first()
        assert task == retrieved_task


def test_get_all_tasks(app, task1, task2):
    with app.app_context():
        tasks = TaskRepository.get_all_tasks()
        assert len(tasks) == 2
        assert task1 in tasks
        assert task2 in tasks


@pytest.mark.parametrize("name, priority", [
    (TASK1_NAME, TASK1_PRIORITY),
    (TASK2_NAME, TASK2_PRIORITY)
])
def test_create_task(name, priority, app):
    with app.app_context():
        task = TaskRepository.create_task(name, priority)
        assert task.id is not None
        assert task.name == name
        assert task.priority == priority
        assert task.created_at is not None
        assert task.updated_at is not None


def test_update_task_by_id(app):
    with app.app_context():
        task = TaskRepository.create_task('task_name', 0)
        updated_task = TaskRepository.update_task_by_id(task.id, 'updated_name', 2)
        non_existing_task = TaskRepository.update_task_by_id(-123, 'updated_name', 2)
        assert updated_task.name == 'updated_name'
        assert updated_task.priority == 2
        assert updated_task.updated_at > updated_task.created_at
        assert non_existing_task is None


def test_delete_task_by_id(app):
    assert TaskRepository.delete_task_by_id(1) == True
    assert TaskRepository.delete_task_by_id(-123) == False


def test_delete_all_tasks(app):
    TaskRepository.delete_all_tasks()
    tasks = TaskRepository.get_all_tasks()
    assert len(tasks) == 0