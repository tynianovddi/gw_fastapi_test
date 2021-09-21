from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page, paginate

from app.crud.notifications import BaseCrudProvider
from app.models.notifications import Notification
from app.schemas.notifications import Notification as NotificationSchema
from app.db.database import SessionLocal


router = APIRouter()
notifications_crud = BaseCrudProvider(Notification)
db = SessionLocal()

# psql -U postgres -W -d app


@router.get("/notification/{notification_id}")
def get_notification_by_id(notification_id):
    return notifications_crud.get_by_id(db, notification_id)


@router.delete("/notification/{notification_id}")
def delete_notification_by_id(notification_id):
    return notifications_crud.delete_by_id(db, notification_id)


@router.put("/notification/{notification_id}")
def update_notification_by_id(notification_id, updated_obj: NotificationSchema):
    obj = notifications_crud.get_by_id(db, notification_id)
    return notifications_crud.update(db, obj, updated_obj)


@router.post("/notification")
def create_notification(updated_obj: NotificationSchema):
    return notifications_crud.create(db, updated_obj)


@router.get("/notification", response_model=Page[NotificationSchema])
def list_notification(order_by=None):
    return paginate(notifications_crud.get_all(db, order_by_field=order_by))
