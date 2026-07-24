from datetime import datetime

from flask import render_template, current_app
from flask_mail import Message

from extensions import mail
from models import Usuario


def enviar_email(
    assunto,
    destinatarios,
    template,
    **contexto
):

    print("\n==============================")
    print("INÍCIO DO ENVIO DE EMAIL")
    print("==============================")

    try:

        contexto["ano"] = datetime.now().year

        print("Template:", template)

        html = render_template(
            template,
            **contexto
        )

        print("Template renderizado com sucesso")

        print("\n===== CONFIG SMTP =====")
        print("Servidor:", current_app.config["MAIL_SERVER"])
        print("Porta:", current_app.config["MAIL_PORT"])
        print("Usuário:", current_app.config["MAIL_USERNAME"])
        print("Remetente:", current_app.config["MAIL_DEFAULT_SENDER"])
        print("TLS:", current_app.config["MAIL_USE_TLS"])
        print("SSL:", current_app.config["MAIL_USE_SSL"])
        print("Senha existe?:", bool(current_app.config["MAIL_PASSWORD"]))
        print("=======================\n")

        print("Destinatários:", destinatarios)

        msg = Message(
            subject=assunto,
            recipients=destinatarios,
            html=html
        )

        print("Objeto Message criado")

        print("Abrindo conexão SMTP...")

        with mail.connect() as conn:

            print("Conexão aberta!")

            print("Enviando mensagem...")

            conn.send(msg)

            print("Mensagem enviada!")

        print("Conexão encerrada")
        print("EMAIL ENVIADO COM SUCESSO!")

    except Exception as e:

        print("\n######## ERRO NO ENVIO ########")
        print("Tipo:", type(e).__name__)
        print("Mensagem:", repr(e))
        print("###############################\n")

        raise


def enviar_alerta_estoque_baixo(
    destinatarios,
    medicamento,
    ubs,
    quantidade,
    minimo,
    sistema
):

    print("Chamando enviar_alerta_estoque_baixo()")

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

    print("Chamando enviar_alerta_estoque_zero()")

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

    for u in usuarios:
        print(
            f"ID={u.id} | "
            f"EMAIL={u.email} | "
            f"ATIVO={u.ativo} ({type(u.ativo)}) | "
            f"PERFIL={u.perfil} ({type(u.perfil)})"
        )

    administradores = Usuario.query.filter(
        Usuario.ativo == True,
        Usuario.perfil == "ADMINISTRADOR"
    ).all()

    print("\n======= ADMINISTRADORES =======")
    print("Quantidade encontrada:", len(administradores))

    for a in administradores:
        print(a.email)

    return [u.email for u in administradores]