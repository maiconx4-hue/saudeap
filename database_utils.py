"""
Funções auxiliares do banco de dados.

Projeto: SaúdeAP
"""

from sqlalchemy import text
from extensions import db


def corrigir_sequence(nome_tabela):
    """
    Corrige a sequence de uma tabela PostgreSQL.

    Exemplo:

        corrigir_sequence("medicamentos")
        corrigir_sequence("estoques")
    """

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