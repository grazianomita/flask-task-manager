from app.models.task import Task
from app import db


class TaskRepository:
    """
    Class to interact with the User model.
    """

    @staticmethod
    def get_task_by_id(id: int) -> Task:
        """
        Get task by id.
        :param id: task id
        :return: task
        """
        return Task.query.filter_by(id=id).first()

    @staticmethod
    def get_all_tasks() -> list[Task]:
        """
        Get all tasks.

        :return: tasks
        """
        return Task.query.all()

    @staticmethod
    def create_task(name: str, priority: int) -> Task:
        """
        Create and insert a new task.

        :param name: name of the task
        :param priority: priority of the task
        :return: task
        """
        task = Task(name=name, priority=priority)
        db.session.add(task)
        db.session.commit()
        return task

    @staticmethod
    def update_task_by_id(id: int, name: str, priority: int) -> Task:
        """
        Update existing task.

        :param id: task id
        :param name: new name for the task
        :param priority: new priority for the task
        :return: updated task if task exists, None otherwise
        """
        task = db.session.get(Task, id)
        if not task:
            return None
        task.name = name
        task.priority = priority
        db.session.commit()
        return task

    @staticmethod
    def delete_task_by_id(id: int) -> bool:
        """
        Delete a task by id.

        :param id: task id
        :return: True if task exists and is deleted, False otherwise
        """
        task = db.session.get(Task, id)
        if not task:
            return False
        db.session.delete(task)
        db.session.commit()
        return True

    @staticmethod
    def delete_all_tasks() -> None:
        """
        Delete all tasks.

        :return: None
        """
        tasks = Task.query.all()
        for task in tasks:
            db.session.delete(task)
        db.session.commit()