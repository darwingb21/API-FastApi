from sqlalchemy.orm import Session
from .. import models, schemas
from datetime import datetime

def get_producto(db: Session, producto_id: int):
    return db.query(models.Producto).filter(models.Producto.id == producto_id).first()

def get_productos(db: Session, skip: int = 0, limit: int = 100, 
                 seccion: str = None, min_precio: float = None, 
                 max_precio: float = None, disponible: bool = None):
    query = db.query(models.Producto)
    
    if seccion:
        query = query.filter(models.Producto.seccion == seccion)
    if min_precio:
        query = query.filter(models.Producto.valor_venta >= min_precio)
    if max_precio:
        query = query.filter(models.Producto.valor_venta <= max_precio)
    if disponible is not None:
        query = query.filter(models.Producto.disponible == disponible)
    
    return query.offset(skip).limit(limit).all()


def get_producto_por_codigo_barras(db: Session, codigo_barras: str):
    return db.query(models.Producto).filter(models.Producto.codigo_barras == codigo_barras).first()

def crear_producto(db: Session, producto: schemas.ProductoBase):
    #db_producto = models.Producto(**producto.dict())
    db_producto = models.Producto(
        descripcion= producto.descripcion,
        valor_venta= producto.valor_venta,
        codigo_barras= producto.codigo_barras,
        seccion= producto.seccion,            
        stock=producto.stock,
        disponible= producto.disponible
    )
    db.add(db_producto)
    db.commit()
    
    db.refresh(db_producto)
 
    return db_producto

def actualizar_producto(db: Session, producto_id: int, producto: schemas.ProductoUpdate):
    db_producto = get_producto(db, producto_id)
    if not db_producto:
        return None
    
    update_data = producto.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_producto, key, value)
    
    db.commit()
    db.refresh(db_producto)
    return db_producto

def eliminar_producto(db: Session, producto_id: int):
    db_producto = get_producto(db, producto_id)
    if not db_producto:
        return False
    
    db.delete(db_producto)
    db.commit()
    return True