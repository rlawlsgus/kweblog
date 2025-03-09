# models/notification.py
from database import db
from datetime import datetime


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    is_read = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    type = db.Column(
        db.String(20), nullable=False
    )  # comment, like, friend_request, friend_accepted
    post_id = db.Column(db.Integer, nullable=True)  # 관련 게시물 ID
    sender_id = db.Column(db.Integer, nullable=True)  # 알림을 보낸 사용자 ID

    def __repr__(self):
        return f"<Notification {self.id}>"
