from fastapi import APIRouter, Depends
from .. import schemas, security

router = APIRouter(tags=["protegidas"])

@router.get("/users/me/", response_model=schemas.Usuario)
async def read_users_me(current_user: schemas.Usuario = Depends(security.get_current_user)):
    return current_user