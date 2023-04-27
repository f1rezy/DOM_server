import json

from werkzeug.security import generate_password_hash, check_password_hash

from database import db
from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    username = db.Column(db.VARCHAR(80))
    name = db.Column(db.VARCHAR(80))
    password_hash = db.Column(db.String(128))

    @property
    def data(self):
        return {
            "username": self.username,
            "name": self.name,
        }

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
