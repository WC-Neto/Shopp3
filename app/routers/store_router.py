from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.store import LojaCreate, LojaResponse
from app.models.store import LojaModel
from app.database import get_db
from app.core.security import obter_usuario_atual

router = APIRouter(
    prefix="/lojas",
    tags=["Lojas"]
)

@router.get(
    "/",
    response_model=List[LojaResponse],
    summary="Listar todas as lojas",
    response_description="Lista de lojas parceiras cadastradas"
)
def listar_lojas(db: Session = Depends(get_db)):
    """Retorna todas as lojas parceiras cadastradas no Shopp3 (acesso público)."""
    return db.query(LojaModel).all()

@router.post(
    "/",
    response_model=LojaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar nova loja",
    response_description="Loja cadastrada com sucesso"
)
def cadastrar_loja(
    loja: LojaCreate, 
    db: Session = Depends(get_db),
    usuario_logado: str = Depends(obter_usuario_atual) 
):
    """
    Registra um novo estabelecimento comercial na plataforma.
    
    - **Requer autenticação:** Token JWT válido.
    """
    db_loja = LojaModel(**loja.model_dump())
    db.add(db_loja)
    db.commit()
    db.refresh(db_loja) 
    return db_loja

@router.put(
    "/{loja_id}",
    response_model=LojaResponse,
    summary="Atualizar dados da loja",
    response_description="Dados da loja atualizados"
)
def atualizar_loja(
    loja_id: int, 
    loja_dados: LojaCreate, 
    db: Session = Depends(get_db),
    usuario_logado: str = Depends(obter_usuario_atual) 
):
    """
    Atualiza o cadastro de uma loja existente pelo `loja_id`.
    
    - **Requer autenticação:** Token JWT válido.
    - **Erro 404:** Caso a loja não seja encontrada.
    """
    db_loja = db.query(LojaModel).filter(LojaModel.id == loja_id).first()
    if not db_loja:
        raise HTTPException(status_code=404, detail="Loja não encontrada")
    
    for chave, valor in loja_dados.model_dump().items():
        setattr(db_loja, chave, valor)
    
    db.commit()
    db.refresh(db_loja)
    return db_loja

@router.delete(
    "/{loja_id}",
    summary="Remover loja",
    response_description="Confirmação de exclusão da loja"
)
def deletar_loja(
    loja_id: int, 
    db: Session = Depends(get_db),
    usuario_logado: str = Depends(obter_usuario_atual) 
):
    """
    Remove uma loja parceira do banco de dados pelo `loja_id`.
    
    - **Requer autenticação:** Token JWT válido.
    - **Erro 404:** Caso a loja não seja encontrada.
    """
    db_loja = db.query(LojaModel).filter(LojaModel.id == loja_id).first()
    if not db_loja:
        raise HTTPException(status_code=404, detail="Loja não encontrada")
    
    db.delete(db_loja)
    db.commit()
    return {"mensagem": "Loja removida com sucesso!"}