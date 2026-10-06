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

@router.put("/{loja_id}", response_model=LojaResponse)
def atualizar_loja(loja_id: int, loja_dados: LojaCreate, db: Session = Depends(get_db)):
    """Atualiza os dados de uma loja parceira no Shopp3."""
    db_loja = db.query(LojaModel).filter(LojaModel.id == loja_id).first()
    
    if not db_loja:
        raise HTTPException(status_code=404, detail="Loja não encontrada")
    
    for chave, valor in loja_dados.model_dump().items():
        setattr(db_loja, chave, valor)
    
    db.commit()
    db.refresh(db_loja)
    
    return db_loja

@router.delete("/{loja_id}")
def deletar_loja(loja_id: int, db: Session = Depends(get_db)):
    db_loja = db.query(LojaModel).filter(LojaModel.id == loja_id).first()
    
    if not db_loja:
        raise HTTPException(status_code=404, detail="Loja não encontrada")
    
    db.delete(db_loja)
    
    db.commit()
    
    return {"mensagem": "Loja removida com sucesso!"}