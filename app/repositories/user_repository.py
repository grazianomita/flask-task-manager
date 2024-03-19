from app.models.user import User
from app import db


class UserRepository:
    """
    Class to interact with the User model.
    """

    @staticmethod
    def get_user_by_username(username: str) -> User:
        """
        Get user by username.

        :param username: username of the user
        :return: user
        """
        return User.query.filter_by(username=username).first()

    @staticmethod
    def create_user(username: str, password: str) -> bool:
        """
        Create and register a user.

        :param username: username
        :param password: plaintext password
        :return:
        """
        if User.query.filter_by(username=username).first():
            return False
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return True
