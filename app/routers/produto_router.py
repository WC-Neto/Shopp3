# from fastapi import APIRouter, Depends, status, HTTPException
# from sqlalchemy.orm import Session
# from typing import List

# from app.schemas.produto import ProdutoCreate, ProdutoResponse
# from app.models.produto import ProdutoModel
# from app.database import get_db

# router = APIRouter(
#     prefix="/produtos",
#     tags=["Produtos"]
# )

# @router.get("/", response_model=List[ProdutoResponse])
# def listar_produtos(db: Session = Depends(get_db)):
#     """Busca todos os produtos salvos no Banco de Dados."""
#     produtos = db.query(ProdutoModel).all()
#     return produtos

# @router.get("/busca", response_model=List[ProdutoResponse])
# def buscar_produtos(q: str, db: Session = Depends(get_db)):
#     """Busca produtos que contenham o termo 'q' no nome."""
#     produtos = db.query(ProdutoModel).filter(ProdutoModel.nome.contains(q)).all()
#     return produtos

# @router.post("/", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
# def cadastrar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
#     """Salva um novo produto no Banco de Dados."""
#     db_produto = ProdutoModel(**produto.model_dump())
    
#     db.add(db_produto)
#     db.commit()
#     db.refresh(db_produto)  # Atualiza a instância com o ID gerado pelo banco
    
#     return db_produto

# @router.put("/{produto_id}", response_model=ProdutoResponse)
# def atualizar_produto(produto_id: int, produto_dados: ProdutoCreate, db: Session = Depends(get_db)):
#     """Atualiza os dados de um produto existente no Banco de Dados."""
#     db_produto = db.query(ProdutoModel).filter(ProdutoModel.id == produto_id).first()
    
#     if not db_produto:
#         raise HTTPException(status_code=404, detail="Produto não encontrado")
    
#     for chave, valor in produto_dados.model_dump().items():
#         setattr(db_produto, chave, valor)
    
#     db.commit()
#     db.refresh(db_produto)
    
#     return db_produto

# @router.delete("/{produto_id}")
# def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
#     """Deleta um produto do Banco de Dados."""    
#     db_produto = db.query(ProdutoModel).filter(ProdutoModel.id == produto_id).first()
    
#     if not db_produto:
#         raise HTTPException(status_code=404, detail="Produto não encontrado")
    
#     db.delete(db_produto)
#     db.commit()
    
#     return {"mensagem": "Produto removido com sucesso!"}


from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.produto import ProdutoCreate, ProdutoResponse

router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"]
)

produtos_db = []


@router.get("/", response_model=List[ProdutoResponse])
def listar_produtos():
    """Busca todos os produtos salvos na memória."""
    return produtos_db


@router.get("/busca", response_model=List[ProdutoResponse])
def buscar_produtos(q: str):
    """Busca produtos que contenham o termo 'q' no nome."""
    resultados = [
        produto for produto in produtos_db 
        if q.lower() in produto["nome"].lower()
    ]
    return resultados


@router.get("/{produto_id}", response_model=ProdutoResponse)
def buscar_produto_por_id(produto_id: int):
    """Busca um produto específico pelo ID."""
    for produto in produtos_db:
        if produto["id"] == produto_id:
            return produto
    raise HTTPException(status_code=404, detail="Produto não encontrado")


@router.post("/", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_produto(produto: ProdutoCreate):
    """Salva um novo produto na memória."""
    novo_produto = produto.model_dump()
    novo_produto["id"] = len(produtos_db) + 1
    novo_produto["loja_id"] = 1  # 👈 Adicione esta linha!

    produtos_db.append(novo_produto)
    return novo_produto


@router.put("/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(produto_id: int, produto_dados: ProdutoCreate):
    """Atualiza os dados de um produto existente na memória."""
    for produto in produtos_db:
        if produto["id"] == produto_id:
            produto.update(produto_dados.model_dump())
            return produto
            
    raise HTTPException(status_code=404, detail="Produto não encontrado")


@router.delete("/{produto_id}")
def deletar_produto(produto_id: int):
    """Deleta um produto da memória."""
    for produto in produtos_db:
        if produto["id"] == produto_id:
            produtos_db.remove(produto)
            return {"mensagem": "Produto removido com sucesso!"}
            
    raise HTTPException(status_code=404, detail="Produto não encontrado")

