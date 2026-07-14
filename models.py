from datetime import datetime
from extensions import db


class UBS(db.Model):
    """Unidade Básica de Saúde."""

    __tablename__ = "ubs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(200), nullable=False)
    endereco = db.Column(db.String(300), nullable=False)
    bairro = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(100), nullable=False, default="Macapá")
    telefone = db.Column(db.String(20))
    horario_funcionamento = db.Column(db.String(200))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    estoques = db.relationship(
        "Estoque",
        backref="ubs",
        lazy=True,
        cascade="all, delete-orphan"
    )

    movimentacoes = db.relationship(
        "Movimentacao",
        backref="ubs_ref",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "endereco": self.endereco,
            "bairro": self.bairro,
            "cidade": self.cidade,
            "telefone": self.telefone,
            "horario_funcionamento": self.horario_funcionamento,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }


class Medicamento(db.Model):
    """Catálogo de medicamentos."""

    __tablename__ = "medicamentos"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(200), nullable=False)
    principio_ativo = db.Column(db.String(200), nullable=False)
    dosagem = db.Column(db.String(50))
    fabricante = db.Column(db.String(200))
    descricao = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    estoques = db.relationship(
        "Estoque",
        backref="medicamento",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "principio_ativo": self.principio_ativo,
            "dosagem": self.dosagem,
            "fabricante": self.fabricante,
            "descricao": self.descricao,
        }


class Estoque(db.Model):
    """Estoque de medicamentos por UBS."""

    __tablename__ = "estoques"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    ubs_id = db.Column(
        db.Integer,
        db.ForeignKey("ubs.id"),
        nullable=False
    )

    medicamento_id = db.Column(
        db.Integer,
        db.ForeignKey("medicamentos.id"),
        nullable=False
    )

    quantidade = db.Column(db.Integer, nullable=False, default=0)
    lote = db.Column(db.String(100))
    validade = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    movimentacoes = db.relationship(
        "Movimentacao",
        backref="estoque",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,

            "ubs_id": self.ubs_id,
            "ubs_nome": self.ubs.nome if self.ubs else None,

            "medicamento_id": self.medicamento_id,
            "medicamento_nome": self.medicamento.nome if self.medicamento else None,

            "quantidade": self.quantidade,
            "lote": self.lote,
            "validade": self.validade.isoformat() if self.validade else None,
        }


class Movimentacao(db.Model):
    """Registro de entrada e saída de medicamentos."""

    __tablename__ = "movimentacoes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    estoque_id = db.Column(
        db.Integer,
        db.ForeignKey("estoques.id"),
        nullable=False
    )

    ubs_id = db.Column(
        db.Integer,
        db.ForeignKey("ubs.id"),
        nullable=True
    )

    tipo = db.Column(
    db.Enum(
        "Entrada",
        "Saída",
        name="tipo_movimentacao"
    ),
    nullable=False
)

    quantidade = db.Column(db.Integer, nullable=False)

    responsavel = db.Column(db.String(200))

    observacao = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,

            "estoque_id": self.estoque_id,

            "ubs_id": self.estoque.ubs.id if self.estoque and self.estoque.ubs else None,
            "ubs_nome": self.estoque.ubs.nome if self.estoque and self.estoque.ubs else None,

            "medicamento_id": self.estoque.medicamento.id if self.estoque and self.estoque.medicamento else None,
            "medicamento_nome": self.estoque.medicamento.nome if self.estoque and self.estoque.medicamento else None,

            "tipo": self.tipo,
            "quantidade": self.quantidade,
            "responsavel": self.responsavel,
            "observacao": self.observacao,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }