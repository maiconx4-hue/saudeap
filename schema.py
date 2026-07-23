"""Compatibiliza instalações existentes sem substituir dados nem tabelas."""
from sqlalchemy import inspect, text

from extensions import db


_COLUNAS_HISTORICO = ("created_by", "updated_by", "deleted_by")


def criar_ou_atualizar_estrutura():
    db.create_all()
    inspector = inspect(db.engine)
    tabelas = set(inspector.get_table_names())
    if "usuarios" in tabelas:
        colunas = {c["name"] for c in inspector.get_columns("usuarios")}

        if "perfil" not in colunas:
            db.session.execute(text("""
                ALTER TABLE usuarios
                ADD COLUMN perfil VARCHAR(30)
                NOT NULL DEFAULT 'Administrador'
            """))

        if "nome" not in colunas:
            db.session.execute(text("""
                ALTER TABLE usuarios
                ADD COLUMN nome VARCHAR(150)
                NOT NULL DEFAULT 'Administrador'
            """))
                
    for tabela in ("ubs", "medicamentos", "estoques", "movimentacoes"):
        if tabela not in tabelas:
            continue
        colunas = {coluna["name"] for coluna in inspector.get_columns(tabela)}
        for coluna in _COLUNAS_HISTORICO:
            if coluna not in colunas:
                db.session.execute(text(f"ALTER TABLE {tabela} ADD COLUMN {coluna} INTEGER"))
    db.session.commit()
