from typing import Optional
from pydantic import BaseModel

class ProductoBase(BaseModel):
    descripcion: str
    valor_venta: float
    codigo_barras: str
    seccion: str
    stock: int
    disponible: bool = True
    fecha_validez: str
    imagen_url: str


class ProductoUpdate(BaseModel):
    descripcion: Optional[str] = None
    valor_venta: Optional[float] = None
    seccion: Optional[str] = None
    stock: Optional[int] = None
    disponible: Optional[bool] = None
    fecha_validez: Optional[str] = None
    imagen_url: Optional[str] = None
    codigo_barras: Optional[str] = None

class Producto(ProductoBase):
    id: int

    class Config:
        orm_mode = True