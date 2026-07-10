"""CRUD de Movimentações — registra entradas e saídas, atualizando o estoque."""
from flask import Blueprint, request, jsonify
from models import Movimentacao, Estoque
from extensions import db

movimentacao_bp = Blueprint("movimentacao", __name__)


@movimentacao_bp.route("/", methods=["GET"])
def listar():
    tipo = request.args.get("tipo")
    query = Movimentacao.query
    if tipo:
        query = query.filter_by(tipo=tipo)
    movs = query.order_by(Movimentacao.created_at.desc()).all()
    return jsonify([m.to_dict() for m in movs])


@movimentacao_bp.route("/", methods=["POST"])
def criar():
    data = request.get_json()
    estoque_id = data.get("estoque_id")
    tipo = data.get("tipo")  # "Entrada" ou "Saída"
    quantidade = data.get("quantidade")

    if not estoque_id or not tipo or quantidade is None:
        return jsonify({"error": "estoque_id, tipo e quantidade são obrigatórios"}), 400

    est = Estoque.query.get_or_404(estoque_id)

    if tipo == "Entrada":
        est.quantidade += quantidade
    elif tipo == "Saída":
        if quantidade > est.quantidade:
            return jsonify({"error": "Quantidade de saída maior que o estoque disponível"}), 400
        est.quantidade -= quantidade
    else:
        return jsonify({"error": "tipo deve ser 'Entrada' ou 'Saída'"}), 400

    mov = Movimentacao(
        estoque_id=estoque_id,
        ubs_id=est.ubs_id,
        tipo=tipo,
        quantidade=quantidade,
        responsavel=data.get("responsavel"),
        observacao=data.get("observacao"),
    )
    db.session.add(mov)
    db.session.commit()
    return jsonify(mov.to_dict()), 201


@movimentacao_bp.route("/<int:mov_id>", methods=["DELETE"])
def deletar(mov_id):
    mov = Movimentacao.query.get_or_404(mov_id)
    db.session.delete(mov)
    db.session.commit()
    return jsonify({"message": "Movimentação removida com sucesso"}), 200