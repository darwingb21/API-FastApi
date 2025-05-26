from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..database import Base

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String, index=True)
    valor_venta = Column(Float)
    codigo_barras = Column(String, unique=True, index=True)
    seccion = Column(String)
    stock = Column(Integer)
    fecha_validez = Column(String, default="0000-00-00")
    disponible = Column(Boolean, default=True)
    imagen_url = Column(String, default="www.img.com/test.png")
