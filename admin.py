"""Blueprint do painel administrativo — renderiza os templates."""
from flask import Blueprint, render_template
from decorators import login_required

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", active_page="dashboard")


@admin_bp.route("/medicamentos")
@login_required
def medicamentos():
    return render_template("medicamentos.html", active_page="medicamentos")


@admin_bp.route("/ubs")
@login_required
def ubs():
    return render_template("ubs.html", active_page="ubs")


@admin_bp.route("/estoque")
@login_required
def estoque():
    return render_template("estoque.html", active_page="estoque")


@admin_bp.route("/movimentacoes")
@login_required
def movimentacoes():
    return render_template("movimentacoes.html", active_page="movimentacoes")


@admin_bp.route("/relatorios")
@login_required
def relatorios():
    return render_template("relatorios.html", active_page="relatorios")