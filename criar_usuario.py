import os

from app import create_app
from extensions import db
from models import Usuario, PerfilUsuario


EMAIL = "farmaceutico@saudeap.gov.br"
SENHA = "123456"
PERFIL = PerfilUsuario.FARMACEUTICO


app = create_app()

with app.app_context():

    usuario = Usuario.query.filter_by(email=EMAIL).first()

    if usuario:
        print("Usuário já existe.")
    else:

        usuario = Usuario(
            email=EMAIL,
            papel="user",
            perfil=PERFIL,
            ativo=True
        )

        usuario.definir_senha(SENHA)

        db.session.add(usuario)
        db.session.commit()

        print("Usuário criado com sucesso!")
        print(f"E-mail : {EMAIL}")
        print(f"Perfil : {PERFIL.value}")