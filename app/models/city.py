from .base import BaseModel

from database import db


class City(BaseModel):
    __tablename__ = "city"

    name = db.Column(db.VARCHAR(50))

    organization = db.relationship("Organization", back_populates="city")


