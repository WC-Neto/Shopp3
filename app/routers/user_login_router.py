from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import UsuarioModel
from app.schemas.user import Token
from app.core.security import verificar_senha, criar_token_acesso

router = APIRouter(tags=["Autenticação"])

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Procura usuário pelo email (OAuth2 envia no campo 'username')
    usuario = db.query(UsuarioModel).filter(UsuarioModel.email == form_data.username).first()
    
    if not usuario or not verificar_senha(form_data.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Gerar token JWT
    access_token = criar_token_acesso(dados={"sub": usuario.email})
    return {"access_token": access_token, "token_type": "bearer"}