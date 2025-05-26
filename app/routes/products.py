from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, crud, security
from ..database import get_db
from typing import Optional

router = APIRouter(prefix="/products", tags=["products"])

credentials_exception_administrator = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials the user is not an administrator",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/", response_model=schemas.Producto, status_code=status.HTTP_201_CREATED)
async def crear_producto(
    producto: schemas.ProductoBase, 
    db: Session = Depends(get_db) , 
    current_user: schemas.Usuario = Depends(security.get_current_user)
):
    
    db_producto = crud.get_producto_por_codigo_barras(db, codigo_barras=producto.codigo_barras)
    if db_producto:
        raise HTTPException(status_code=400, detail="Codigo barras ya registrado")
    return crud.crear_producto(db=db, producto=producto) 

@router.get("/", response_model=list[schemas.Producto])
def listar_productos(
    skip: int = 0,
    limit: int = 100,
    seccion: Optional[str] = None,
    min_precio: Optional[float] = None,
    max_precio: Optional[float] = None,
    disponible: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: schemas.Usuario = Depends(security.get_current_user)
):
    return crud.get_productos(
        db,
        skip=skip,
        limit=limit,
        seccion=seccion,
        min_precio=min_precio,
        max_precio=max_precio,
        disponible=disponible
    )

@router.get("/{producto_id}", response_model=schemas.Producto )
def obtener_producto(producto_id: int, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(security.get_current_user)  ):
    
        
    db_producto = crud.get_producto(db, producto_id=producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

@router.put("/{producto_id}", response_model=schemas.Producto)
def actualizar_producto(
    producto_id: int,
    producto: schemas.ProductoUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.Usuario = Depends(security.get_current_user)
):
    
    if current_user.administrador == 0:
        raise credentials_exception_administrator
    
    db_producto = crud.get_producto_por_codigo_barras(db, codigo_barras=producto.codigo_barras)

    if db_producto:
        raise HTTPException(status_code=400, detail="Codigo barras ya registrado")

    db_producto = crud.actualizar_producto(db, producto_id=producto_id, producto=producto)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

@router.delete("/{producto_id}")
def eliminar_producto(producto_id: int, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(security.get_current_user)):
    
    if current_user.administrador == 0:
        raise credentials_exception_administrator
    
    success = crud.eliminar_producto(db, producto_id=producto_id)

    if not success:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": "Producto eliminado correctamente"}