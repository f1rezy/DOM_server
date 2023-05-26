from database import db
from .base import BaseModel


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
    user_info_id = db.Column(db.INTEGER(), db.ForeignKey())
    organization_id = db.Column(db.ForeignKey('organization.id'))
    extra = db.Column(db.TEXT(), nullable=True)
    banner_id = db.Column(db.ForeignKey('file.id'))
    doc_id = db.Column(db.ForeignKey('file.id'))
    field_id = db.Column(db.ForeignKey('????.id'))
    status_id = db.Column(db.ForeignKey('event_status.id'))
    origin = db.Column(db.TEXT(), nullable=True)

    level = db.relationship("Level", back_populates="events")
    organization = db.relationship("Organization", back_populates="events")
    banner = db.relationship("File", back_populates="banner_event")
    docs = db.relationship("File", back_populates="doc_event")
    status = db.relationship("EventStatus", back_populates="events")
