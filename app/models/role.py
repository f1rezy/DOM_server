from .base import BaseModel

from database import db


class Role(BaseModel):
    __tablename__ = "role"

    name = db.Column(db.VARCHAR(20))

