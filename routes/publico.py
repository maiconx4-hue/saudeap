"""Rotas públicas — consulta de medicamentos e lista de UBS."""
from flask import Blueprint, request, jsonify
from models import UBS, Medicamento, Estoque
from extensions import db
from sqlalchemy import or_

publico_bp = Blueprint("publico", __name__)


@publico_bp.route("/api/ubs", methods=["GET"])
def listar_ubs_publico():
    """Lista todas as UBS (endpoint público)."""
    unidades = UBS.query.all()
    return jsonify([u.to_dict() for u in unidades])


@publico_bp.route("/api/consulta", methods=["GET"])
def consultar_medicamento():
    """Consulta pública: busca medicamento por nome ou princípio ativo
    e retorna em quais UBS está disponível, agrupado por medicamento."""
    termo = request.args.get("q", "").strip().lower()
    if not termo:
        return jsonify({"error": "Parâmetro 'q' é obrigatório"}), 400

    medicamentos = Medicamento.query.filter(
        or_(
            Medicamento.nome.ilike(f"%{termo}%"),
            Medicamento.principio_ativo.ilike(f"%{termo}%"),
        )
    ).all()

    resultados = []
    for med in medicamentos:
        estoques = Estoque.query.filter_by(medicamento_id=med.id).filter(Estoque.quantidade > 0).all()
        unidades = []
        for est in estoques:
            if est.ubs:
                unidades.append({
                    "ubs": est.ubs.to_dict(),
                    "quantidade": est.quantidade,
                    "lote": est.lote,
                    "validade": est.validade.isoformat() if est.validade else None,
                })
        if unidades:
            resultados.append({
                "medicamento": med.to_dict(),
                "unidades": unidades,
            })

    return jsonify(resultados)