import re

from flask import current_app, Response
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from flask_restx import Resource
from app.repositories.user_repository import UserRepository
from app.api.api_models import login_model
from app.api import ns


@ns.route("/register")
class UserRegistration(Resource):
    """
    Class implementing the UserRegistration resource.
    """

    @staticmethod
    def password_validator(password: str) -> None:
        """
        Password validation checks.

        :param password: password to be validated
        :return:
        """
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search("[a-z]", password):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search("[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search("[0-9]", password):
            raise ValueError("Password must contain at least one digit.")
        if not re.search("[^a-zA-Z0-9]", password):
            raise ValueError("Password must contain at least one symbol.")

    @ns.expect(login_model)
    def post(self) -> (Response, int):
        """
        Register a user.

        :return: message, status_code
        """
        try:
            self.password_validator(ns.payload['password'])
        except ValueError as e:
            msg = str(e)
            current_app.logger.error(msg)
            return {'message': msg}, 400
        if not UserRepository.create_user(ns.payload['username'], ns.payload['password']):
            msg = f'username {ns.payload["username"]} already exists'
            current_app.logger.error(msg)
            return {'message': msg}, 400
        msg = f'user {ns.payload["username"]} created successfully'
        current_app.logger.info(msg)
        return {'message': msg}, 201


@ns.route("/login")
class UserLogin(Resource):
    """
    Class implementing the UserLogin resource.
    """

    @ns.expect(login_model)
    def post(self) -> (Response, int):
        """
        Login.

        :return: error_message or access_token, status_code
        """
        user = UserRepository.get_user_by_username(ns.payload['username'])
        if not user or not user.check_password(ns.payload['password']):
            msg = 'invalid username or password'
            current_app.logger.error(msg)
            return {'message': msg}, 401
        access_token = create_access_token(identity=user.username)  # identity used to create the token
        refresh_token = create_refresh_token(identity=user.username)
        current_app.logger.info('successful login')
        return {'access_token': access_token, 'refresh_token': refresh_token}, 200


@ns.route("/refresh")
class TokenRefresh(Resource):
    """
    Class implementing the TokenRefresh resource.
    """

    @jwt_required(refresh=True)
    @ns.doc(security="jsonWebToken")
    def post(self) -> (Response, int):
        """
        Get a new access token.

        :return: message, status_code
        """
        current_user = get_jwt_identity()  # username -> identity extracted from the refresh token
        new_access_token = create_access_token(identity=current_user)
        current_app.logger.info('token refreshed')
        return {'access_token': new_access_token}, 200
