from app import db
from app.models.base import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash


class User(BaseModel):
    """
    User model. It inherits from BaseModel.
    """
    __tablename__ = "user"

    username = db.Column(db.String(32), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password: str):
        """
        It generates a password hash.

        :param password: plaintext password
        :return: None
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        It compares a password with its hash.

        :param password: plaintext password to be checked
        :return: True if the provided password matches the stored password hash, False otherwise
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """
        String representation of User.

        :return: 'User <id> - username: <username>'
        """
        return f'User {self.id} - username: {self.username}'

    def __eq__(self, other):
        """
        Check if two objects are equal.

        :param other: other object
        :return: True if username, password and date fields are the same, False otherwise
        """
        if not isinstance(other, User):
            return False
        return self.username == other.username
