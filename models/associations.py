# models/associations.py
from database import db
from datetime import datetime

# 좋아요 관계 테이블
likes = db.Table(
    "likes",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("post_id", db.Integer, db.ForeignKey("post.id"), primary_key=True),
)

# 저장된 게시물 관계 테이블
saved_posts = db.Table(
    "saved_posts",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("post_id", db.Integer, db.ForeignKey("post.id"), primary_key=True),
)

# 서로이웃 관계 테이블
friends = db.Table(
    "friends",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("friend_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column(
        "status", db.String(20), nullable=False, default="pending"
    ),  # pending, accepted
    db.Column("created_at", db.DateTime, nullable=False, default=datetime.now),
)
