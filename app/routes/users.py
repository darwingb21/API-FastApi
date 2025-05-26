from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, crud, security
from ..database import get_db
from typing import Optional


router = APIRouter(prefix="/clientes", tags=["clientes"])

credentials_exception_administrator = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials the user is not an administrator",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/", response_model=schemas.Usuario)
def crear_usuario(
    usuario: schemas.UsuarioCreate, 
    db: Session = Depends(get_db), 
    current_user: schemas.Usuario = Depends(security.get_current_user)
    ):
    if current_user.administrador == 0:
        raise credentials_exception_administrator

    db_usuario = crud.get_usuario_por_email(db, email=usuario.email)
    if db_usuario:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    
    db_usuario_cpf = crud.get_usuario_por_cpf(db, cpf=usuario.cpf)
    if db_usuario_cpf:
        raise HTTPException(status_code=400, detail="CPF ya registrado")    
    
    return crud.crear_usuario(db=db, usuario=usuario)

@router.get("/", response_model=list[schemas.Usuario])
def leer_usuarios(
    skip: int = 0, 
    limit: int = 100,
    email: Optional[str] = None,
    nombre: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: schemas.Usuario = Depends(security.get_current_user)
    ):
    


    usuarios = crud.get_usuarios(db, skip=skip, limit=limit, email=email, nombre=nombre)
    if usuarios is None or len(usuarios) == 0:
        raise HTTPException(status_code=404, detail="Usuario(s) no encontrado")
    return usuarios

@router.get("/{usuario_id}", response_model=schemas.Usuario)
def leer_usuario(
    usuario_id: int, 
    db: Session = Depends(get_db),
    current_user: schemas.Usuario = Depends(security.get_current_user)
    ):
    
    db_usuario = crud.get_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario


@router.put("/{user_id}", response_model=schemas.Usuario)
def actualizar_usuario(
    user_id: int,
    usuario: schemas.UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.Usuario = Depends(security.get_current_user)
):
    if current_user.administrador == 0:
        raise credentials_exception_administrator
    
    print(11)
    db_usuario = crud.get_usuario_por_email(db, email=usuario.email)
    if db_usuario:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    
    db_usuario = crud.get_usuario_por_cpf(db, cpf=usuario.cpf)
    if db_usuario:
        raise HTTPException(status_code=400, detail="CPF ya registrado")

    db_usuario = crud.actualizar_usuario(db, user_id=user_id, usuario=usuario)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario


@router.delete("/{user_id}")
def eliminar_producto(user_id: int, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(security.get_current_user)):
    
    if current_user.administrador == 0:
        raise credentials_exception_administrator
    
    success = crud.eliminar_usuario(db, user_id=user_id)

    if not success:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado correctamente"}