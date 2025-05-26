from pydantic import BaseModel, EmailStr

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


class Usuario(UsuarioBase):
    id: int

    class Config:
        orm_mode = True

class UsuarioInDB(Usuario):
    hashed_password: str