# routes/profile.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from database import db
from models.user import User
from models.post import Post
from utils.decorators import login_required
from utils.helpers import convert_urls_to_links
from datetime import datetime
import os

profile = Blueprint("profile", __name__)


@profile.route("/profile/<username>")
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user_id=user.id).order_by(Post.created_at.desc()).all()

    bio_with_links = convert_urls_to_links(user.bio)

    current_user = None
    if "user_id" in session:
        current_user = User.query.get(session["user_id"])

    return render_template(
        "profile.html",
        user=user,
        posts=posts,
        bio_with_links=bio_with_links,
        current_user=current_user,
    )


@profile.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    user = User.query.get_or_404(session["user_id"])

    if request.method == "POST":
        bio = request.form["bio"]

        # 프로필 사진 처리
        if "profile_pic" in request.files:
            file = request.files["profile_pic"]
            if file.filename != "":
                filename = secure_filename(file.filename)
                filename = f"{user.username}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
                file.save(
                    os.path.join(
                        profile.root_path,
                        "..",
                        "static",
                        "uploads",
                        "profiles",
                        filename,
                    )
                )

                # 기존 프로필 사진이 기본이 아니면 삭제
                if user.profile_pic != "default.jpg":
                    try:
                        os.remove(
                            os.path.join(
                                profile.root_path,
                                "..",
                                "static",
                                "uploads",
                                "profiles",
                                user.profile_pic,
                            )
                        )
                    except:
                        pass

                user.profile_pic = filename

        user.bio = bio
        db.session.commit()
        flash("프로필이 성공적으로 업데이트되었습니다.")
        return redirect(url_for("profile.user_profile", username=user.username))

    return render_template("edit_profile.html", user=user)


@profile.route("/friend/request/<int:user_id>")
@login_required
def request_friend(user_id):
    current_user = User.query.get(session["user_id"])
    target_user = User.query.get_or_404(user_id)

    success, message = current_user.send_friend_request(target_user)

    flash(message)
    return redirect(url_for("profile.user_profile", username=target_user.username))


@profile.route("/friend/remove/<int:user_id>")
@login_required
def remove_friend(user_id):
    current_user = User.query.get(session["user_id"])
    target_user = User.query.get_or_404(user_id)

    success, message = current_user.remove_friend(target_user)

    flash(message)
    return redirect(url_for("profile.user_profile", username=target_user.username))


@profile.route("/friend/accept/<int:user_id>")
@login_required
def accept_friend(user_id):
    current_user = User.query.get(session["user_id"])
    sender = User.query.get_or_404(user_id)

    success, message = current_user.accept_friend_request(sender)

    flash(message)
    return redirect(url_for("profile.user_profile", username=sender.username))


@profile.route("/friend/reject/<int:user_id>")
@login_required
def reject_friend(user_id):
    current_user = User.query.get(session["user_id"])
    sender = User.query.get_or_404(user_id)

    success, message = current_user.remove_friend(sender)

    flash(message)
    return redirect(url_for("profile.user_profile", username=sender.username))


@profile.route("/saved_posts")
@login_required
def saved_posts():
    user = User.query.get(session["user_id"])
    return render_template("saved_posts.html", posts=user.saved)
