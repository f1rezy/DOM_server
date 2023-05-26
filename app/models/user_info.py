from werkzeug.security import generate_password_hash, check_password_hash

from database import db
from .base import BaseModel


class UserInfo(BaseModel):
    __tablename__ = "user_info"

    email = db.Column(db.TEXT())
    first_name = db.Column(db.TEXT())
    last_name = db.Column(db.TEXT())
    second_name = db.Column(db.TEXT())
    region_id = db.Column(db.INTEGER())
    city_id = db.Column(db.INTEGER())
    phone = db.Column(db.TEXT())
    password = db.Column(db.String(128))
    organization_id = db.Column(db.ForeignKey("organization.id"))
    role_id = db.Column(db.INTEGER(), db.ForeignKey("role.id"))
    subscription_id = db.Column(db.ForeignKey('subscription.id'))
    phone_public = db.Column(db.BOOLEAN(), default=False)
    icon_id = db.Column(db.ForeignKey('file.id'))
    email_confirmed = db.Column(db.BOOLEAN(), default=False)
    phone_confirmed = db.Column(db.BOOLEAN(), default=False)

    organization = db.relationship("Organization", back_populates="user_info")
    role = db.relationship("Role", back_populates="users_info")
    subscription = db.relationship("Subscription", back_populates="user_info")
    icon = db.relationship("File", back_populates="user_info")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
