from flask import Blueprint
from flask_restx import Api, Namespace


authorizations = {
    "jsonWebToken": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}

api_bp = Blueprint('api', __name__)
api = Api(api_bp)
ns = Namespace("api", authorizations=authorizations)
api.add_namespace(ns)

# Import and register resource classes
from app.api.resources.user import UserRegistration, UserLogin, TokenRefresh
from app.api.resources.task import TasksResource, TaskResource
ns.add_resource(UserRegistration, "/register")
ns.add_resource(UserLogin, "/login")
ns.add_resource(TokenRefresh, "/refresh")
ns.add_resource(TasksResource, "/tasks")
ns.add_resource(TaskResource, "/tasks/<int:task_id>")
