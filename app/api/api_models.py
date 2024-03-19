from flask_restx import fields
from app.api import api


user_model = api.model("User", {
    'id': fields.Integer,
    'username': fields.String,
    'password': fields.String,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime
})

login_model = api.model("Login", {
    'username': fields.String(required=True, description='Username cannot be blank'),
    'password': fields.String(required=True, description='Password cannot be blank')
})

task_model = api.model("Task", {
    'id': fields.Integer,
    'name': fields.String,
    'priority': fields.Integer,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime
})

task_post_model = api.model("TaskPost", {
    'name': fields.String(required=True, description='Name cannot be blank'),
    'priority': fields.Integer(required=False, description='Priority is optional (default=1)', default=1)
})
