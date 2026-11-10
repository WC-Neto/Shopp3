from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.product import ProdutoCreate, ProdutoResponse
from app.models.product import ProdutoModel
from app.database import get_db
from app.core.security import obter_usuario_atual

router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"]
)

@router.get("/", response_model=List[ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    """Busca todos os produtos salvos no Banco de Dados."""
    produtos = db.query(ProdutoModel).all()
    return produtos

@router.get("/busca", response_model=List[ProdutoResponse])
def buscar_produtos(q: str, db: Session = Depends(get_db)):
    """Busca produtos que contenham o termo 'q' no nome."""
    produtos = db.query(ProdutoModel).filter(ProdutoModel.nome.contains(q)).all()
    return produtos

@router.post("/", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_produto(
    produto: ProdutoCreate, 
    db: Session = Depends(get_db),
    usuario_logado: str = Depends(obter_usuario_atual) # 👈 AQUI nos parênteses!
):
    """Salva um novo produto no Banco de Dados."""
    db_produto = ProdutoModel(**produto.model_dump())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

@router.put("/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(
    produto_id: int, 
    produto_dados: ProdutoCreate, 
    db: Session = Depends(get_db),
    usuario_logado: str = Depends(obter_usuario_atual) # 👈 AQUI nos parênteses!
):
    """Atualiza os dados de um produto existente no Banco de Dados."""
    db_produto = db.query(ProdutoModel).filter(ProdutoModel.id == produto_id).first()
    
    if not db_produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    for chave, valor in produto_dados.model_dump().items():
        setattr(db_produto, chave, valor)
    
    db.commit()
    db.refresh(db_produto)
    return db_produto

@router.delete("/{produto_id}")
def deletar_produto(
    produto_id: int, 
    db: Session = Depends(get_db),
    usuario_logado: str = Depends(obter_usuario_atual) 
):
    """Deleta um produto do Banco de Dados."""    
    db_produto = db.query(ProdutoModel).filter(ProdutoModel.id == produto_id).first()
    
    if not db_produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    db.delete(db_produto)
    db.commit()
    return {"mensagem": "Produto removido com sucesso!"}