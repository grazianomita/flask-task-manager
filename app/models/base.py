from app import db
from datetime import datetime

class BaseModel(db.Model):
    """
    Abstract model class that defines the fields shared by all the models.
    Fields are automatically generated, no need to specify them at creation time.
    """
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
