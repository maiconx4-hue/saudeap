from datetime import datetime

from flask import Blueprint, jsonify

from permissions import admin_required
from session_manager import listar_usuarios_online

admin_users_bp = Blueprint(
    "admin_users",
    __name__,
    url_prefix="/api/admin"
)


@admin_users_bp.route("/usuarios-online", methods=["GET"])
@admin_required
def usuarios_online():
    """
    Lista todos os usuários com sessões ativas.
    Apenas Administradores podem acessar.
    """

    sessoes = listar_usuarios_online()

    # Mais recentes primeiro
    sessoes.sort(
        key=lambda s: s.ultimo_ping,
        reverse=True
    )

    agora = datetime.utcnow()

    usuarios = []

    for sessao in sessoes:

        tempo = agora - sessao.inicio

        segundos = int(tempo.total_seconds())

        horas = segundos // 3600
        minutos = (segundos % 3600) // 60

        usuarios.append({

            "sessao_id": sessao.id,

            "usuario_id": sessao.usuario.id,

            # Futuramente trocar por sessao.usuario.nome
            "nome": sessao.usuario.nome,

            "email": sessao.usuario.email,

            "perfil": (
                sessao.usuario.perfil.value
                if sessao.usuario.perfil
                else "-"
            ),

            "ip": sessao.ip or "-",

            "user_agent": sessao.user_agent or "-",

            "inicio": sessao.inicio.isoformat(),

            "ultimo_ping": sessao.ultimo_ping.isoformat(),

            "tempo_online": f"{horas}h {minutos}min",

            "ativa": sessao.ativa

        })

    return jsonify({
        "total_online": len(usuarios),
        "usuarios": usuarios
    })