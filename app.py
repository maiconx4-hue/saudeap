import os
from flask import Flask, render_template
from flask_cors import CORS

from extensions import db
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)

    # Importa os modelos
    from models import UBS, Medicamento, Estoque, Movimentacao


# ===========================
# Site
# ===========================

    from routes.site import site_bp
    app.register_blueprint(site_bp)

    # ===========================
    # Blueprints da API
    # ===========================
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

    # ===========================
    # Página pública
    # ===========================
    @app.route("/")
    def index():
        return render_template("index.html")

    # ===========================
    # Autenticação
    # ===========================
    from auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    # ===========================
    # Painel Administrativo
    # ===========================
    from admin import admin_bp
    app.register_blueprint(admin_bp)

    # ===========================
    # Criação automática das tabelas
    # ===========================
    with app.app_context():
        try:
            db.create_all()
            print("✅ Banco conectado com sucesso.")
        except Exception as e:
            print(f"❌ Erro ao conectar ao banco: {e}")

    return app


# Cria a aplicação
app = create_app()


# Executa apenas localmente
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )