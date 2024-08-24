from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Plano(Base):
    __tablename__ = "planos"

    id = Column(String, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    data_hora_criacao = Column(String, nullable=False)

    # Relacionamento com o modelo Cliente
    clientes = relationship("Cliente", back_populates="plano_atual")