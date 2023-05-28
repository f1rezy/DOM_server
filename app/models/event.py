from database import db
from .base import BaseModel
from .many_to_many_relations import *


class Event(BaseModel):
    __tablename__ = "event"

    name = db.Column(db.VARCHAR(50))
    description = db.Column(db.TEXT())
    reg_form = db.Column(db.TEXT())
    online = db.Column(db.BOOLEAN(), default=True)
    fcdo = db.Column(db.BOOLEAN(), default=False)
    start_date = db.Column(db.DATE())
    end_date = db.Column(db.DATE(), nullable=True)
    level_id = db.Column(db.ForeignKey("level.id"))
    ages = db.Column(db.TEXT())
    organization_id = db.Column(db.ForeignKey('organization.id'))
    extra = db.Column(db.TEXT(), nullable=True)
    status_id = db.Column(db.ForeignKey('event_status.id'))
    origin = db.Column(db.TEXT(), nullable=True)

    level = db.relationship("Level", back_populates="events")
    organization = db.relationship("Organization", back_populates="events")
    files = db.relationship("File", secondary=event_to_file, back_populates="event")
    status = db.relationship("EventStatus", back_populates="events")

    users_info = db.relationship("UserInfo", secondary=event_to_user_info, back_populates="events")
    fields = db.relationship("Field", secondary=event_to_field, back_populates="events")

    @property
    def data(self):
        return {
            "name": self.name,
            "description": self.description,
            "region": self.organization.region.name,
            "city": self.organization.city.name,
            "address": self.organization.address,
            "reg_form": self.reg_form,
            "online": self.online,
            "fcdo": self.fcdo,
            "date": self.start_date.strftime('%d.%m.%y') + "-" + self.end_date.strftime(
                '%d.%m.%y') if self.end_date else self.start_date.strftime("%d.%m.%y"),
            "level": self.level.name,
            "ages": self.ages,
            "organization_id": self.organization_id,
            "organization_name": self.organization.full_name,
            "extra": self.extra,
            "status": self.status.name,
            "origin": self.origin,
            "fields": [str(field.name) for field in self.fields],
            "banner": ["/api/file/" + str(file.id) for file in filter(lambda x: x.type == "banner", self.files)][0],
            "docs": [{"name": str(file.name), "data": "/api/file/" + str(file.id)} for file in
                     filter(lambda x: x.type == "doc", self.files)],
            "organization_logo": "/api/file/" + str(self.organization.logo.name)
        }



