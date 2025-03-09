# app.py
from flask import Flask
from database import db, migrate, bcrypt
from routes import register_blueprints
from dotenv import load_dotenv
from utils.helpers import create_upload_folders
import os


def create_app():
    app = Flask(
        __name__,
        static_folder="./static",
        template_folder="./templates",
    )

    load_dotenv()

    # 설정
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["UPLOAD_FOLDER"] = "static/uploads"
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

    # 데이터베이스 초기화
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # 파일 업로드를 위한 폴더 생성
    create_upload_folders(app)

    # 블루프린트 등록
    register_blueprints(app)

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
