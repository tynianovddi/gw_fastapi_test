import datetime
import uuid
from json import dumps
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..db.database import Base, SessionLocal
from ..core.config import settings
from ..main import app
from ..models.notifications import (
    NotificationSender,
    Notification,
    NotificationStatusEnum,
    NotificationTypeEnum,
    NotificationActionEnum,
)
from ..crud.notifications import BaseCrudProvider

db = SessionLocal()
sender_crud = BaseCrudProvider(NotificationSender)
notification_crud = BaseCrudProvider(Notification)

engine = create_engine(
    settings.DATABASE_URI,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)
test_db = TestingSessionLocal()


def override_get_db():
    try:
        _db = TestingSessionLocal()
        yield _db
    finally:
        _db.close()


app.dependency_overrides[db] = override_get_db
db = TestingSessionLocal()
client = TestClient(app)

NOTIFICATION_DATA = {
    "id": str(uuid.uuid1()),
    "message": "test message",
    "params": {},
    "sender_id": str(db.query(NotificationSender).first().id),
    "notification_type": NotificationTypeEnum.enums[0],
    "action": NotificationActionEnum.enums[0],
    "status": NotificationStatusEnum.enums[0],
}

# @pytest.fixture
# def test_sender():
#     return sender_crud.create(db, {
#         "id": uuid.uuid1(),
#         "name": "name",
#         "avatar": "avatar"
#     })
#
#
# @pytest.fixture
# def test_notification(test_sender):
#     return notification_crud.create(db, {
#         "id": uuid.uuid1(),
#         "message": "test message",
#         "params": {},
#         "sender_id": test_sender.id,
#         "notification_type": NotificationTypeEnum.enums[0],
#         "action": NotificationActionEnum.enums[0],
#         "status": NotificationStatusEnum.enums[0],
#     })


def test_list_all_notifications():
    response = client.get('/api/v1/notification')
    assert response.status_code == 200
    assert db.query(Notification).count() == response.json()['total']


def test_list_all_notifications_with_invalid_url():
    response = client.get('/api/v1/notificationdsfsfsdfsf')
    assert response.status_code == 404


def test_get_notification_by_id():
    first_notification = db.query(Notification).first()
    response = client.get(f'/api/v1/notification/{first_notification.id}')
    assert response.status_code == 200
    data = response.json()
    for key, value in data.items():
        if isinstance(getattr(first_notification, key), datetime.datetime):
            assert value == getattr(first_notification, key).isoformat()
        elif isinstance(getattr(first_notification, key), uuid.UUID):
            assert value == str(getattr(first_notification, key))
        else:
            assert value == getattr(first_notification, key)


def test_get_notification_by_invalid_id():
    first_notification = db.query(Notification).first()
    response = client.get(f'/api/v1/notification/{first_notification.id}+error')
    assert response.status_code == 404


# def test_delete_notification_by_id():
#     count_before = db.query(Notification).count()
#     first_notification = db.query(Notification).first()
#     response = client.delete(f'/api/v1/notification/{first_notification.id}')
#     print(response.json())
#     assert response.status_code == 200
#     assert db.query(Notification).filter(Notification.id == first_notification.id).count() == 0
#     assert db.query(Notification).count() == count_before - 1


def test_delete_notification_by_invalid_id():
    count_before = db.query(Notification).count()
    first_notification = db.query(Notification).first()
    response = client.delete(f'/api/v1/notification/{first_notification.id}+error')
    assert response.status_code == 404
    assert db.query(Notification).filter(Notification.id == first_notification.id).count() == 1
    assert db.query(Notification).count() == count_before


# def test_create_notification_with_valid_data():
#     count_before = db.query(Notification).count()
#     response = client.post('/api/v1/notification', json=NOTIFICATION_DATA)
#     print(response.text)
#     assert response.status_code == 200
#     assert db.query(Notification).count() == count_before + 1


def test_create_notification_with_invalid_data():
    count_before = db.query(Notification).count()
    del NOTIFICATION_DATA['id']
    response = client.post('/api/v1/notification', json=NOTIFICATION_DATA)
    assert response.status_code == 400
    assert db.query(Notification).count() == count_before


def test_update_notification_with_invalid_id():
    first_notification = db.query(Notification).first()
    response = client.put(f'/api/v1/notification/{first_notification.id}+error', data=dumps(NOTIFICATION_DATA))
    assert response.status_code == 404


def test_update_notification_with_valid_id():
    first_notification = db.query(Notification).first()
    NOTIFICATION_DATA['message'] = 'message_to_test'
    NOTIFICATION_DATA['id'] = str(uuid.uuid1())
    response = client.put(f'/api/v1/notification/{first_notification.id}', data=dumps(NOTIFICATION_DATA))
    print(response.text)
    assert response.status_code == 200
    assert first_notification.id == NOTIFICATION_DATA['id']
    for key, value in NOTIFICATION_DATA.items():
        if isinstance(getattr(first_notification, key), datetime.datetime):
            assert value == getattr(first_notification, key).isoformat()
        elif isinstance(getattr(first_notification, key), uuid.UUID):
            assert value == str(getattr(first_notification, key))
        else:
            assert value == getattr(first_notification, key)

