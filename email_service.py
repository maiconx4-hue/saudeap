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

    print("1 - Entrou enviar_email")

    contexto["ano"] = datetime.now().year

    print("2 - Renderizando HTML")

    html = render_template(
        template,
        **contexto
    )

    print("3 - Criando Message")

    msg = Message(
        subject=assunto,
        recipients=destinatarios,
        html=html
    )

    print("4 - Vai enviar email")

    mail.send(msg)

    print("5 - Email enviado")


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

    usuarios = Usuario.query.all()

    for u in usuarios:
        print("EMAIL:", u.email)
        print("PERFIL:", u.perfil)
        print("ATIVO:", u.ativo)

    return [u.email for u in usuarios]