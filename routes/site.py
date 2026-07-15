from flask import Blueprint, render_template

from models import UBS, Estoque


site_bp = Blueprint("site", __name__)


@site_bp.route("/")
def index():
    ubs = UBS.query.all()
    return render_template("index.html", ubs=ubs)


@site_bp.route("/ubs/<int:ubs_id>")
def detalhes_ubs(ubs_id):

    ubs = UBS.query.get_or_404(ubs_id)

    return render_template(
        "ubs_detalhes.html",
        ubs=ubs
    )