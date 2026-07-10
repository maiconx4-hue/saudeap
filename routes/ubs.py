"""CRUD de Unidades Básicas de Saúde."""
from flask import Blueprint, request, jsonify
from models import UBS
from extensions import db

ubs_bp = Blueprint("ubs", __name__)


@ubs_bp.route("/", methods=["GET"])
def listar():
    unidades = UBS.query.all()
    return jsonify([u.to_dict() for u in unidades])


@ubs_bp.route("/<int:ubs_id>", methods=["GET"])
def obter(ubs_id):
    ubs = UBS.query.get_or_404(ubs_id)
    return jsonify(ubs.to_dict())


@ubs_bp.route("/", methods=["POST"])
def criar():
    data = request.get_json()
    ubs = UBS(
        nome=data.get("nome"),
        endereco=data.get("endereco"),
        bairro=data.get("bairro"),
        cidade=data.get("cidade", "Macapá"),
        telefone=data.get("telefone"),
        horario_funcionamento=data.get("horario_funcionamento"),
        latitude=data.get("latitude"),
        longitude=data.get("longitude"),
    )
    db.session.add(ubs)
    db.session.commit()
    return jsonify(ubs.to_dict()), 201


@ubs_bp.route("/<int:ubs_id>", methods=["PUT"])
def atualizar(ubs_id):
    ubs = UBS.query.get_or_404(ubs_id)
    data = request.get_json()
    for campo in ["nome", "endereco", "bairro", "cidade", "telefone",
                  "horario_funcionamento", "latitude", "longitude"]:
        if campo in data:
            setattr(ubs, campo, data[campo])
    db.session.commit()
    return jsonify(ubs.to_dict())


@ubs_bp.route("/<int:ubs_id>", methods=["DELETE"])
def deletar(ubs_id):
    ubs = UBS.query.get_or_404(ubs_id)
    db.session.delete(ubs)
    db.session.commit()
    return jsonify({"message": "UBS removida com sucesso"}), 200