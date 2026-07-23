"""Serviços de sessão. O token é armazenado apenas como impressão SHA-256."""
from datetime import datetime
from hashlib import sha256

from flask import current_app, request, session

from extensions import db
from models import Sessao


def _agora():
    return datetime.utcnow()


def _token_hash(token):
    return sha256(token.encode("utf-8")).hexdigest()


def _encerrar_expiradas():
    limite = _agora() - current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]
    Sessao.query.filter(Sessao.ativa.is_(True), Sessao.ultimo_ping < limite).update(
        {"ativa": False, "fim": _agora()}, synchronize_session=False
    )


def criar_sessao(usuario_id, token):
    """Registra uma autenticação bem-sucedida e devolve a sessão persistida."""
    sessao_aberta = Sessao(
        usuario_id=usuario_id,
        token=_token_hash(token),
        ip=request.remote_addr if request else None,
        user_agent=(request.user_agent.string or "")[:512] if request else None,
    )
    db.session.add(sessao_aberta)
    db.session.flush()
    session["sessao_id"] = sessao_aberta.id
    return sessao_aberta


def atualizar_ping(sessao_id=None):
    _encerrar_expiradas()
    sessao_id = sessao_id or session.get("sessao_id")
    if sessao_id:
        aberta = db.session.get(Sessao, sessao_id)
        if aberta and aberta.ativa:
            aberta.ultimo_ping = _agora()
    db.session.commit()


def encerrar_sessao(sessao_id):
    aberta = db.session.get(Sessao, sessao_id)
    if aberta and aberta.ativa:
        aberta.ativa = False
        aberta.fim = _agora()
        aberta.ultimo_ping = aberta.fim
        db.session.commit()
        return True
    return False


def encerrar_todas_as_sessoes(usuario_id):
    total = Sessao.query.filter_by(usuario_id=usuario_id, ativa=True).update(
        {"ativa": False, "fim": _agora()}, synchronize_session=False
    )
    db.session.commit()
    return total


def listar_sessoes_ativas():
    _encerrar_expiradas()
    db.session.commit()
    return Sessao.query.filter_by(ativa=True).order_by(Sessao.inicio.desc()).all()


def listar_usuarios_online():
    """Uma sessão ativa representa um usuário online; inclui usuário e sessão."""
    return listar_sessoes_ativas()
