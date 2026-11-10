from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db  # Tua dependência de sessão do banco
from app.models.user import UsuarioModel
from app.schemas.user import UsuarioCreate, UsuarioResponse
from app.core.security import gerar_hash_senha

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # 1. Verificar se o e-mail já existe
    usuario_existente = db.query(UsuarioModel).filter(UsuarioModel.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este e-mail já está cadastrado."
        )
    
    # 2. Gerar a hash da senha
    senha_criptografada = gerar_hash_senha(usuario.senha)
    
    # 3. Criar e salvar o novo usuário
    novo_usuario = UsuarioModel(
        email=usuario.email,
        senha_hash=senha_criptografada
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    
    return novo_usuario