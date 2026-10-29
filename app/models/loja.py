"""from sqlalchemy import Column, Integer, String
from app.database import Base

class LojaModel(Base):
    __tablename__ = "lojas"

    id = Column(Integer, primary_key=True, index=True)
    
    nome_fantasia = Column(String, index=True, nullable=False)
    endereco = Column(String, nullable=False)
    whatsapp = Column(String, nullable=False) 
    categoria = Column(String, nullable=True) """