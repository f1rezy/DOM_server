from database import db
from .base import BaseModel


class OrganizationRoleUser(BaseModel):
    __tablename__ = "ogranization_role_user"

    user_id = db.Column(db.ForeignKey("user_info.id"))
    organization_id = db.Column(db.ForeignKey("organization.id"))
    organization_role_id = db.Column(db.ForeignKey("organization_role.id"))

    user_info = db.relationship("UserInfo", back_populates="organization_role_user")
    organization = db.relationship("Organization", back_populates="organization_role_user")
    organization_role = db.relationship("OrganizationRole", back_populates="organization_role_user")
