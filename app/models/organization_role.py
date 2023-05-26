from .base import BaseModel

from database import db


class OrganizationRole(BaseModel):
    __tablename__ = "organization_role"

    name = db.Column(db.TEXT)

    organization_role_user = db.relationship("OrganizationRoleUser", back_populates="organization_role")
