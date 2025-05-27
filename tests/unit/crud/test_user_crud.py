from app.schemas import UsuarioCreate, UsuarioUpdate
from app.models import Usuario
from app.crud import (
    crear_usuario,
    get_usuario_por_email,
    get_usuario_por_cpf,
    get_usuario,
    get_usuarios,
    actualizar_usuario,
    eliminar_usuario
)
import pytest


def test_crear_usuario(db):
    # Datos de prueba
    user_data = UsuarioCreate(
        email="test@example.com",
        nombre="Nombre de prueba",
        cpf="12345678901",
        administrador=0,
        password="secret"
    )

   
    user = crear_usuario(db, user_data)

    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.nombre == "Nombre de prueba"
    assert user.cpf == "12345678901"
    assert user.administrador == 0



#######################################################################


def test_get_usuario_por_email(db):
    
    test_email = "test@example.com"

    user_data = Usuario(
        email=test_email,
        nombre="CPF Test",
        password="hashedpass",
        cpf="12345678901",
        administrador=0
    )
    db.add(user_data)
    db.commit()
    db.refresh(user_data)

    user = get_usuario_por_email(db, test_email)
    assert user is not None
    assert user.email == test_email
 
    # email que no existe
    assert get_usuario_por_cpf(db, "Otroemail@example.com") is None



#######################################################################



def test_get_usuario_por_cpf(db):
    
    test_cpf = "99988877766"

    user_data = Usuario(
        email="cpftest@example.com",
        nombre="CPF Test",
        password="hashedpass",
        cpf=test_cpf,
        administrador=1
    )

    db.add(user_data)
    db.commit()
    db.refresh(user_data)

    user = get_usuario_por_cpf(db, test_cpf)
    assert user is not None
    assert user.cpf == test_cpf
    
    # CPF que no existe
    assert get_usuario_por_cpf(db, "00000000000") is None


#######################################################################



def test_get_usuario(db):

    user_data = Usuario(
    email="test@example.com",
    nombre="Nombre de prueba",
    password="hashedpass",
    cpf="12345678901",
    administrador=0
    )

    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    

    test_user = get_usuario(db, user_data.id)
    assert test_user is not None
    assert user_data.email == test_user.email
    assert user_data.nombre == test_user.nombre
    assert user_data.cpf == test_user.cpf
    assert user_data.id == test_user.id


#######################################################################


def test_get_usuarios(db):
    # varios usuarios de prueba

    user1_data = Usuario( email="user1@example.com", nombre="User 1", password="hashedpass",
                                cpf="11111111111", administrador=0
    )

    user2_data = Usuario( email="user2@example.com", nombre="User 2", password="hashedpass",
                                cpf="22222222222", administrador=0
    )

    user3_data = Usuario( email="user3Admin@example.com", nombre="User 3", password="hashedpass",
                                cpf="33333333333", administrador=1
    )

    db.add(user1_data)
    db.add(user2_data)
    db.add(user3_data)    
    db.commit()
 
   
    users = get_usuarios(db)
    assert len(users) == 3
    
    # Probar con límite
    assert len(get_usuarios(db, limit=2)) == 2
    
    # Probar filtro por email
    filtered = get_usuarios(db, email="user3Admin@example.com")
    assert len(filtered) == 1
    assert filtered[0].nombre == "User 3"
    
    # Probar filtro por nombre
    filtered = get_usuarios(db, nombre="User 1")
    assert len(filtered) == 1
    assert filtered[0].email == "user1@example.com"



#######################################################################


def test_actualizar_usuario(db):

    nombre_original = "nombre original"
    nombre_actualizado = "nombre actualizado"
    email="original@example.com"
    
    test_user_data = Usuario(
        email=email,
        nombre= nombre_original,
        password="hashedpass",
        cpf="55555555555",
        administrador=0
    )

    db.add(test_user_data)
    db.commit()
    db.refresh(test_user_data)
    
    # Datos de actualización
    update_data = UsuarioUpdate(
        nombre= nombre_actualizado,
        administrador=1
    )

    # Actualizar
    updated_user = actualizar_usuario(db, test_user_data.id, update_data)
    
    assert updated_user is not None
    assert updated_user.nombre == nombre_actualizado
    assert updated_user.administrador == 1
    assert updated_user.email == email  # No debería cambiar
    
    user = get_usuario_por_email(db, email)
    assert user.nombre == nombre_actualizado



#######################################################################


def test_eliminar_usuario(db):
    # Crear usuario para eliminar
    test_user = Usuario(
        email="example@example.com",
        nombre="user",
        password="hashedpass",
        cpf="66666666666",
        administrador=0
    )
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    user_id = test_user.id
    
    # Eliminar
    result = eliminar_usuario(db, user_id)
    assert result is True
    
    # Verificar que ya no existe
    assert db.query(Usuario).filter(Usuario.id == user_id).first() is None
    
    # Probar eliminar usuario que no existe
    assert eliminar_usuario(db, 999999) is False