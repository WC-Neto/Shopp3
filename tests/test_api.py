import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_home_status_200():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"mensagem": "API Shopp3 rodando com sucesso!"}


def test_listar_produtos_publico_200():
    response = client.get("/produtos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_listar_lojas_publico_200():
    response = client.get("/lojas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_criar_loja_sem_token_401():
    payload = {
        "nome_fantasia": "Loja Teste Sem Token",
        "endereco": "Rua Principal, 100",
        "telefone": "11999999999"    }
    response = client.post("/lojas/", json=payload)
    assert response.status_code == 401

def test_fluxo_autenticado_criar_loja_201():
    user_payload = {"email": "teste@shopp3.com", "senha": "123456"}
    res_user = client.post("/usuarios/", json=user_payload)
    assert res_user.status_code == 201

    login_data = {"username": "teste@shopp3.com", "password": "123456"}
    res_login = client.post("/login", data=login_data)
    assert res_login.status_code == 200
    token = res_login.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    loja_payload = {
        "nome_fantasia": "Padaria Central",
        "endereco": "Av. Brasil, 50",
        "whatsapp": "67999998888",
        "categoria": "Alimentos",
        "id": 0
    }
    res_loja = client.post("/lojas/", json=loja_payload, headers=headers)
    assert res_loja.status_code == 201
    assert res_loja.json()["nome_fantasia"] == "Padaria Central"


def test_deletar_produto_inexistente_404():
    login_data = {"username": "teste@shopp3.com", "password": "123456"}
    res_login = client.post("/login", data=login_data)
    token = res_login.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete("/produtos/99999", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Produto não encontrado"