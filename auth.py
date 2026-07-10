"""Blueprint de autenticação — login/logout com sessão simples."""
from flask import Blueprint, render_template, redirect, url_for, request, session, flash

auth_bp = Blueprint("auth", __name__)

# Credenciais simuladas (em produção, use hash + banco de dados)
USERS = {
    "admin@saudeap.gov.br": "admin123",
}


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        if USERS.get(email) == password:
            session["user_id"] = email
            return redirect(url_for("admin.dashboard"))
        flash("E-mail ou senha inválidos.", "error")
    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))