from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.produto import ProdutoCreate, ProdutoResponse
from app.models.produto import ProdutoModel
from app.database import get_db

router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"]
)

@router.get("/", response_model=List[ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    """Busca todos os produtos salvos no Banco de Dados."""
    produtos = db.query(ProdutoModel).all()
    return produtos

@router.post("/", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    """Salva um novo produto no Banco de Dados."""
    # Transforma o Schema Pydantic em um Modelo SQLAlchemy
    db_produto = ProdutoModel(**produto.model_dump())
    
    # Salva no banco de dados
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)  # Atualiza a instância com o ID gerado pelo banco
    
    return db_produto