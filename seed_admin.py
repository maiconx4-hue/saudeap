"""Cria ou atualiza o administrador inicial a partir de variáveis de ambiente."""
import os
import sys

from app import create_app
from extensions import db
from models import Usuario


def main():
    email = os.getenv("ADMIN_EMAIL", "").strip().lower()
    senha = os.getenv("ADMIN_PASSWORD", "")
    if not email or not senha:
        sys.exit("Defina ADMIN_EMAIL e ADMIN_PASSWORD antes de executar o seed.")

    app = create_app()
    with app.app_context():
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario is None:
            usuario = Usuario(email=email, papel="admin", ativo=True)
            db.session.add(usuario)

        usuario.papel = "admin"
        usuario.ativo = True
        usuario.definir_senha(senha)
        db.session.commit()
        print(f"Administrador preparado para {email}.")


if __name__ == "__main__":
    main()
