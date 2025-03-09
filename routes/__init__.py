# routes/__init__.py
from routes.main import main
from routes.auth import auth
from routes.post import post
from routes.profile import profile
from routes.notification import notification


def register_blueprints(app):
    """애플리케이션에 블루프린트 등록"""
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(post)
    app.register_blueprint(profile)
    app.register_blueprint(notification)
