"""CRUD de Unidades Básicas de Saúde."""

from flask import Blueprint, request, jsonify

from models import UBS
from extensions import db
from database_utils import corrigir_sequence


ubs_bp = Blueprint("ubs", __name__)


# ==========================================================
# LISTAR
# ==========================================================

@ubs_bp.route("/", methods=["GET"])
def listar():

    unidades = UBS.query.all()

    return jsonify(
        [u.to_dict() for u in unidades]
    )


# ==========================================================
# OBTER
# ==========================================================

@ubs_bp.route("/<int:ubs_id>", methods=["GET"])
def obter(ubs_id):

    unidade = UBS.query.get_or_404(ubs_id)

    return jsonify(
        unidade.to_dict()
    )


# ==========================================================
# CRIAR
# ==========================================================

@ubs_bp.route("/", methods=["POST"])
def criar():

    data = request.get_json()

    if not data:

        return jsonify({
            "erro": "JSON inválido."
        }), 400

    try:

        # Corrige automaticamente a sequence
        corrigir_sequence("ubs")

        unidade = UBS(

            nome=data.get("nome"),

            endereco=data.get("endereco"),

            bairro=data.get("bairro"),

            cidade=data.get("cidade", "Macapá"),

            telefone=data.get("telefone"),

            horario_funcionamento=data.get(
                "horario_funcionamento"
            ),

            latitude=data.get("latitude"),

            longitude=data.get("longitude")

        )

        db.session.add(unidade)

        db.session.commit()

        return jsonify(
            unidade.to_dict()
        ), 201

    except Exception as erro:

        db.session.rollback()

        return jsonify({

            "erro": str(erro)

        }), 500


# ==========================================================
# ATUALIZAR
# ==========================================================

@ubs_bp.route("/<int:ubs_id>", methods=["PUT"])
def atualizar(ubs_id):

    unidade = UBS.query.get_or_404(ubs_id)

    data = request.get_json()

    try:

        campos = [

            "nome",

            "endereco",

            "bairro",

            "cidade",

            "telefone",

            "horario_funcionamento",

            "latitude",

            "longitude"

        ]

        for campo in campos:

            if campo in data:

                setattr(
                    unidade,
                    campo,
                    data[campo]
                )

        db.session.commit()

        return jsonify(
            unidade.to_dict()
        )

    except Exception as erro:

        db.session.rollback()

        return jsonify({

            "erro": str(erro)

        }), 500


# ==========================================================
# DELETAR
# ==========================================================

@ubs_bp.route("/<int:ubs_id>", methods=["DELETE"])
def deletar(ubs_id):

    unidade = UBS.query.get_or_404(ubs_id)

    try:

        db.session.delete(unidade)

        db.session.commit()

        return jsonify({

            "message": "UBS removida com sucesso."

        }), 200

    except Exception as erro:

        db.session.rollback()

        return jsonify({

            "erro": str(erro)

        }), 500