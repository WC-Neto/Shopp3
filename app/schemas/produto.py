from pydantic import BaseModel
from typing import Optional

class ProdutoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float
    categoria: str
    em_estoque: bool = True

class ProdutoCreate(ProdutoBase):
    """Schema usado para a criação de um produto (o cliente envia estes dados)."""
    pass

class ProdutoResponse(ProdutoBase):
    """Schema usado para responder ao cliente (inclui o ID gerado pelo banco)."""
    id: int
    loja_id: int

    class Config:
        from_attributes = True