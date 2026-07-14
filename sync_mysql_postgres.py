"""
===========================================================
SINCRONIZADOR MYSQL -> POSTGRESQL
Projeto: SaúdeAP

MySQL = Banco Mestre
PostgreSQL = Espelho

Autor: Maicon Sardinha
===========================================================
"""

import os
import time
from dataclasses import dataclass

from dotenv import load_dotenv

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.inspection import inspect

from models import (
    UBS,
    Medicamento,
    Estoque,
    Movimentacao
)

# ===========================================================
# CARREGA .ENV
# ===========================================================

load_dotenv()

# ===========================================================
# MYSQL
# ===========================================================

MYSQL_URL = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

mysql_engine = create_engine(
    MYSQL_URL,
    pool_pre_ping=True
)

MySQLSession = sessionmaker(bind=mysql_engine)
mysql = MySQLSession()

# ===========================================================
# POSTGRES
# ===========================================================

POSTGRES_URL = (
    f"postgresql+psycopg2://"
    f"{os.getenv('PG_USER')}:"
    f"{os.getenv('PG_PASSWORD')}@"
    f"{os.getenv('PG_HOST')}:"
    f"{os.getenv('PG_PORT')}/"
    f"{os.getenv('PG_DATABASE')}"
)

postgres_engine = create_engine(
    POSTGRES_URL,
    pool_pre_ping=True
)

PostgresSession = sessionmaker(bind=postgres_engine)
postgres = PostgresSession()

# ===========================================================
# CABEÇALHO
# ===========================================================

inicio = time.perf_counter()

print("=" * 65)
print("             SINCRONIZADOR SAÚDEAP")
print("=" * 65)

print("✅ MySQL conectado")
print("✅ PostgreSQL conectado")
print()

# ===========================================================
# ESTATÍSTICAS
# ===========================================================


@dataclass
class SyncStats:

    nome: str

    inseridos: int = 0
    atualizados: int = 0
    restaurados: int = 0
    removidos: int = 0

    def imprimir(self):

        total = (
            self.inseridos
            + self.atualizados
            + self.removidos
        )

        print("\n" + "=" * 65)
        print(self.nome)
        print("=" * 65)

        print(f"✔ Inseridos   : {self.inseridos}")
        print(f"✔ Atualizados : {self.atualizados}")
        print(f"✔ Removidos   : {self.removidos}")
        print(f"Total         : {total}")


# ===========================================================
# FUNÇÕES AUXILIARES
# ===========================================================


def copiar_campos(origem, destino):
    """
    Copia automaticamente todos os campos
    exceto a chave primária.
    """

    mapper = inspect(origem.__class__)

    for coluna in mapper.columns:

        if coluna.key == "id":
            continue

        setattr(
            destino,
            coluna.key,
            getattr(origem, coluna.key)
        )


def criar_dicionario(session, modelo):
    """
    Retorna:

    {
        id: objeto
    }

    Muito mais rápido do que fazer
    SELECT para cada registro.
    """

    return {
        registro.id: registro
        for registro in session.query(modelo).all()
    }


def corrigir_sequence(nome_tabela):

    sql = text(f"""
        SELECT setval(
            pg_get_serial_sequence(:tabela,'id'),
            COALESCE(
                (SELECT MAX(id) FROM {nome_tabela}),
                1
            ),
            true
        )
    """)

    postgres.execute(
        sql,
        {
            "tabela": nome_tabela
        }
    )


def corrigir_sequences():

    print("\n")
    print("=" * 65)
    print("Corrigindo Sequences...")
    print("=" * 65)

    tabelas = [
        "ubs",
        "medicamentos",
        "estoques",
        "movimentacoes"
    ]

    for tabela in tabelas:

        corrigir_sequence(tabela)

        print(f"✔ {tabela}")

# ===========================================================
# SINCRONIZAÇÃO GENÉRICA
# ===========================================================

def sincronizar_generico(modelo, nome_tabela):

    print()
    print("=" * 65)
    print(f"Sincronizando {nome_tabela}")
    print("=" * 65)

    stats = SyncStats(nome_tabela)

    # Carrega tudo uma única vez

    mysql_dict = criar_dicionario(mysql, modelo)
    postgres_dict = criar_dicionario(postgres, modelo)

    # ======================================================
    # INSERIR / ATUALIZAR / RESTAURAR
    # ======================================================

    for id_registro, registro_mysql in mysql_dict.items():

        registro_pg = postgres_dict.get(id_registro)

        # ----------------------------------------------
        # NÃO EXISTE NO POSTGRES
        # ----------------------------------------------

        
        
        
        if registro_pg is None:

            novo = modelo()

            copiar_campos(
                registro_mysql,
                novo
            )

            # mantém o mesmo ID do MySQL
            novo.id = registro_mysql.id

            postgres.add(novo)

            stats.inseridos += 1

            continue

        # ----------------------------------------------
        # COMPARAR CAMPOS
        # ----------------------------------------------

        alterou = False

        for coluna in modelo.__table__.columns:

            if coluna.name == "id":
                continue

            if getattr(registro_mysql, coluna.name) != getattr(registro_pg, coluna.name):

                alterou = True
                break

        if alterou:

            copiar_campos(
                registro_mysql,
                registro_pg
            )

            stats.atualizados += 1

    # ======================================================
    # REMOVER DO POSTGRES O QUE NÃO EXISTE MAIS NO MYSQL
    # ======================================================

    mysql_ids = set(mysql_dict.keys())

    for id_registro, registro_pg in postgres_dict.items():

        if id_registro not in mysql_ids:

            postgres.delete(registro_pg)

            stats.removidos += 1

    return stats


# ===========================================================
# SINCRONIZA TODAS AS TABELAS
# ===========================================================

def sincronizar_banco():

    relatorio = []

    relatorio.append(
        sincronizar_generico(
            UBS,
            "UBS"
        )
    )

    relatorio.append(
        sincronizar_generico(
            Medicamento,
            "Medicamentos"
        )
    )

    relatorio.append(
        sincronizar_generico(
            Estoque,
            "Estoques"
        )
    )

    relatorio.append(
        sincronizar_generico(
            Movimentacao,
            "Movimentações"
        )
    )

    return relatorio


try:

    relatorio = sincronizar_banco()

    corrigir_sequences()

    postgres.flush()

    postgres.expire_all()

    postgres.commit()

    print()

    print("=" * 65)
    print("RESUMO")
    print("=" * 65)

    for item in relatorio:

        item.imprimir()

    fim = time.perf_counter()

    print()
    print("=" * 65)
    print("SINCRONIZAÇÃO FINALIZADA")
    print("=" * 65)

    print(f"Tempo total: {fim-inicio:.2f} segundos")

except Exception as erro:

    postgres.rollback()

    print()
    print("=" * 65)
    print("ERRO")
    print("=" * 65)

    print(type(erro).__name__)
    print(erro)

finally:

    mysql.close()
    postgres.close()

    print("\nConexões encerradas.")