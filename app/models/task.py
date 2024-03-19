from app import db
from app.models.base import BaseModel


class Task(BaseModel):
    """
    Task model. It inherits from BaseModel.
    """
    __tablename__ = "task"

    name = db.Column(db.String(255), nullable=False)
    priority = db.Column(db.Integer, nullable=False, default=1)
    # description = db.Column(db.String(255))

    def __repr__(self):
        """
        String representation of Task.

        :return: 'Task <id> - name: <name>, priority: <priority>, created_at: <created_at>, updated_at: <updated_at>'
        """
        return f'Task {self.id} - name: {self.name}, priority: {self.priority}, ' \
               f'created_at: {self.created_at}, updated_at: {self.updated_at}'

    def __eq__(self, other):
        """
        Check if two objects are equal.

        :param other: other object
        :return: True if name, password and date fields are the same, False otherwise
        """
        if not isinstance(other, Task):
            return False
        return self.name == other.name and self.priority == other.priority \
            and self.created_at == other.created_at and self.updated_at == other.updated_at
