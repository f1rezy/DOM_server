from .base import BaseModel

from database import db
from sqlalchemy.dialects.postgresql import BYTEA


class File(BaseModel):
    __tablename__ = "file"

    name = db.Column(db.VARCHAR(50))
    meta = db.Column(db.VARCHAR(20))
    data = db.Column(BYTEA())

    user_info = db.relationship("UserInfo", back_populates="icon")
    banner_event = db.relationship("Event", back_populates="banner")
    doc_event = db.relationship("Event", back_populates="docs")
    organization = db.relationship("Organization", back_populates="logo")
