"""
Funções auxiliares do banco de dados.

Projeto: SaúdeAP
"""

from extensions import db
from sqlalchemy import text


def corrigir_sequence(nome_tabela):

    # MySQL não possui sequences
    if db.engine.dialect.name != "postgresql":
        return

    db.session.execute(text(f"""
        SELECT setval(
            pg_get_serial_sequence('{nome_tabela}','id'),
            COALESCE(
                (SELECT MAX(id) FROM {nome_tabela}),
                1
            ),
            true
        );
    """))