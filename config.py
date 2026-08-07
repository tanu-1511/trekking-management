import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "this-will-be-changed-later"

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" + os.path.join(BASE_DIR, "instance", "trekking.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False