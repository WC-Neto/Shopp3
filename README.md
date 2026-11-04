# Shopp3 - API Vitrine Local 🛍️

Backend desenvolvido em **FastAPI** para conectar moradores ao comércio local.

---

## 👥 Integrantes da Dupla
* Walter Camargo Neto

---

## 🗄️ Persistência de Dados
O projeto utiliza persistência relacional com **SQLAlchemy** e **SQLite**. O controle e versionamento do esquema do banco de dados são gerenciados através de migrações com o **Alembic** 📦.

---

## 🚀 Como Executar o Projeto Localmente

### 1. Clonar o repositório e acessar a pasta:
```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd shopp3

1. Ativar o ambiente virtual e instalar dependências:
Bash
# No Windows:
.\venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
2. Executar as migrações do banco de dados (Alembic):
Bash
alembic upgrade head
3. Executar a aplicação FastAPI:
Bash
uvicorn main:app --reload
A documentação interativa estará disponível em: http://127.0.0.1:8000/docs
