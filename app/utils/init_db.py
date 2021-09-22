import uuid
import requests
import logging
from random import randint

from app.db.database import SessionLocal
from app.models.notifications import (
    Notification,
    NotificationSender,
    NotificationTypeEnum,
    NotificationActionEnum,
    NotificationStatusEnum
)
from app.crud.notifications import BaseCrudProvider


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

notification_sender_crud = BaseCrudProvider(NotificationSender)
notification_crud = BaseCrudProvider(Notification)
db = SessionLocal()


def init_db():
    users_created = 0
    notification_created = 0
    user_error_counter = 0
    notification_error_counter = 0

    users_request_url = 'https://randomuser.me/api/?results=25'
    req = requests.get(users_request_url).json()

    results = req.get('results')

    if not results:
        logger.warning("Error occurred while creating users")

    for result in results:
        try:
            name = result['name']
            user_data = {
                'name': f'{name["title"]} {name["first"]} {name["last"]}',
                'id': result['login']['uuid'],
                'avatar': result['picture']['thumbnail']
            }
            user = notification_sender_crud.create(db, user_data)
            users_created += 1
            logger.warning(f"user created")

            for i in range(randint(1, 10)):
                try:
                    notification_data = {
                        "message": "test message",
                        "params": {},
                        "notification_type": NotificationTypeEnum.enums[0],
                        "action": NotificationActionEnum.enums[0],
                        "status": NotificationStatusEnum.enums[0],
                        "id": uuid.uuid1(),
                        "sender_id": user.id
                    }
                    notification_crud.create(db, notification_data)
                    notification_created += 1
                except Exception as e:
                    logger.warning(f">>>>> {e}")
                    notification_error_counter += 1

        except Exception as e:
            logger.warning(f">>>>> {e}")
            user_error_counter += 1

    logger.warning(f"user created count {users_created}")
    logger.warning(f"user creation error counter {user_error_counter}")
    logger.warning(f"notification created count {notification_created}")
    logger.warning(f"notification creation error counter {notification_error_counter}")
