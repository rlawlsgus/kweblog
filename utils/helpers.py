# utils/helpers.py
import os
import re


def convert_urls_to_links(text):
    """URL을 하이퍼링크로 변환하는 함수"""
    if not text:
        return ""
    url_pattern = re.compile(r"https?://\S+")
    return url_pattern.sub(
        lambda m: f'<a href="{m.group(0)}" target="_blank">{m.group(0)}</a>', text
    )


def create_upload_folders(app):
    """업로드 폴더 생성 함수"""
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(os.path.join(app.config["UPLOAD_FOLDER"], "profiles"), exist_ok=True)
    os.makedirs(os.path.join(app.config["UPLOAD_FOLDER"], "posts"), exist_ok=True)
