from .base import BaseModel

from database import db


class Level(BaseModel):
    __tablename__ = "level"

    name = db.Column(db.VARCHAR(20))

    events = db.relationship("Event", back_populates="level")

    @property
    def data(self):
        return {
            "id": self.id,
            "name": self.name
        }
