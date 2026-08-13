import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, "..", ".env"))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URI",
        "sqlite:///" + os.path.join(basedir, "..", "instance", "app.db"),
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
    AWS_REGION = os.environ.get("AWS_REGION", "ap-south-1")

    # Only used for local dev if IAM role isn't available. Leave blank on EC2.
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID") or None
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY") or None

    MAX_CONTENT_LENGTH = 25 * 1024 * 1024  # 25 MB upload limit
    ALLOWED_EXTENSIONS = {"pdf", "docx", "doc", "txt", "png", "jpg", "jpeg", "xlsx", "pptx"}
