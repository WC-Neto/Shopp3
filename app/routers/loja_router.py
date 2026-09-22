from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.loja import LojaCreate, LojaResponse
from app.models.loja import LojaModel
from app.database import get_db

# Instancia o roteador para concentrar tudo relacionado a /lojas
router = APIRouter(
    prefix="/lojas",
    tags=["Lojas"]
)

@router.get("/", response_model=List[LojaResponse])
def listar_lojas(db: Session = Depends(get_db)):
    """Busca e retorna todas as lojas cadastradas na cidade."""
    lojas = db.query(LojaModel).all()
    return lojas

@router.post("/", response_model=LojaResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_loja(loja: LojaCreate, db: Session = Depends(get_db)):
    """Cadastra uma nova loja parceira no Shopp3."""
    # 1. Converte o JSON do Pydantic no modelo do Banco (SQLAlchemy)
    db_loja = LojaModel(**loja.model_dump())
    
    # 2. Grava no banco
    db.add(db_loja)
    db.commit()
    db.refresh(db_loja) # Pega o ID gerado automaticamente
    
    return db_loja