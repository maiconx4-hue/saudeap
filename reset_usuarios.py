from app import create_app
from extensions import db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        print("Limpando tabela usuarios...")

        db.session.execute(
            text("TRUNCATE TABLE usuarios RESTART IDENTITY CASCADE;")
        )

        db.session.commit()

        print("✅ Tabela usuarios limpa com sucesso!")

    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro: {e}")