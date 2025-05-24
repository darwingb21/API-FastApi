from pydantic import BaseModel, EmailStr

####
from typing import Optional
####


###
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class TokenRefresh(BaseModel):
    refresh_token: str
    
###

class UsuarioBase(BaseModel):
    email: EmailStr
    nombre: str

class UsuarioCreate(UsuarioBase):
    password: str

class Usuario(UsuarioBase):
    id: int

    class Config:
        orm_mode = True

##
# 

class UsuarioInDB(Usuario):
    hashed_password: str

#        