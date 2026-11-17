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

@router.get(
    "/",
    response_model=List[ProdutoResponse],
    summary="Listar todos os produtos",
    response_description="Lista de produtos cadastrados"
)
def listar_produtos(db: Session = Depends(get_db)):
    """Retorna todos os produtos disponíveis na vitrine (acesso público)."""
    return db.query(ProdutoModel).all()

@router.get(
    "/busca",
    response_model=List[ProdutoResponse],
    summary="Buscar produtos por nome",
    response_description="Lista de produtos filtrados pelo termo de busca"
)
def buscar_produtos(q: str, db: Session = Depends(get_db)):
    """Filtra produtos cujo nome contenha o termo informado no parâmetro `q` (acesso público)."""
    return db.query(ProdutoModel).filter(ProdutoModel.nome.contains(q)).all()

@router.post(
    "/",
    response_model=ProdutoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar novo produto",
    response_description="Produto criado com sucesso"
)
def cadastrar_produto(
    produto: ProdutoCreate, 
    db: Session = Depends(get_db),
    usuario_logado: str = Depends(obter_usuario_atual)
):
    """
    Cria e salva um novo produto no banco de dados.
    
    - **Requer autenticação:** Token JWT válido no cabeçalho `Authorization`.
    """
    db_produto = ProdutoModel(**produto.model_dump())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

@router.put(
    "/{produto_id}",
    response_model=ProdutoResponse,
    summary="Atualizar produto existente",
    response_description="Dados do produto atualizados"
)
def atualizar_produto(
    produto_id: int, 
    produto_dados: ProdutoCreate, 
    db: Session = Depends(get_db),
    usuario_logado: str = Depends(obter_usuario_atual)
):
    """
    Atualiza as informações de um produto pelo seu `produto_id`.
    
    - **Requer autenticação:** Token JWT válido.
    - **Erro 404:** Caso o ID não exista no banco.
    """
    db_produto = db.query(ProdutoModel).filter(ProdutoModel.id == produto_id).first()
    if not db_produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    for chave, valor in produto_dados.model_dump().items():
        setattr(db_produto, chave, valor)
    
    db.commit()
    db.refresh(db_produto)
    return db_produto

@router.delete(
    "/{produto_id}",
    summary="Remover produto",
    response_description="Confirmação de exclusão do produto"
)
def deletar_produto(
    produto_id: int, 
    db: Session = Depends(get_db),
    usuario_logado: str = Depends(obter_usuario_atual) 
):
    """
    Exclui permanentemente um produto pelo seu `produto_id`.
    
    - **Requer autenticação:** Token JWT válido.
    - **Erro 404:** Caso o ID não exista no banco.
    """
    db_produto = db.query(ProdutoModel).filter(ProdutoModel.id == produto_id).first()
    if not db_produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    db.delete(db_produto)
    db.commit()
    return {"mensagem": "Produto removido com sucesso!"}