from .base import BaseModel

from database import db


class Region(BaseModel):
    __tablename__ = "region"

    name = db.Column(db.VARCHAR(30))

    organization = db.relationship(back_populates="region")