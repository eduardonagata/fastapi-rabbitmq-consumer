from sqlalchemy import Column, String, ForeignKey, Numeric, DateTime, Enum
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime
import enum

# Definindo os valores para os Enums
class TipoMovimentacaoEnum(str, enum.Enum):
    ABERTURA = "ABERTURA"
    ENCERRAMENTO = "ENCERRAMENTO"

class MotivoMovimentacaoEnum(str, enum.Enum):
    NOVO = "NOVO"
    CANCELAMENTO = "CANCELAMENTO"
    UPGRADE = "UPGRADE"
    DOWNGRADE = "DOWNGRADE"

class Movimentacao(Base):
    __tablename__ = "movimentacoes"

    id = Column(String, primary_key=True, index=True, nullable=False)
    data_hora_efetivacao = Column(DateTime, nullable=False, default=datetime.utcnow)  # Armazena data/hora no formato ISO 8601 UTC
    cliente_id = Column(String, ForeignKey('clientes.id'), nullable=False)  # Referência para Cliente
    tipo_movimentacao = Column(Enum(TipoMovimentacaoEnum), nullable=False)  # Valores "ABERTURA" ou "ENCERRAMENTO"
    motivo_movimentacao = Column(Enum(MotivoMovimentacaoEnum), nullable=False)  # Valores "NOVO", "CANCELAMENTO", etc.
    plano_id = Column(String, ForeignKey('planos.id'), nullable=False)  # Referência para Plano
    valor = Column(Numeric(10, 2), nullable=False)  # Valor decimal obrigatório
    moeda = Column(String, nullable=False)  # Moeda obrigatória

    # Relacionamentos (Opcional)
    cliente = relationship("Cliente", backref="movimentacoes")
    plano = relationship("Plano", backref="movimentacoes")
