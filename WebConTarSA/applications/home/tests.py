from django.test import TestCase
import pytest
from .models import *

@pytest.mark.django_db
def test_usuario_creacion():
    usuario = Usuario.objects.create_user(
        usuario = 'Test1',
        contraseña = '123321',
        nombres = 'Raúl Román',
        apellidos = 'Romero Riveroa',
        rut = '12345678-9',
        correo = 'test1@gmail.com',
        celular = '+56987654321',
        calle_id_calle = 1,
        jerarquia_id_jerarquia = 1,
        rol_id_rol = 1,
        unidad_id_unidad = 1
    )
    assert usuario.usuario == 'Test1'