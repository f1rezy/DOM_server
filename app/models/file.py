from sqlalchemy.ext.associationproxy import association_proxy
from .base import BaseModel

from database import db
from sqlalchemy.dialects.postgresql import BYTEA


class File(BaseModel):
    __tablename__ = "file"

    name = db.Column(db.VARCHAR(50))
    data = db.Column(BYTEA())

    user_info = db.relationship("UserInfo", back_populates="icon")
    event_files = db.relationship("EventFile", back_populates="event")
    organization = db.relationship("Organization", back_populates="logo")

    events = association_proxy("event_files", "file")

