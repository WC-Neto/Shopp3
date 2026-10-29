"""from fastapi import FastAPI
from app.routers import produto_router
from app.database import engine, Base
from app.models import produto as produto_model
from app.models import produto as produto_model
from app.models import loja as loja_model
from app.routers import produto_router, loja_router
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Shopp3 - Vitrine Local",
    description="Backend para conectar moradores ao comércio da cidade.",
    version="1.0.0"
)

app.include_router(produto_router.router)
app.include_router(loja_router.router)

@app.get("/")
def home():
    return {"mensagem": "API Shopp3 rodando com sucesso!"}"""

from fastapi import FastAPI
from app.routers import produto_router, loja_router

app = FastAPI(
    title="API Shopp3 - Vitrine Local",
    description="Backend para conectar moradores ao comércio da cidade.",
    version="1.0.0"
)

app.include_router(produto_router.router)
app.include_router(loja_router.router)

@app.get("/")
def home():
    return {"mensagem": "API Shopp3 rodando com sucesso na memória!"}
