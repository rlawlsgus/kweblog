# routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from database import db, bcrypt
from models.user import User
from datetime import datetime
import os

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        bio = request.form["bio"]

        # 아이디 중복 체크
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("이미 사용 중인 아이디입니다.")
            return redirect(url_for("auth.register"))

        # 비밀번호 해싱
        hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")

        # 프로필 사진 처리
        profile_pic = "default.jpg"
        if "profile_pic" in request.files:
            file = request.files["profile_pic"]
            if file.filename != "":
                filename = secure_filename(file.filename)
                filename = (
                    f"{username}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
                )
                file.save(
                    os.path.join(
                        auth.root_path, "..", "static", "uploads", "profiles", filename
                    )
                )
                profile_pic = filename

        # 새 사용자 생성
        new_user = User(
            username=username, password=hashed_pw, bio=bio, profile_pic=profile_pic
        )
        db.session.add(new_user)
        db.session.commit()

        flash("회원가입이 완료되었습니다. 로그인하세요.")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            flash("로그인 성공!")
            return redirect(url_for("main.index"))
        else:
            flash("로그인 실패. 아이디 또는 비밀번호를 확인하세요.")

    return render_template("login.html")


@auth.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    flash("로그아웃되었습니다.")
    return redirect(url_for("main.index"))
