from .base import BaseModel

from database import db


class Organization(BaseModel):
    __tablename__ = "organization"

    short_name = db.Column(db.VARCHAR(30))
    full_name = db.Column(db.VARCHAR(255))
    address = db.Column(db.VARCHAR(255))
    tax_number = db.Column(db.VARCHAR(10))
    email = db.Column(db.VARCHAR(50))
    site = db.Column(db.TEXT)
    confirmed = db.Column(db.BOOLEAN, default=False)
    logo_id = db.Column(db.ForeignKey("file.id"))
    region_id = db.Column(db.ForeignKey("region.id"))
    city_id = db.Column(db.ForeignKey("city.id"))

    logo = db.relationship("File", back_populates="organization")
    region = db.relationship("Region", back_populates="organization")
    city = db.relationship("City", back_populates="organization")
    user_info = db.relationship("UserInfo", back_populates="organization")
    events = db.relationship("Event", back_populates="organization")
    organization_role_user = db.relationship("OrganizationRoleUser", back_populates="organization")

