from flask import Blueprint

from permissions import admin_required

usuarios_bp = Blueprint(
    "usuarios",
    __name__,
    url_prefix="/api/usuarios"
)

from flask import request, jsonify

from extensions import db
from models import Usuario, PerfilUsuario


@usuarios_bp.route("", methods=["GET"])
@admin_required
def listar_usuarios():

    usuarios = Usuario.query.order_by(Usuario.nome).all()

    resultado = []

    for usuario in usuarios:

        resultado.append({
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "perfil": usuario.perfil,
            "ativo": usuario.ativo,
            "created_at": usuario.created_at.strftime("%d/%m/%Y %H:%M")
        })

    return jsonify(resultado)