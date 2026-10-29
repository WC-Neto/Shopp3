"""import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Monta o caminho absoluto do arquivo do banco
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "shopp3.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# 2. Criamos o engine (com o argumento necessário para SQLite)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# 3. Criador de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Classe base para os modelos
Base = declarative_base()

# 5. Função utilitária para abrir/fechar sessão
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""