from fastapi import FastAPI
from app.database import engine, Base 
from app.models import product, store, user

# Importando os roteadores da pasta app/routers/
from app.routers import (
    product_router,
    store_router,
    user_create_router,
    user_login_router
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Shopp3 - Vitrine Local",
    description="Backend para conectar moradores ao comércio da cidade.",
    version="1.0.0"
)


app.include_router(product_router.router)
app.include_router(store_router.router)
app.include_router(user_create_router.router)
app.include_router(user_login_router.router)

@app.get("/")
def home():
    return {"mensagem": "API Shopp3 rodando com sucesso!"}