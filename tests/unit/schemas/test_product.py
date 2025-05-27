from app.schemas import ProductoBase, ProductoUpdate
import pytest



def test_producto_create_valid():

    producto = ProductoBase(

        descripcion= "description example",
        valor_venta= 550.50,
        codigo_barras= "1234567890123",
        seccion= "cocina",
        stock= 10,
        disponible= True,
        fecha_validez= "2024-12-31",
        imagen_url= "http://example.com/image.jpg"
    )

    assert producto.codigo_barras == "1234567890123"
    assert producto.valor_venta == 550.50
    assert producto.stock == 10
    assert producto.imagen_url == "http://example.com/image.jpg"



def test_producto_update():
    producto = ProductoUpdate(

        descripcion= "nueva descripcion",
        valor_venta= 1000,
        stock= 50,
    )

    assert producto.valor_venta == 1000
    assert producto.stock == 50
    assert producto.descripcion == "nueva descripcion"
    assert producto.codigo_barras  is None
    assert producto.imagen_url is None

