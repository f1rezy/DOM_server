from database import db
from .base import BaseModel
from .many_to_many_relations import event_to_field


class Field(BaseModel):
    __tablename__ = "field"

    name = db.Column(db.TEXT())

    events = db.relationship("Event", secondary=event_to_field, back_populates="fields")
