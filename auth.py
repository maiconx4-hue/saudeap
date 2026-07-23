"""Rotas de autenticação para o painel web e clientes da API."""

from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
    unset_jwt_cookies,
)

from extensions import db
from models import Usuario
from session_manager import (
    criar_sessao,
    encerrar_sessao,
)

auth_bp = Blueprint("auth", __name__)


# ==========================================================
# Validação de usuário
# ==========================================================

def validar_credenciais(email, password):
    usuario = Usuario.query.filter_by(email=email.lower()).first()

    if not usuario:
        return None

    if not usuario.ativo:
        return None

    if not usuario.verificar_senha(password):
        return None

    return usuario


# ==========================================================
# JWT
# ==========================================================

def gerar_token(usuario):
    perfil = (
        usuario.perfil.value
        if hasattr(usuario.perfil, "value")
        else usuario.perfil
    )

    return create_access_token(
        identity=str(usuario.id),
        additional_claims={
            "role": usuario.papel,
            "perfil": perfil,
        },
    )


# ==========================================================
# LOGIN
# ==========================================================

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    # Já autenticado?
    if "user_id" in session:

        try:
            usuario_id = int(session["user_id"])

        except (TypeError, ValueError):
            session.clear()

        else:

            usuario = db.session.get(Usuario, usuario_id)

            if usuario and usuario.eh_admin:
                return redirect(url_for("admin.dashboard"))

            session.clear()

    # Enviou formulário
    if request.method == "POST":

        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        usuario = validar_credenciais(email, password)

        if usuario:

            token = gerar_token(usuario)

            # Sessão Flask
            session["user_id"] = usuario.id

            # Registra sessão no banco
            criar_sessao(
                usuario.id,
                token,
            )

            db.session.commit()

            response = redirect(url_for("admin.dashboard"))

            set_access_cookies(
                response,
                token,
            )

            return response

        flash(
            "E-mail ou senha inválidos.",
            "error",
        )

    return render_template("login.html")


# ==========================================================
# TOKEN PARA API
# ==========================================================

@auth_bp.route("/token", methods=["POST"])
def token():

    data = request.get_json(silent=True) or {}

    email = data.get("email", "").strip()
    password = data.get("password", "")

    usuario = validar_credenciais(email, password)

    if not usuario:

        return jsonify(
            {
                "erro": "E-mail ou senha inválidos."
            }
        ), 401

    token = gerar_token(usuario)

    criar_sessao(
        usuario.id,
        token,
    )

    db.session.commit()

    return jsonify(
        {
            "access_token": token,
            "token_type": "Bearer",
            "expires_in": int(
                current_app.config[
                    "JWT_ACCESS_TOKEN_EXPIRES"
                ].total_seconds()
            ),
        }
    )


# ==========================================================
# LOGOUT
# ==========================================================

@auth_bp.route("/logout")
def logout():

    sessao_id = session.get("sessao_id")

    if sessao_id:
        encerrar_sessao(sessao_id)

    session.clear()

    response = redirect(url_for("auth.login"))

    unset_jwt_cookies(response)

    return response