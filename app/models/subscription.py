from database import db
from .base import BaseModel

from sqlalchemy.dialects.postgresql import JSON, UUID


class Subscription(BaseModel):
    __tablename__ = "subscription"

    user_info_id = db.Column(db.ForeignKey("user_info.id"))
    # user_info_id = db.Column(UUID)
    filter = db.Column(JSON)

    user_info = db.relationship("UserInfo", back_populates="subscription")
