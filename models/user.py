# models/user.py
from database import db
from models.notification import Notification
from models.associations import likes, saved_posts, friends


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    profile_pic = db.Column(db.String(200), nullable=True, default="default.jpg")
    bio = db.Column(db.Text, nullable=True)

    # 관계 설정
    posts = db.relationship("Post", backref="author", lazy=True)
    comments = db.relationship("Comment", backref="author", lazy=True)
    notifications = db.relationship("Notification", backref="user", lazy=True)
    liked_posts = db.relationship(
        "Post", secondary=likes, backref=db.backref("liked_by", lazy="dynamic")
    )
    saved = db.relationship(
        "Post", secondary=saved_posts, backref=db.backref("saved_by", lazy="dynamic")
    )
    friend_requests_sent = db.relationship(
        "User",
        secondary=friends,
        primaryjoin=(id == friends.c.user_id),
        secondaryjoin=(id == friends.c.friend_id),
        backref=db.backref("friend_requests_received", lazy="dynamic"),
        lazy="dynamic",
    )

    def __repr__(self):
        return f"<User {self.username}>"

    def send_friend_request(self, user):
        if user.id == self.id:
            return False, "자신에게 서로이웃 요청을 보낼 수 없습니다."

        if self.is_friend_with(user):
            return False, "이미 서로이웃 상태입니다."

        if self.has_pending_request_to(user):
            return False, "이미 서로이웃 요청을 보냈습니다."

        # 상대방이 나에게 보낸 요청이 있는지 확인
        existing_request = (
            db.session.query(friends)
            .filter(friends.c.user_id == user.id, friends.c.friend_id == self.id)
            .first()
        )

        if existing_request:
            # 상대방이 나에게 보낸 요청이 있으면 자동으로 수락
            self.accept_friend_request(user)
            return True, "서로이웃 요청이 수락되었습니다."

        # 새 요청 생성
        self.friend_requests_sent.append(user)
        db.session.commit()

        # 알림 생성
        notification = Notification(
            content=f"{self.username}님이 서로이웃 요청을 보냈습니다.",
            user_id=user.id,
            sender_id=self.id,
            type="friend_request",
        )
        db.session.add(notification)
        db.session.commit()

        return True, "서로이웃 요청을 보냈습니다."

    # 서로이웃 요청 수락
    def accept_friend_request(self, user):
        # 요청 상태를 'accepted'로 변경
        db.session.query(friends).filter(
            friends.c.user_id == user.id, friends.c.friend_id == self.id
        ).update({"status": "accepted"})

        # 양방향 관계 설정 (상대방이 아직 나에게 요청을 보내지 않았을 경우)
        existing_request = (
            db.session.query(friends)
            .filter(friends.c.user_id == self.id, friends.c.friend_id == user.id)
            .first()
        )

        if not existing_request:
            new_relation = friends.insert().values(
                user_id=self.id, friend_id=user.id, status="accepted"
            )
            db.session.execute(new_relation)
        else:
            db.session.query(friends).filter(
                friends.c.user_id == self.id, friends.c.friend_id == user.id
            ).update({"status": "accepted"})

        db.session.commit()

        # 알림 생성
        notification = Notification(
            content=f"{self.username}님이 서로이웃 요청을 수락했습니다.",
            user_id=user.id,
            type="friend_accepted",
            sender_id=self.id,
        )
        db.session.add(notification)
        db.session.commit()

        return True, "서로이웃 요청을 수락했습니다."

    # 서로이웃 요청 거절 또는 관계 해제
    def remove_friend(self, user):
        # 양방향 관계 모두 제거
        db.session.query(friends).filter(
            (friends.c.user_id == self.id) & (friends.c.friend_id == user.id)
        ).delete()

        db.session.query(friends).filter(
            (friends.c.user_id == user.id) & (friends.c.friend_id == self.id)
        ).delete()

        db.session.commit()
        return True, "서로이웃 관계가 해제되었습니다."

    # 서로이웃 상태 확인
    def is_friend_with(self, user):
        return (
            db.session.query(friends)
            .filter(
                friends.c.user_id == self.id,
                friends.c.friend_id == user.id,
                friends.c.status == "accepted",
            )
            .count()
            > 0
        )

    # 보낸 서로이웃 요청 확인 (대기 중)
    def has_pending_request_to(self, user):
        return (
            db.session.query(friends)
            .filter(
                friends.c.user_id == self.id,
                friends.c.friend_id == user.id,
                friends.c.status == "pending",
            )
            .count()
            > 0
        )

    # 받은 서로이웃 요청 확인 (대기 중)
    def has_pending_request_from(self, user):
        return (
            db.session.query(friends)
            .filter(
                friends.c.user_id == user.id,
                friends.c.friend_id == self.id,
                friends.c.status == "pending",
            )
            .count()
            > 0
        )
