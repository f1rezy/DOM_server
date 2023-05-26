from database import db
from .base import BaseModel


class EventStatus(BaseModel):
    __tablename__ = "event_status"

    name = db.Column(db.TEXT())
