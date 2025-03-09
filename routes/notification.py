# routes/notification.py
from flask import Blueprint, render_template, jsonify, session
from database import db
from models.notification import Notification
from utils.decorators import login_required

notification = Blueprint("notification", __name__)


@notification.route("/notifications")
@login_required
def view_notifications():
    notifications = (
        Notification.query.filter_by(user_id=session["user_id"])
        .order_by(Notification.created_at.desc())
        .all()
    )

    # 알림을 읽음으로 표시
    for notif in notifications:
        if not notif.is_read:
            notif.is_read = True

    db.session.commit()

    return render_template("notifications.html", notifications=notifications)


@notification.route("/api/unread_notifications")
@login_required
def unread_notifications():
    count = Notification.query.filter_by(
        user_id=session["user_id"], is_read=False
    ).count()
    return jsonify({"count": count})
