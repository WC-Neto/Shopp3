from fastapi import FastAPI
from app.database import engine, Base 
from app.models import product, store, user

from app.routers import (
    product_router,
    store_router,
    user_create_router,
    user_login_router
)

Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "Autenticação",
        "description": "Geração de tokens JWT para acesso às rotas protegidas.",
    },
    {
        "name": "Usuários",
        "description": "Cadastro e gerenciamento de contas de usuários na plataforma.",
    },
    {
        "name": "Lojas",
        "description": "Consulta pública e administração de estabelecimentos parceiros.",
    },
    {
        "name": "Produtos",
        "description": "Vitrine de produtos locais: listagem pública e gerenciamento autenticado.",
    },
]

app = FastAPI(
    title="API Shopp3 - Vitrine Local",
    description="Backend para conectar moradores ao comércio da cidade com autenticação OAuth2/JWT.",
    version="1.0.0",
    openapi_tags=tags_metadata
)

app.include_router(product_router.router)
app.include_router(store_router.router)
app.include_router(user_create_router.router)
app.include_router(user_login_router.router)

@app.get("/", summary="Status da API", tags=["Status"])
def home():
    """Verifica se a API Shopp3 está online e respondendo corretamente."""
    return {"mensagem": "API Shopp3 rodando com sucesso!"}