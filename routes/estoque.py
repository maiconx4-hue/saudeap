"""CRUD de Estoque."""
from flask import Blueprint, request, jsonify
from models import Estoque, UBS, Medicamento
from extensions import db
from datetime import datetime

estoque_bp = Blueprint("estoque", __name__)


@estoque_bp.route("/", methods=["GET"])
def listar():
    ubs_id = request.args.get("ubs_id")
    med_id = request.args.get("medicamento_id")
    query = Estoque.query
    if ubs_id:
        query = query.filter_by(ubs_id=ubs_id)
    if med_id:
        query = query.filter_by(medicamento_id=med_id)
    estoques = query.all()
    return jsonify([e.to_dict() for e in estoques])


@estoque_bp.route("/<int:est_id>", methods=["GET"])
def obter(est_id):
    est = Estoque.query.get_or_404(est_id)
    return jsonify(est.to_dict())


@estoque_bp.route("/", methods=["POST"])
def criar():
    data = request.get_json()
    est = Estoque(
        ubs_id=data.get("ubs_id"),
        medicamento_id=data.get("medicamento_id"),
        quantidade=data.get("quantidade", 0),
        lote=data.get("lote"),
        validade = datetime.strptime(
        data["validade"],
        "%Y-%m-%d"
        ).date(),
    )
    db.session.add(est)
    db.session.commit()
    return jsonify(est.to_dict()), 201


@estoque_bp.route("/<int:est_id>", methods=["PUT"])
def atualizar(est_id):
    est = Estoque.query.get_or_404(est_id)
    data = request.get_json()
    for campo in ["ubs_id", "medicamento_id", "quantidade", "lote", "validade"]:
        if campo in data:
            setattr(est, campo, data[campo])
    db.session.commit()
    return jsonify(est.to_dict())


@estoque_bp.route("/<int:est_id>", methods=["DELETE"])
def deletar(est_id):
    est = Estoque.query.get_or_404(est_id)
    db.session.delete(est)
    db.session.commit()
    return jsonify({"message": "Estoque removido com sucesso"}), 200