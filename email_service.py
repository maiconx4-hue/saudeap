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
    """
    Envia um e-mail HTML utilizando os templates
    da pasta templates/emails.
    """

    contexto["ano"] = datetime.now().year

    html = render_template(
        template,
        **contexto
    )

    msg = Message(
        subject=assunto,
        recipients=destinatarios,
        html=html
    )

    mail.send(msg)


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