from .base import BaseModel

from database import db


class OrganizationRole(BaseModel):
    __tablename__ = "orgsmization_role"

    name = db.Column(db.TEXT)
