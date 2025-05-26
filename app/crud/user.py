from sqlalchemy.orm import Session
from .. import models, schemas, security

def get_usuario(db: Session, usuario_id: int):
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

def get_usuario_por_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def get_usuario_por_cpf(db: Session, cpf: str):
    return db.query(models.Usuario).filter(models.Usuario.cpf == cpf).first()

def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Usuario).offset(skip).limit(limit).all()

def crear_usuario(db: Session, usuario: schemas.UsuarioCreate):
    hashed_password = security.get_password_hash(usuario.password)
    db_usuario = models.Usuario(
        email=usuario.email,
        nombre=usuario.nombre,
        password=hashed_password,
        cpf=usuario.cpf,
        administrador=usuario.administrador
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario
