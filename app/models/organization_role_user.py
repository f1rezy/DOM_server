from database import db


class OrganizationRoleUser(db.Model):
    __tablename__ = "ogranization_role_user"

    user_id = db.Column(db.ForeignKey("user.id"))
    organization_id = db.Column(db.ForeignKey("organization.id"))
    organization_role_id = db.Column(db.ForeignKey("organization_role.id"))

    user = db.relationship("UserInfo", back_populates="organization_role_user")
    organization = db.relationship("Organization", back_populates="organization_role_user")
    organization_role = db.relationship("OrganizationRole", back_populates="organization_role_user")
