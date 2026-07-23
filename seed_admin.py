"""Cria ou atualiza o administrador inicial a partir de variáveis de ambiente."""
import os
import sys

from app import create_app
from extensions import db
from models import Usuario, PerfilUsuario


def main():
    email = os.getenv("ADMIN_EMAIL", "").strip().lower()
    senha = os.getenv("ADMIN_PASSWORD", "")

    if not email or not senha:
        sys.exit("Defina ADMIN_EMAIL e ADMIN_PASSWORD antes de executar o seed.")

    app = create_app()

    with app.app_context():

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario is None:
            usuario = Usuario(
                nome="Administrador",
                email=email,
                papel="admin",
                perfil=PerfilUsuario.ADMINISTRADOR,
                ativo=True
            )
            db.session.add(usuario)

        usuario.nome = "Administrador"
        usuario.papel = "admin"
        usuario.perfil = PerfilUsuario.ADMINISTRADOR
        usuario.ativo = True
        usuario.definir_senha(senha)

        db.session.commit()

        print(f"Administrador preparado para {email}.")


if __name__ == "__main__":
    main()