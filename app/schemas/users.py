from pydantic import BaseModel, EmailStr
from typing import Optional

class UsuarioBase(BaseModel):
    email: EmailStr
    nombre: str
    cpf: str
    administrador: int

class UsuarioPassword(BaseModel):
    email: EmailStr
    password: str

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioUpdate(UsuarioBase):
    email: Optional[EmailStr] = None 
    nombre: Optional[str] = None
    cpf: Optional[str] = None
    administrador: Optional[int] = None

class Usuario(UsuarioBase):
    id: int

    class Config:
        orm_mode = True

class UsuarioInDB(Usuario):
    hashed_password: str