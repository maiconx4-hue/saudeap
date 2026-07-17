from functools import wraps
from flask import abort, session, redirect, url_for, flash
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from extensions import db
from models import Usuario


def login_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            usuario_id = int(session.get("user_id"))
        except (TypeError, ValueError):
            usuario_id = None

        usuario = db.session.get(Usuario, usuario_id) if usuario_id is not None else None
        if not usuario or not usuario.eh_admin:
            session.clear()
            flash("Faça login para acessar.", "error")
            return redirect(url_for("auth.login"))

        return f(*args, **kwargs)

    return decorated


def exigir_jwt_admin():
    """Exige JWT válido de um administrador ativo nas APIs administrativas."""
    verify_jwt_in_request()
    try:
        usuario_id = int(get_jwt_identity())
    except (TypeError, ValueError):
        abort(401)

    usuario = db.session.get(Usuario, usuario_id)
    if not usuario or not usuario.eh_admin:
        abort(403)
