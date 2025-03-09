# routes/main.py
from flask import Blueprint, render_template
from models.post import Post

main = Blueprint("main", __name__)


@main.route("/")
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("index.html", posts=posts)
