from database import db
from .base import BaseModel


class Field(BaseModel):
    __tablename__ = "field"

    name = db.Column(db.TEXT())
