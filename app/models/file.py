from .base import BaseModel

from database import db
from sqlalchemy.dialects.postgresql import BYTEA


class File(BaseModel):
    __tablename__ = "file"

    name = db.Column(db.TEXT)
    meta = db.Column(db.TEXT)
    data = db.Column(BYTEA())


