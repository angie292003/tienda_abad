import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask

from infrastructure.web_flask.routes import register_routes


BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")


def create_app():

    app = Flask(
        __name__,
        template_folder=str(BASE_DIR / "interface" / "templates"),
        static_folder=str(BASE_DIR / "interface" / "static")
    )

    app.secret_key = os.getenv("SECRET_KEY", "clave_desarrollo")

    register_routes(app)

    return app