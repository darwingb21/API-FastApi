
from app.schemas import UsuarioCreate, UsuarioUpdate
import pytest


def test_usuario_create_valid():
    user = UsuarioCreate(
        email="Adrian@example.com",
        nombre="Test",
        cpf="12345678901",
        administrador=0,
        password="secret"
    )
    assert user.email == "Adrian@example.com"
    assert user.administrador == 0

def test_usuario_update_partial_1():
    user = UsuarioUpdate(
        nombre="Nuevo nombre",
        administrador=1
    )
    assert user.nombre == "Nuevo nombre"
    assert user.administrador == 1
    assert user.email is None
    assert user.cpf is None

def test_usuario_create_invalid_email():
    with pytest.raises(ValueError):
        UsuarioCreate(
            email="not-an-email",
            nombre="Test",
            cpf="12345678901",
            administrador=0,
            password="secret"
        )   