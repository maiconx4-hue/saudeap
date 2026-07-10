from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_cors import CORS
from extensions import db
#from functools import wraps
from config import Config

from extensions import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)

    from models import UBS, Medicamento, Estoque, Movimentacao  # noqa: F401

    # --- API Blueprints ---
    from routes.publico import publico_bp
    from routes.ubs import ubs_bp
    from routes.medicamento import medicamento_bp
    from routes.estoque import estoque_bp
    from routes.movimentacao import movimentacao_bp

    app.register_blueprint(publico_bp)
    app.register_blueprint(ubs_bp, url_prefix="/api/ubs")
    app.register_blueprint(medicamento_bp, url_prefix="/api/medicamentos")
    app.register_blueprint(estoque_bp, url_prefix="/api/estoques")
    app.register_blueprint(movimentacao_bp, url_prefix="/api/movimentacoes")

    # --- Páginas públicas ---
    @app.route("/")
    def index():
        return render_template("index.html")

    # --- Auth (simulado com sessão) ---
    from auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    # --- Painel administrativo ---
    from admin import admin_bp
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)