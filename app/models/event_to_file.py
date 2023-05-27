from database import db
from .base import BaseModel


class EventFile(BaseModel):
    __tablename__ = "event_to_file"

    type = db.Column(db.VARCHAR(20)),
    event_id = db.Column(db.ForeignKey("event.id")),
    file_id = db.Column(db.ForeignKey("file.id"))

    event = db.relationship("Event", back_populates="event_files")
    file = db.relationship("File", back_populates="event_files")
