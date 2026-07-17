import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    # Use uma chave exclusiva e longa em produção via JWT_SECRET_KEY.
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    JWT_COOKIE_SECURE = os.getenv("JWT_COOKIE_SECURE", "true").lower() == "true"
    JWT_COOKIE_SAMESITE = "Lax"
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(os.getenv("JWT_ACCESS_TOKEN_HOURS", "8")))

    # Se existir DATABASE_URL (Render), usa PostgreSQL.
    # Caso contrário, usa MySQL local.
    if os.getenv("DATABASE_URL"):

        database_url = os.getenv("DATABASE_URL")

        # Compatibilidade SQLAlchemy
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

        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{os.getenv('DB_USER')}:"
            f"{os.getenv('DB_PASSWORD')}@"
            f"{os.getenv('DB_HOST')}:"
            f"{os.getenv('DB_PORT')}/"
            f"{os.getenv('DB_NAME')}"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @classmethod
    def validar_segredos(cls):
        ausentes = [nome for nome in ("SECRET_KEY", "JWT_SECRET_KEY") if not getattr(cls, nome)]
        if ausentes:
            raise RuntimeError("Configure as variáveis de ambiente obrigatórias: " + ", ".join(ausentes))
