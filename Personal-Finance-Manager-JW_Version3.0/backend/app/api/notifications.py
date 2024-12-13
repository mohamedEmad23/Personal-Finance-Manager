from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from ..schemas.notificationSchema import NotificationCreate, NotificationUpdate
from ..services.notification_service import create_notification, get_notifications, update_notification, \
    delete_notification
from ..core.database import get_db

notification_router = APIRouter()


@notification_router.post("/notifications/", status_code=status.HTTP_201_CREATED)
def create_notification_endpoint(user_id: int, notification: NotificationCreate, db: Session = Depends(get_db)):
    return create_notification(user_id, notification, db)


@notification_router.get("/notifications/")
def list_notifications(user_id: int, db: Session = Depends(get_db)):
    notifications = get_notifications(user_id, db)
    if not notifications:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No notifications found for the user")
    return notifications


@notification_router.put("/notifications/{notification_id}/")
def update_notification_endpoint(notification_id: int, notification_update: NotificationUpdate,
                                 db: Session = Depends(get_db)):
    db_notification = update_notification(notification_id, notification_update, db)
    if not db_notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    return db_notification


@notification_router.delete("/notifications/{notification_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification_endpoint(notification_id: int, db: Session = Depends(get_db)):
    db_notification = delete_notification(notification_id, db)
    if not db_notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
