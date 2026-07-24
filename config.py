import os
from datetime import timedelta

from flask_mail import Mail
from dotenv import load_dotenv

mail = Mail()

load_dotenv()


class Config:

    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    JWT_COOKIE_SECURE = os.getenv(
        "JWT_COOKIE_SECURE",
        "true"
    ).lower() == "true"

    JWT_COOKIE_SAMESITE = "Lax"
    JWT_COOKIE_CSRF_PROTECT = True

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        hours=int(os.getenv("JWT_ACCESS_TOKEN_HOURS", "8"))
    )

    # ==========================================
    # BANCO
    # ==========================================

    if os.getenv("DATABASE_URL"):

        database_url = os.getenv("DATABASE_URL")

        print("====================================")
        print("✅ PostgreSQL detectado")
        print("DATABASE_URL:", database_url)
        print("====================================")

        if database_url.startswith("postgres://"):

            database_url = database_url.replace(
                "postgres://",
                "postgresql+psycopg2://",
                1
            )

        elif database_url.startswith("postgresql://"):

            database_url = database_url.replace(
                "postgresql://",
                "postgresql+psycopg2://",
                1
            )

        SQLALCHEMY_DATABASE_URI = database_url

    else:

        print("====================================")
        print("✅ MySQL Local")
        print("====================================")

        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{os.getenv('DB_USER')}:"
            f"{os.getenv('DB_PASSWORD')}@"
            f"{os.getenv('DB_HOST')}:"
            f"{os.getenv('DB_PORT')}/"
            f"{os.getenv('DB_NAME')}"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    # ==========================================
    # URL
    # ==========================================
    #URL_SISTEMA = "http://localhost:5000"
    URL_SISTEMA = "https://saudeap.onrender.com"

    # ==========================================
    # FLASK MAIL
    # ==========================================

    MAIL_SERVER = os.getenv(
        "MAIL_SERVER",
        "smtp.gmail.com"
    )

    MAIL_PORT = int(
        os.getenv("MAIL_PORT", 587)
    )

    MAIL_USE_TLS = (
        os.getenv("MAIL_USE_TLS", "True") == "True"
    )

    MAIL_USE_SSL = (
        os.getenv("MAIL_USE_SSL", "False") == "True"
    )

    MAIL_USERNAME = os.getenv("MAIL_USERNAME")

    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    MAIL_DEFAULT_SENDER = os.getenv(
        "MAIL_DEFAULT_SENDER",
        MAIL_USERNAME
    )

    # ==========================================
    # DEBUG CONFIG
    # ==========================================

    print("\n========== CONFIGURAÇÃO ==========")

    print("MAIL_SERVER:", MAIL_SERVER)

    print("MAIL_PORT:", MAIL_PORT)

    print("MAIL_USE_TLS:", MAIL_USE_TLS)

    print("MAIL_USE_SSL:", MAIL_USE_SSL)

    print("MAIL_USERNAME:", MAIL_USERNAME)

    print("MAIL_DEFAULT_SENDER:", MAIL_DEFAULT_SENDER)

    print("MAIL_PASSWORD EXISTE?:", bool(MAIL_PASSWORD))

    print("JWT_SECRET_KEY EXISTE?:", bool(JWT_SECRET_KEY))

    print("SECRET_KEY EXISTE?:", bool(SECRET_KEY))

    print("==================================\n")

    @classmethod
    def validar_segredos(cls):

        ausentes = [

            nome

            for nome in (
                "SECRET_KEY",
                "JWT_SECRET_KEY"
            )

            if not getattr(cls, nome)

        ]

        if ausentes:

            raise RuntimeError(

                "Configure as variáveis obrigatórias: "

                + ", ".join(ausentes)

            )