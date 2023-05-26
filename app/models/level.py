from .base import BaseModel

from database import db


class Level(BaseModel):
    __tablename__ = "level"

    name = db.Column(db.VARCHAR(20))


