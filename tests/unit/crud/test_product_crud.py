from app.schemas import ProductoBase, ProductoUpdate
from app.models import Producto
from app.crud import (
    crear_producto,
    get_producto_por_codigo_barras,
    get_producto,
    get_productos,
    actualizar_producto,
    eliminar_producto
)
import pytest



def test_crear_producto(db):
    # Datos de prueba
    producto_data = ProductoBase(
        descripcion= "description example",
        valor_venta= 550.50,
        codigo_barras= "1234567890123",
        seccion= "cocina",
        stock= 10,
        disponible= True,
        fecha_validez= "2024-12-31",
        imagen_url= "www.miexample.com/image.jpg"
    )

   
    producto = crear_producto(db, producto_data)

    assert producto.id is not None
    assert producto.descripcion == "description example"
    assert producto.codigo_barras == "1234567890123"
    assert producto.seccion == "cocina"
    assert producto.valor_venta == 550.50
    assert producto.stock == 10
    assert producto.disponible == True
    assert producto.imagen_url == "www.miexample.com/image.jpg"
    assert producto.fecha_validez == "2024-12-31"


#######################################################################


def test_get_producto_por_codigo_barras(db):
    
    test_codigo_barras = "1234567890123"

    producto_data = Producto(
        descripcion= "description example",
        valor_venta= 550.50,
        codigo_barras= "1234567890123",
        seccion= "cocina",
        stock= 10,
        disponible= True,
        fecha_validez= "2024-12-31",
        imagen_url= "www.miexample.com/image.jpg"
    )

    db.add(producto_data)
    db.commit()
    db.refresh(producto_data)

    producto = get_producto_por_codigo_barras(db, test_codigo_barras)
    assert producto is not None
    assert producto.codigo_barras == test_codigo_barras
 
    # codigo barras que no existe
    assert get_producto_por_codigo_barras(db, "98765432198") is None



#######################################################################



def test_get_producto(db):

    producto_data = Producto(
        descripcion= "description example",
        valor_venta= 550.50,
        codigo_barras= "1234567890123",
        seccion= "cocina",
        stock= 10,
        disponible= True,
        fecha_validez= "2024-12-31",
        imagen_url= "www.miexample.com/image.jpg"
    )

    db.add(producto_data)
    db.commit()
    db.refresh(producto_data)
    

    producto_user = get_producto(db, producto_data.id)
    assert producto_user is not None
    assert producto_user.valor_venta == producto_data.valor_venta
    assert producto_user.codigo_barras == producto_data.codigo_barras
    assert producto_user.seccion == producto_data.seccion
    assert producto_user.imagen_url == producto_data.imagen_url
    assert producto_user.disponible == producto_data.disponible
    assert producto_user.stock == producto_data.stock

    
#######################################################################


def test_get_productos(db):
    
    # varios usuarios de prueba
    producto1_data = Producto(
        descripcion= "description prueba 1",
        valor_venta= 550.50,
        codigo_barras= "1111111111111",
        seccion= "Armas",
        stock= 10,
        disponible= True,
        fecha_validez= "2024-12-31",
        imagen_url= "www.miexample.com/image1.jpg"
    )

    producto2_data = Producto(
        descripcion= "description prueba 2",
        valor_venta= 1050.50,
        codigo_barras= "222222222222",
        seccion= "Tecnologia",
        stock= 0,
        disponible= False,
        fecha_validez= "2024-10-11",
        imagen_url= "www.miexample.com/image2.jpg"
    )

    producto3_data = Producto(
        descripcion= "description prueba 3",
        valor_venta= 75500,
        codigo_barras= "333333333333",
        seccion= "cocina",
        stock= 5,
        disponible= True,
        fecha_validez= "2024-11-01",
        imagen_url= "www.miexample.com/image3.jpg"
    )

    producto4_data = Producto(
        descripcion= "description prueba 4",
        valor_venta= 10,
        codigo_barras= "444444444444",
        seccion= "cocina",
        stock= 0,
        disponible= False,
        fecha_validez= "2024-01-01",
        imagen_url= "www.miexample.com/image4.jpg"
    )


    db.add(producto1_data)
    db.add(producto2_data)
    db.add(producto3_data)    
    db.add(producto4_data)  
    db.commit()
 
   
    users = get_productos(db)
    assert len(users) == 4
    
    # Probar con límite
    assert len(get_productos(db, limit=2)) == 2
    
    # Probar filtro por descripcion
    filtered = get_productos(db, seccion="cocina")
    assert len(filtered) == 2
    
    # Probar filtro por nombre
    filtered = get_productos(db, disponible=False)
    assert len(filtered) == 2
    assert filtered[0].stock == 0
    assert filtered[1].stock == 0


#######################################################################


def test_actualizar_producto(db):

    valor_venta_original = 20
    valor_venta_actualizado = 500
    stock_inicial = 10
    stock_actualizado = 5
    
    test_producto_data = Producto(
        descripcion= "descripcion elemento actualizar",
        valor_venta= valor_venta_original,
        codigo_barras= "1234455656789",
        seccion= "Tecnologia",
        stock= stock_inicial,
        disponible= False,
        fecha_validez= "2024-10-11",
        imagen_url= "www.miexample.com/image.jpg"
    )

    db.add(test_producto_data)
    db.commit()
    db.refresh(test_producto_data)
    
    # Datos de actualización
    update_data = ProductoUpdate(
        valor_venta= valor_venta_actualizado,
        stock=stock_actualizado
    )

    # Actualizar
    updated_producto = actualizar_producto(db, test_producto_data.id, update_data)
    
    assert updated_producto is not None
    assert updated_producto.valor_venta == valor_venta_actualizado
    assert updated_producto.stock == stock_actualizado
    


#######################################################################


def test_eliminar_producto(db):
    # Crear usuario para eliminar
    test_producto = Producto(
        descripcion= "description example",
        valor_venta= 550.50,
        codigo_barras= "1234567890123",
        seccion= "cocina",
        stock= 10,
        disponible= True,
        fecha_validez= "2024-12-31",
        imagen_url= "www.miexample.com/image.jpg"
    )
    db.add(test_producto)
    db.commit()
    db.refresh(test_producto)

    result = eliminar_producto(db, test_producto.id)
    assert result is True
    
    # Verificar que ya no existe
    assert db.query(Producto).filter(Producto.id == test_producto.id).first() is None
    
    # eliminar usuario que no existe
    assert eliminar_producto(db, 999999) is False