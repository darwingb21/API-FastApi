from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from .. import schemas, crud, security, database
from ..database import get_db


router = APIRouter(tags=["autenticación"])

@router.post("/auth/register", response_model=schemas.Usuario)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = crud.get_usuario_por_email(db, email=usuario.email)
    if db_usuario:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    
    db_usuario_cpf = crud.get_usuario_por_cpf(db, cpf=usuario.cpf)
    if db_usuario_cpf:
        raise HTTPException(status_code=400, detail="CPF ya registrado") 
    
    return crud.crear_usuario(db=db, usuario=usuario)


@router.post("/auth/login", response_model=schemas.Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):
    user = crud.authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    db_usuario = crud.get_usuario_por_email(db, email=form_data.username)
    if db_usuario:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    
    db_usuario_cpf = crud.get_usuario_por_cpf(db, cpf=form_data.cpf)
    if db_usuario_cpf:
        raise HTTPException(status_code=400, detail="CPF ya registrado")


    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=security.REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    refresh_token = security.create_refresh_token(
        data={"sub": user.email}, expires_delta=refresh_token_expires
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/auth/refresh-token", response_model=schemas.Token)
async def refresh_token(refresh_token: schemas.TokenRefresh, db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(refresh_token.refresh_token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        if payload.get("type") != "refresh":
            raise credentials_exception
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        print("JWTError occurred")
        raise credentials_exception
    
    user = crud.get_usuario_por_email(db, email=email)
    if user is None:
        raise credentials_exception
    
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    new_refresh_token = security.create_refresh_token(
        data={"sub": user.email}, expires_delta=timedelta(days=security.REFRESH_TOKEN_EXPIRE_MINUTES)
    )
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }