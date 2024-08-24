from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

class Oferta(Base):
    __tablename__ = "ofertas"

    id = Column(String, primary_key=True, index=True)
    descricao = Column(String, nullable=False)
    data_hora_criacao = Column(DateTime, default=datetime.utcnow, nullable=False)
    plano_id = Column(String, ForeignKey('planos.id'), nullable=True)
    valor = Column(Numeric(10, 2), nullable=False)  # Campo decimal
    moeda = Column(String, nullable=False)
