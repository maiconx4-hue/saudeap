"""Auditoria automática e campos de autoria via eventos do SQLAlchemy."""
import json
from datetime import datetime

from flask import has_request_context, request, session
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import event, inspect
from sqlalchemy.orm import Session

from models import LogAuditoria, Sessao, Usuario


_IGNORADOS = (LogAuditoria, Sessao)


def _usuario_id():
    if not has_request_context():
        return None
    valor = session.get("user_id")
    if valor is None:
        try:
            valor = get_jwt_identity()
        except RuntimeError:
            return None
    try:
        return int(valor)
    except (TypeError, ValueError):
        return None


def _detalhes(obj, acao):
    estado = inspect(obj)
    dados = {}
    for coluna in estado.mapper.columns:
        if coluna.key in {"senha_hash"}:
            continue
        historico = estado.attrs[coluna.key].history
        if acao == "UPDATE" and not historico.has_changes():
            continue
        valor = getattr(obj, coluna.key, None)
        dados[coluna.key] = str(valor) if valor is not None else None
    return json.dumps(dados, ensure_ascii=False, default=str)


@event.listens_for(Session, "before_flush")
def preparar_auditoria(sessao, _flush_context, _instances):
    if sessao.info.get("audit_preparing"):
        return
    usuario_id = _usuario_id()
    pendentes = sessao.info.setdefault("audit_pending", [])
    for colecao, acao in ((sessao.new, "CREATE"), (sessao.dirty, "UPDATE"), (sessao.deleted, "DELETE")):
        for obj in list(colecao):
            if isinstance(obj, _IGNORADOS) or not hasattr(obj, "__tablename__"):
                continue
            if acao == "UPDATE" and not sessao.is_modified(obj, include_collections=False):
                continue
            if acao == "CREATE" and hasattr(obj, "created_by"):
                obj.created_by = usuario_id
            elif acao == "UPDATE" and hasattr(obj, "updated_by"):
                obj.updated_by = usuario_id
            # Em exclusões físicas, deleted_by é preservado nos detalhes do log.
            pendentes.append((obj, acao, usuario_id, _detalhes(obj, acao)))


@event.listens_for(Session, "after_flush_postexec")
def gravar_auditoria(sessao, _flush_context):
    pendentes = sessao.info.pop("audit_pending", [])
    if not pendentes:
        return
    ip = request.remote_addr if has_request_context() else None
    user_agent = (request.user_agent.string or "")[:512] if has_request_context() else None
    for obj, acao, usuario_id, detalhes in pendentes:
        sessao.add(LogAuditoria(
            usuario_id=usuario_id, acao=acao, tabela=obj.__tablename__,
            registro_id=getattr(obj, "id", None), ip=ip, user_agent=user_agent,
            data_hora=datetime.utcnow(), detalhes=detalhes,
        ))
