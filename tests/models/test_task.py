import pytest
from app.models.task import Task


TASK_NAME = "Sample Task"
TASK_PRIORITY = 2


@pytest.fixture
def sample_task():
    return Task(name=TASK_NAME, priority=TASK_PRIORITY)


def test_task_initialization(sample_task):
    assert sample_task.name == TASK_NAME
    assert sample_task.priority == TASK_PRIORITY


def test_task_repr(sample_task):
    str_task = repr(sample_task)
    str_expected = f'Task {None} - name: {TASK_NAME}, priority: {TASK_PRIORITY}, ' \
               f'created_at: {None}, updated_at: {None}'
    assert str_task == str_expected


def test_task_eq():
    task1 = Task(name='Task 1', priority=1, created_at='2022-01-01', updated_at='2022-01-01')
    task2 = Task(name='Task 2', priority=2, created_at='2022-01-02', updated_at='2022-01-02')
    assert task1 == task1
    assert task1 != task2
    assert task1 != object()
