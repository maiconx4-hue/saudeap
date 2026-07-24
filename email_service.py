from datetime import datetime

from flask import render_template
from flask_mail import Message

from extensions import mail
from models import Usuario, PerfilUsuario

def enviar_email(
    assunto,
    destinatarios,
    template,
    **contexto
):
    try:
        contexto["ano"] = datetime.now().year

        html = render_template(
            template,
            **contexto
        )

        print("========== EMAIL ==========")
        print("Assunto:", assunto)
        print("Destinatários:", destinatarios)
        print("Servidor:", mail.state.app.config["MAIL_SERVER"])
        print("Usuário:", mail.state.app.config["MAIL_USERNAME"])
        print("TLS:", mail.state.app.config["MAIL_USE_TLS"])

        msg = Message(
            subject=assunto,
            recipients=destinatarios,
            html=html
        )

        print("Conectando ao Gmail...")

        mail.send(msg)

        print("EMAIL ENVIADO COM SUCESSO!")

    except Exception as e:
        print("ERRO AO ENVIAR EMAIL")
        print(type(e).__name__)
        print(str(e))
        raise


def enviar_alerta_estoque_baixo(
    destinatarios,
    medicamento,
    ubs,
    quantidade,
    minimo,
    sistema
):
    enviar_email(
        assunto="⚠️ SaúdeAP - Estoque Baixo",
        destinatarios=destinatarios,
        template="emails/estoque_baixo.html",
        medicamento=medicamento,
        ubs=ubs,
        quantidade=quantidade,
        minimo=minimo,
        sistema=sistema
    )


def enviar_alerta_estoque_zero(
    destinatarios,
    medicamento,
    ubs,
    sistema
):
    enviar_email(
        assunto="🚨 SaúdeAP - Estoque Zerado",
        destinatarios=destinatarios,
        template="emails/estoque_zerado.html",
        medicamento=medicamento,
        ubs=ubs,
        sistema=sistema
    )


def emails_administradores():

    administradores = Usuario.query.filter(
        Usuario.ativo == True,
        Usuario.perfil == PerfilUsuario.ADMINISTRADOR.value
    ).all()

    return [u.email for u in administradores]