from sqlalchemy.orm import Session
from .. import security
from .user import get_usuario_por_email

def authenticate_user(db: Session, email: str, password: str):

    user = get_usuario_por_email(db, email)
    if not user:
        return False
    if not security.verify_password(password, user.password):
        return False

    return user