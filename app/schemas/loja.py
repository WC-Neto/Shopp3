from pydantic import BaseModel
from typing import Optional

class LojaBase(BaseModel):
    nome_fantasia: str
    endereco: str
    whatsapp: str
    categoria: Optional[str] = None

class LojaCreate(LojaBase):
    pass

class LojaResponse(LojaBase):
    id: int

    class Config:
        from_attributes = True 