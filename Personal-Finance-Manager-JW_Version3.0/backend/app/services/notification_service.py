from sqlalchemy.orm import Session
from ..models.notificationModel import Notification
from ..schemas.notificationSchema import NotificationCreate, NotificationUpdate, NotificationType
from ..models.budgetModel import Budget
from ..models.userModel import User
from datetime import datetime


def create_notification(user_id: int, notification: NotificationCreate, db: Session):
    db_notification = Notification(
        user_id=user_id,
        type=notification.type,
        title=notification.title,
        message=notification.message,
        is_read=notification.is_read,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification


def get_notifications(user_id: int, db: Session):
    return db.query(Notification).filter(Notification.user_id == user_id).all()


def update_notification(notification_id: int, notification_update: NotificationUpdate, db: Session):
    db_notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if db_notification:
        if notification_update.is_read is not None:
            db_notification.is_read = notification_update.is_read
        db_notification.updated_at = datetime.now()
        db.commit()
        db.refresh(db_notification)
        return db_notification
    return None


def delete_notification(notification_id: int, db: Session):
    db_notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if db_notification:
        db.delete(db_notification)
        db.commit()
        return db_notification
    return None
