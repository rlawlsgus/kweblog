# routes/post.py
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    jsonify,
)
from werkzeug.utils import secure_filename
from database import db
from models.post import Post
from models.user import User
from models.comment import Comment
from models.notification import Notification
from utils.decorators import login_required
from datetime import datetime
import os

post = Blueprint("post", __name__)


@post.route("/new_post", methods=["GET", "POST"])
@login_required
def new_post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        # 이미지 처리
        image_filename = None
        if "image" in request.files:
            file = request.files["image"]
            if file.filename != "":
                filename = secure_filename(file.filename)
                filename = f"post_{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
                file.save(
                    os.path.join(
                        post.root_path, "..", "static", "uploads", "posts", filename
                    )
                )
                image_filename = filename

        # 새 게시물 생성
        new_post = Post(
            title=title,
            content=content,
            image=image_filename,
            user_id=session["user_id"],
        )

        db.session.add(new_post)
        db.session.commit()

        flash("게시물이 성공적으로 작성되었습니다.")
        return redirect(url_for("main.index"))

    return render_template("new_post.html")


@post.route("/post/<int:post_id>")
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)

    # 사용자가 로그인했는지 확인
    if "user_id" in session:
        user = User.query.get(session["user_id"])
        current_user = {"saved": user.saved, "liked_posts": user.liked_posts}
    else:
        current_user = {"saved": [], "liked_posts": []}
    return render_template("post_detail.html", post=post, current_user=current_user)


@post.route("/post/<int:post_id>/comment", methods=["POST"])
@login_required
def add_comment(post_id):
    post_item = Post.query.get_or_404(post_id)
    content = request.form["content"]

    # 새 댓글 생성
    new_comment = Comment(content=content, user_id=session["user_id"], post_id=post_id)

    db.session.add(new_comment)

    # 게시물 작성자에게 알림 전송 (자신의 게시물에 자신이 댓글을 단 경우는 제외)
    if post_item.user_id != session["user_id"]:
        notification = Notification(
            content=f"{session['username']}님이 회원님의 게시물에 댓글을 남겼습니다.",
            user_id=post_item.user_id,
            type="comment",
            post_id=post_id,
            sender_id=session["user_id"],
        )
        db.session.add(notification)

    db.session.commit()

    flash("댓글이 성공적으로 작성되었습니다.")
    return redirect(url_for("post.post_detail", post_id=post_id))


@post.route("/post/<int:post_id>/like", methods=["POST"])
@login_required
def like_post(post_id):
    post_item = Post.query.get_or_404(post_id)
    user = User.query.get(session["user_id"])

    # 이미 좋아요를 눌렀는지 확인
    if post_item in user.liked_posts:
        user.liked_posts.remove(post_item)
        liked = False
    else:
        user.liked_posts.append(post_item)
        liked = True

        # 자신의 게시물에 자신이 좋아요를 누른 경우를 제외하고 알림 생성
        if post_item.user_id != session["user_id"]:
            notification = Notification(
                content=f"{session['username']}님이 회원님의 게시물을 좋아합니다.",
                user_id=post_item.user_id,
                type="like",
                post_id=post_id,
                sender_id=session["user_id"],
            )
            db.session.add(notification)

    db.session.commit()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify(
            {"status": "success", "liked": liked, "count": post_item.liked_by.count()}
        )
    else:
        return redirect(url_for("post.post_detail", post_id=post_id))


@post.route("/post/<int:post_id>/save", methods=["POST"])
@login_required
def save_post(post_id):
    post_item = Post.query.get_or_404(post_id)
    user = User.query.get(session["user_id"])

    # 이미 저장했는지 확인
    if post_item in user.saved:
        user.saved.remove(post_item)
        saved = False
    else:
        user.saved.append(post_item)
        saved = True

    db.session.commit()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"status": "success", "saved": saved})
    else:
        return redirect(url_for("post.post_detail", post_id=post_id))
