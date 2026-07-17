"""Rotas de autenticação para o painel web e clientes da API."""
from flask import Blueprint, current_app, flash, jsonify, redirect, render_template, request, session, url_for
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies

from extensions import db
from models import Usuario


auth_bp = Blueprint("auth", __name__)


def validar_credenciais(email, password):
    usuario = Usuario.query.filter_by(email=email.lower()).first()
    if not usuario or not usuario.ativo or not usuario.verificar_senha(password):
        return None
    return usuario


def gerar_token(usuario):
    return create_access_token(
        identity=str(usuario.id),
        additional_claims={"role": usuario.papel},
    )


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
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

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        usuario = validar_credenciais(email, password)

        if usuario:
            session["user_id"] = usuario.id
            response = redirect(url_for("admin.dashboard"))
            set_access_cookies(response, gerar_token(usuario))
            return response

        flash("E-mail ou senha inválidos.", "error")

    return render_template("login.html")


@auth_bp.route("/token", methods=["POST"])
def token():
    """Emite JWT para integrações que usam Authorization: Bearer."""
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").strip()
    password = data.get("password", "")
    usuario = validar_credenciais(email, password)

    if not usuario:
        return jsonify({"erro": "E-mail ou senha inválidos."}), 401

    return jsonify({
        "access_token": gerar_token(usuario),
        "token_type": "Bearer",
        "expires_in": int(current_app.config["JWT_ACCESS_TOKEN_EXPIRES"].total_seconds()),
    })


@auth_bp.route("/logout")
def logout():
    session.clear()
    response = redirect(url_for("auth.login"))
    unset_jwt_cookies(response)
    return response
