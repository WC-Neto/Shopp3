from pydantic import BaseModel
from typing import Optional

# 1. Base: Campos comuns a todas as operações de Loja
class LojaBase(BaseModel):
    nome_fantasia: str
    endereco: str
    whatsapp: str
    categoria: Optional[str] = None

# 2. Create: Dados necessários para CADASTRAR uma loja (o que o cliente envia)
class LojaCreate(LojaBase):
    pass

# 3. Response: Dados que a API DEVOLVE (inclui o ID que o banco gerou)
class LojaResponse(LojaBase):
    id: int

    class Config:
        from_attributes = True # Permite converter o modelo SQLAlchemy em Pydantic