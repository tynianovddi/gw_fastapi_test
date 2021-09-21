import enum
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)
from sqlalchemy.orm import relationship

from app.db.database import Base
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.dialects.postgresql.json import JSONB


NOTIFICATION_TYPES = (
    'Error',
    'Info',
    'Success',
    'Warning',
)


NOTIFICATION_ACTIONS = (
    'ListCreated',
    'ListRemoved',
    'InvitationAccepted',
    'InvitationDeclined',
)


NOTIFICATION_STATUSES = (
    'New',
    'Deleted',
    'Viewed',
    'Archived',
)


NotificationTypeEnum = ENUM(*NOTIFICATION_TYPES, name='notification_types', create_type=False)

NotificationStatusEnum = ENUM(*NOTIFICATION_STATUSES, name='notification_statuses', create_type=False)

NotificationActionEnum = ENUM(*NOTIFICATION_STATUSES, name='notification_actions', create_type=False)


class NotificationSender(Base):
    __tablename__ = "notification_senders"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
    )
    name = Column(String)
    avatar = Column(String)
    notifications = relationship(
        "Notification",
        back_populates="sender",
    )


class Notification(Base):
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
    )
    notification_type = Column(NotificationTypeEnum)
    action = Column(NotificationActionEnum)
    status = Column(NotificationStatusEnum)
    sent_at = Column(DateTime, default=datetime.utcnow)
    viewed_at = Column(DateTime, default=datetime.utcnow)
    sender_id = Column(UUID, ForeignKey('notification_senders.id'))
    sender = relationship(
        "NotificationSender",
        back_populates="notifications",
    )
    message = Column(String)
    params = Column(JSONB)
