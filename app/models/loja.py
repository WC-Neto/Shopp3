from sqlalchemy import Column, Integer, String
from app.database import Base

class LojaModel(Base):
    __tablename__ = "lojas"

    # Chave primária: ID único para cada loja
    id = Column(Integer, primary_key=True, index=True)
    
    # Dados da Loja
    nome_fantasia = Column(String, index=True, nullable=False)
    endereco = Column(String, nullable=False)
    whatsapp = Column(String, nullable=False) # Ex: "67999998888"
    categoria = Column(String, nullable=True) # Ex: "Vestuário", "Autopeças"