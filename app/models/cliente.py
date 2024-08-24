from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(String, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    data_hora_aquisicao = Column(String, nullable=False)
    plano_atual_id = Column(String, ForeignKey('planos.id'), nullable=True)
    oferta_id = Column(String, nullable=True)
    email = Column(String, unique=True, index=True)
    ativo = Column(Boolean, default=True, nullable=False)

    # Relacionamento com o modelo Plano
    plano_atual = relationship("Plano", back_populates="clientes")
