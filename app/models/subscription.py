from database import db
from .base import BaseModel

from sqlalchemy.dialects.postgresql import JSON


class Subscription(BaseModel):
    __tablename__ = "event"

    user_info_id = db.Column(db.INTEGER(), db.ForeignKey('user_info.id'))
    user_info = db.relationship(back_populates="user_info")
    filter = db.Column(JSON())
