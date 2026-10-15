from datetime import datetime
import os

import resend

from flask import render_template

from models import Usuario

resend.api_key = os.getenv("RESEND_API_KEY")


def enviar_email(
    assunto,
    destinatarios,
    template,
    **contexto
):

    print("\n==============================")
    print("INÍCIO DO ENVIO DE EMAIL")
    print("==============================")

    contexto["ano"] = datetime.now().year

    html = render_template(
        template,
        **contexto
    )

    try:

        print("Assunto:", assunto)
        print("Destinatários:", destinatarios)

        params = {
            "from": os.getenv("RESEND_FROM"),
            "to": destinatarios,
            "subject": assunto,
            "html": html
        }

        resposta = resend.Emails.send(params)

        print("EMAIL ENVIADO COM SUCESSO")
        print(resposta)

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

    print("\n======= TODOS OS USUÁRIOS =======")

    usuarios = Usuario.query.all()

    print("Quantidade total:", len(usuarios))

    administradores = []

    for u in usuarios:

        print(
            f"ID={u.id} | "
            f"EMAIL={u.email} | "
            f"ATIVO={u.ativo} | "
            f"PERFIL={u.perfil}"
        )

        if (
            u.ativo is True and
            str(u.perfil).upper() == "ADMINISTRADOR"
        ):
            administradores.append(u.email)

    print("\n======= ADMINISTRADORES =======")
    print("Quantidade encontrada:", len(administradores))

    for email in administradores:
        print(email)

    return administradores