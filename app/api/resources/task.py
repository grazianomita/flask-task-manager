from flask import current_app, Response, abort
from flask_restx import Resource
from flask_jwt_extended import jwt_required
from app import limiter
from app.repositories.task_repository import TaskRepository
from app.api.api_models import task_model, task_post_model
from app.api import ns


@ns.route("/tasks")
class TasksResource(Resource):
    """
    Class implementing the Tasks resource.
    """

    @jwt_required()
    @ns.doc(security="jsonWebToken")
    @ns.marshal_list_with(task_model)
    def get(self) -> (Response, int):
        """
        Get all tasks.

        :return: list of tasks, status_code
        """
        tasks = TaskRepository.get_all_tasks()
        msg = 'all tasks returned'
        current_app.logger.info(msg)
        return tasks, 200

    @jwt_required()
    @ns.doc(security="jsonWebToken")
    @ns.expect(task_post_model)
    @ns.marshal_with(task_model)
    @limiter.limit('1 per 10 second')
    def post(self) -> (Response, int):
        """
        Create a new task.

        :return: task, status_code
        """
        task = TaskRepository.create_task(ns.payload["name"], ns.payload["priority"])
        msg = f'task {task.id} successfully created'
        current_app.logger.info(msg)
        return task, 201

    @jwt_required()
    @ns.doc(security="jsonWebToken")
    def delete(self) -> (Response, int):
        """
        Delete all tasks.

        :return: message, status_code
        """
        TaskRepository.delete_all_tasks()
        msg = 'all tasks deleted'
        current_app.logger.info(msg)
        return {}, 204


@ns.route("/tasks/<int:task_id>")
class TaskResource(Resource):
    """
    Class implementing the Task resource.
    """

    @jwt_required()
    @ns.doc(security="jsonWebToken")
    @ns.marshal_with(task_model)
    def get(self, task_id: int) -> (Response, int):
        """
        Get task by task_id.

        :param task_id: task id
        :return: task, status_code
        """
        task = TaskRepository.get_task_by_id(task_id)
        if task is None:
            # return {'message': f'task {task_id} not found'}, 404  @marshal_with would return a task with all nulls
            msg = f'task {task_id} not found'
            current_app.logger.warning(msg)
            abort(404, msg)
        current_app.logger.info(f'get task {task_id}')
        return task, 200

    @jwt_required()
    @ns.doc(security="jsonWebToken")
    @ns.expect(task_post_model)
    @limiter.limit('1 per 10 second')
    def put(self, task_id: int) -> (Response, int):
        """
        Update a task by id.

        :param task_id: task id
        :return: message, status_code
        """
        task = TaskRepository.update_task_by_id(task_id, ns.payload["name"], ns.payload["priority"])
        if task is None:
            msg = f'task {task_id} not found'
            current_app.logger.warning(msg)
            return {'message': msg}, 404
        msg = f'task {task_id} updated'
        current_app.logger.info(msg)
        return {'message': msg}, 200

    @jwt_required()
    @ns.doc(security="jsonWebToken")
    def delete(self, task_id: int) -> (Response, int):
        """
        Delete a task by id.

        :param task_id: task id
        :return: message, status_code
        """
        if not TaskRepository.delete_task_by_id(task_id):
            # return {'message': f'task {task_id} not found'}, 404
            msg = f'task {task_id} not found'
            current_app.logger.warning(msg)
            abort(404, f'task {task_id} not found')
        msg = f'task {task_id} deleted'
        current_app.logger.info(msg)
        return {}, 204
