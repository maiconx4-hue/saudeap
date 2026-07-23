"""Decorator reutilizável para autorização por perfil."""
from functools import wraps

from flask import jsonify, session
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from extensions import db
from models import PerfilUsuario, Usuario


def _usuario_atual():
    usuario_id = session.get("user_id")
    if usuario_id is None:
        verify_jwt_in_request(optional=True)
        usuario_id = get_jwt_identity()
    try:
        return db.session.get(Usuario, int(usuario_id))
    except (TypeError, ValueError):
        return None


def roles_required(*perfis):
    permitidos = {perfil.value if isinstance(perfil, PerfilUsuario) else perfil for perfil in perfis}

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            usuario = _usuario_atual()
            perfil = usuario.perfil if usuario else None
            if not usuario or not usuario.ativo:
                return jsonify({"erro": "Autenticação necessária."}), 401
            if perfil not in permitidos:
                return jsonify({"erro": "Permissão insuficiente."}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator


def is_admin(usuario):
    return (
        usuario
        and usuario.ativo
        and usuario.perfil == PerfilUsuario.ADMINISTRADOR.value
    )


def is_gestor(usuario):
    return (
        usuario
        and usuario.ativo
        and usuario.perfil == PerfilUsuario.GESTOR.value
    )


def is_farmaceutico(usuario):
    return (
        usuario
        and usuario.ativo
        and usuario.perfil == PerfilUsuario.FARMACEUTICO.value
    )


def wrapper(*args, **kwargs):

    usuario = _usuario_atual()
    perfil = usuario.perfil if usuario else None

    print("="*50)
    print("Perfil banco:", perfil)
    print("Permitidos:", permitidos)
    print("="*50)

    if not usuario or not usuario.ativo:
        ...

def admin_required(func):
    return roles_required(
        PerfilUsuario.ADMINISTRADOR
    )(func)


def gestor_required(func):
    return roles_required(
        PerfilUsuario.ADMINISTRADOR,
        PerfilUsuario.GESTOR
    )(func)


def farmacia_required(func):
    return roles_required(
        PerfilUsuario.ADMINISTRADOR,
        PerfilUsuario.GESTOR,
        PerfilUsuario.FARMACEUTICO
    )(func)