"""CRUD de Movimentações."""

from flask import Blueprint, request, jsonify
from decorators import exigir_jwt_admin
from sqlalchemy.orm import selectinload

from models import Movimentacao, Estoque
from extensions import db
from database_utils import corrigir_sequence


movimentacao_bp = Blueprint("movimentacao", __name__)


@movimentacao_bp.before_request
def exigir_jwt():
    exigir_jwt_admin()


# ==========================================================
# LISTAR
# ==========================================================

@movimentacao_bp.route("/", methods=["GET"])
def listar():

    tipo = request.args.get("tipo")
    limite = request.args.get("limit", type=int)

    query = Movimentacao.query

    if tipo:
        query = query.filter_by(tipo=tipo)

    query = query.options(
        selectinload(Movimentacao.estoque).selectinload(Estoque.ubs),
        selectinload(Movimentacao.estoque).selectinload(Estoque.medicamento),
    ).order_by(Movimentacao.created_at.desc())

    if limite is not None:
        query = query.limit(max(1, min(limite, 100)))

    movimentacoes = query.all()

    return jsonify(
        [m.to_dict() for m in movimentacoes]
    )


# ==========================================================
# CRIAR
# ==========================================================

@movimentacao_bp.route("/", methods=["POST"])
def criar():

    data = request.get_json()

    if not data:

        return jsonify({
            "erro": "JSON inválido."
        }), 400

    estoque_id = data.get("estoque_id")
    tipo = data.get("tipo")
    quantidade = data.get("quantidade")

    if not estoque_id:

        return jsonify({
            "erro": "estoque_id é obrigatório."
        }), 400

    if tipo not in ["Entrada", "Saída"]:

        return jsonify({
            "erro": "Tipo deve ser Entrada ou Saída."
        }), 400

    if quantidade is None:

        return jsonify({
            "erro": "Quantidade é obrigatória."
        }), 400

    try:

        estoque = Estoque.query.get_or_404(estoque_id)

        # Corrige a sequence antes do INSERT
        corrigir_sequence("movimentacoes")

        # Atualiza o estoque

        if tipo == "Entrada":

            estoque.quantidade += quantidade

        else:

            if quantidade > estoque.quantidade:

                return jsonify({

                    "erro": "Quantidade maior que o estoque."

                }), 400

            estoque.quantidade -= quantidade

        movimentacao = Movimentacao(

            estoque_id=estoque.id,

            ubs_id=estoque.ubs_id,

            tipo=tipo,

            quantidade=quantidade,

            responsavel=data.get("responsavel"),

            observacao=data.get("observacao")

        )

        db.session.add(movimentacao)

        db.session.commit()

        return jsonify(
            movimentacao.to_dict()
        ), 201

    except Exception as erro:

        db.session.rollback()

        return jsonify({

            "erro": str(erro)

        }), 500


# ==========================================================
# DELETAR
# ==========================================================

@movimentacao_bp.route("/<int:mov_id>", methods=["DELETE"])
def deletar(mov_id):

    movimentacao = Movimentacao.query.get_or_404(mov_id)

    try:

        db.session.delete(movimentacao)

        db.session.commit()

        return jsonify({

            "message": "Movimentação removida com sucesso."

        }), 200

    except Exception as erro:

        db.session.rollback()

        return jsonify({

            "erro": str(erro)

        }), 500
