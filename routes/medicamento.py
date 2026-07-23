"""CRUD de Medicamentos."""

from flask import Blueprint, request, jsonify
from decorators import exigir_jwt_admin
from sqlalchemy import or_, text

from models import Medicamento
from extensions import db

medicamento_bp = Blueprint("medicamento", __name__)


@medicamento_bp.before_request
def exigir_jwt():
    exigir_jwt_admin()


# ==========================================================
# LISTAR
# ==========================================================

@medicamento_bp.route("/", methods=["GET"])
def listar():

    termo = request.args.get("q", "").strip()

    query = Medicamento.query

    if termo:
        query = query.filter(
            or_(
                Medicamento.nome.ilike(f"%{termo}%"),
                Medicamento.principio_ativo.ilike(f"%{termo}%")
            )
        )

    medicamentos = query.order_by(Medicamento.nome).all()

    return jsonify(
        [m.to_dict() for m in medicamentos]
    )


# ==========================================================
# OBTER
# ==========================================================

@medicamento_bp.route("/<int:med_id>", methods=["GET"])
def obter(med_id):

    medicamento = Medicamento.query.get_or_404(med_id)

    return jsonify(medicamento.to_dict())


# ==========================================================
# CRIAR
# ==========================================================

@medicamento_bp.route("/", methods=["POST"])
def criar():

    data = request.get_json()

    if not data:

        return jsonify({
            "erro": "JSON inválido."
        }), 400

    if not data.get("nome"):

        return jsonify({
            "erro": "Nome é obrigatório."
        }), 400

    if not data.get("principio_ativo"):

        return jsonify({
            "erro": "Princípio ativo é obrigatório."
        }), 400

    try:

        # Corrige automaticamente a sequence
        db.session.execute(text("""

            SELECT setval(

                pg_get_serial_sequence('medicamentos','id'),

                COALESCE(
                    (SELECT MAX(id) FROM medicamentos),
                    1
                ),

                true

            );

        """))

        medicamento = Medicamento(

            nome=data.get("nome"),

            principio_ativo=data.get("principio_ativo"),

            dosagem=data.get("dosagem"),

            fabricante=data.get("fabricante"),

            descricao=data.get("descricao"),

            estoque_minimo=data.get("estoque_minimo", 10)

        )

        db.session.add(medicamento)

        db.session.commit()

        return jsonify(medicamento.to_dict()), 201

    except Exception as erro:

        db.session.rollback()

        return jsonify({
            "erro": str(erro)
        }), 500


# ==========================================================
# ATUALIZAR
# ==========================================================

@medicamento_bp.route("/<int:med_id>", methods=["PUT"])
def atualizar(med_id):

    medicamento = Medicamento.query.get_or_404(med_id)

    data = request.get_json()

    for campo in [
        "nome",
        "principio_ativo",
        "dosagem",
        "fabricante",
        "descricao",
        "estoque_minimo"
    ]:

        if campo in data:

            setattr(
                medicamento,
                campo,
                data[campo]
            )

    db.session.commit()

    return jsonify(medicamento.to_dict())


# ==========================================================
# EXCLUIR
# ==========================================================

@medicamento_bp.route("/<int:med_id>", methods=["DELETE"])
def deletar(med_id):

    medicamento = Medicamento.query.get_or_404(med_id)

    try:

        db.session.delete(medicamento)

        db.session.commit()

        return jsonify({

            "message": "Medicamento removido com sucesso."

        }), 200

    except Exception as erro:

        db.session.rollback()

        return jsonify({

            "erro": str(erro)

        }), 500
