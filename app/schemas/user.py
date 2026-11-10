from pydantic import BaseModel, EmailStr

class UsuarioCreate(BaseModel):
    email: EmailStr
    senha: str

class UsuarioResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True  # Permite converter objetos do SQLAlchemy para Pydantic

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

    