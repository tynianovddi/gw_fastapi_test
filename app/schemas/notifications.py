import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, validator

from ..models.notifications import (
    NotificationTypeEnum,
    NotificationStatusEnum,
    NotificationActionEnum
)


class NotificationSender(BaseModel):
    id: Optional[uuid.UUID] = None
    name: str
    avatar: Optional[str] = None

    class Config:
        orm_mode = True


class Notification(BaseModel):
    id: Optional[uuid.UUID] = None
    notification_type: str
    action: str
    status: str
    sent_at: Optional[datetime] = None
    viewed_at: Optional[datetime] = None
    sender: Optional[NotificationSender] = None
    sender_id: Optional[uuid.UUID] = None
    message: str

    @validator('notification_type')
    def notification_type_check(cls, v):
        if v not in NotificationTypeEnum.enums:
            raise ValueError("Invalid notification_type")
        return v

    @validator('action')
    def notification_action_check(cls, v):
        if v not in NotificationActionEnum.enums:
            raise ValueError("Invalid notification action")
        return v

    @validator('status')
    def notification_status_check(cls, v):
        if v not in NotificationStatusEnum.enums:
            raise ValueError("Invalid notification status")
        return v

    class Config:
        orm_mode = True
        use_enum_values = True
