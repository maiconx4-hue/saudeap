"""CRUD de Medicamentos."""
from flask import Blueprint, request, jsonify
from models import Medicamento
from extensions import db

medicamento_bp = Blueprint("medicamento", __name__)


@medicamento_bp.route("/", methods=["GET"])
def listar():
    termo = request.args.get("q", "").strip()
    query = Medicamento.query
    if termo:
        query = query.filter(
            or_(
                Medicamento.nome.ilike(f"%{termo}%"),
                Medicamento.principio_ativo.ilike(f"%{termo}%"),
            )
        )
    meds = query.all()
    return jsonify([m.to_dict() for m in meds])


@medicamento_bp.route("/<int:med_id>", methods=["GET"])
def obter(med_id):
    med = Medicamento.query.get_or_404(med_id)
    return jsonify(med.to_dict())


@medicamento_bp.route("/", methods=["POST"])
def criar():
    data = request.get_json()
    med = Medicamento(
        nome=data.get("nome"),
        principio_ativo=data.get("principio_ativo"),
        dosagem=data.get("dosagem"),
        fabricante=data.get("fabricante"),
        descricao=data.get("descricao"),
    )
    db.session.add(med)
    db.session.commit()
    return jsonify(med.to_dict()), 201


@medicamento_bp.route("/<int:med_id>", methods=["PUT"])
def atualizar(med_id):
    med = Medicamento.query.get_or_404(med_id)
    data = request.get_json()
    for campo in ["nome", "principio_ativo", "dosagem", "fabricante", "descricao"]:
        if campo in data:
            setattr(med, campo, data[campo])
    db.session.commit()
    return jsonify(med.to_dict())


@medicamento_bp.route("/<int:med_id>", methods=["DELETE"])
def deletar(med_id):
    med = Medicamento.query.get_or_404(med_id)
    db.session.delete(med)
    db.session.commit()
    return jsonify({"message": "Medicamento removido com sucesso"}), 200