"""from sqlalchemy import Column, Integer, String, Float, Boolean
from app.database import Base

class ProdutoModel(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    descricao = Column(String, nullable=True)
    preco = Column(Float, nullable=False)
    categoria = Column(String, index=True, nullable=False)
    em_estoque = Column(Boolean, default=True)
    loja_id = Column(Integer, default=1)"""  