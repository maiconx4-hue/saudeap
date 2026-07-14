"""CRUD de Estoque."""

from datetime import datetime

from flask import Blueprint, request, jsonify

from models import Estoque
from extensions import db
from database_utils import corrigir_sequence


estoque_bp = Blueprint("estoque", __name__)


# ==========================================================
# LISTAR
# ==========================================================

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

    return jsonify(
        [e.to_dict() for e in estoques]
    )


# ==========================================================
# OBTER
# ==========================================================

@estoque_bp.route("/<int:est_id>", methods=["GET"])
def obter(est_id):

    estoque = Estoque.query.get_or_404(est_id)

    return jsonify(
        estoque.to_dict()
    )


# ==========================================================
# CRIAR
# ==========================================================

@estoque_bp.route("/", methods=["POST"])
def criar():

    data = request.get_json()

    if not data:

        return jsonify({
            "erro": "JSON inválido."
        }), 400

    try:

        # Corrige automaticamente a sequence
        corrigir_sequence("estoques")

        validade = None

        if data.get("validade"):

            validade = datetime.strptime(
                data["validade"],
                "%Y-%m-%d"
            ).date()

        estoque = Estoque(

            ubs_id=data.get("ubs_id"),

            medicamento_id=data.get("medicamento_id"),

            quantidade=data.get("quantidade", 0),

            lote=data.get("lote"),

            validade=validade

        )

        db.session.add(estoque)

        db.session.commit()

        return jsonify(
            estoque.to_dict()
        ), 201

    except Exception as erro:

        db.session.rollback()

        return jsonify({

            "erro": str(erro)

        }), 500


# ==========================================================
# ATUALIZAR
# ==========================================================

@estoque_bp.route("/<int:est_id>", methods=["PUT"])
def atualizar(est_id):

    estoque = Estoque.query.get_or_404(est_id)

    data = request.get_json()

    try:

        if "ubs_id" in data:
            estoque.ubs_id = data["ubs_id"]

        if "medicamento_id" in data:
            estoque.medicamento_id = data["medicamento_id"]

        if "quantidade" in data:
            estoque.quantidade = data["quantidade"]

        if "lote" in data:
            estoque.lote = data["lote"]

        if "validade" in data:

            if data["validade"]:

                estoque.validade = datetime.strptime(
                    data["validade"],
                    "%Y-%m-%d"
                ).date()

            else:

                estoque.validade = None

        db.session.commit()

        return jsonify(
            estoque.to_dict()
        )

    except Exception as erro:

        db.session.rollback()

        return jsonify({

            "erro": str(erro)

        }), 500


# ==========================================================
# DELETAR
# ==========================================================

@estoque_bp.route("/<int:est_id>", methods=["DELETE"])
def deletar(est_id):

    estoque = Estoque.query.get_or_404(est_id)

    try:

        db.session.delete(estoque)

        db.session.commit()

        return jsonify({

            "message": "Estoque removido com sucesso."

        }), 200

    except Exception as erro:

        db.session.rollback()

        return jsonify({

            "erro": str(erro)

        }), 500