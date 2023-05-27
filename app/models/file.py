from .many_to_many_relations import *
from .base import BaseModel

from database import db
from sqlalchemy.dialects.postgresql import BYTEA


class File(BaseModel):
    __tablename__ = "file"

    name = db.Column(db.VARCHAR(50))
    meta = db.Column(db.VARCHAR(20))
    data = db.Column(BYTEA())

    user_info = db.relationship("UserInfo", back_populates="icon")
    event = db.relationship("Event", secondary=event_to_file, back_populates="files")
    organization = db.relationship("Organization", back_populates="logo")
