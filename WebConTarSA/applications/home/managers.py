#----------------------------------------------------------------------------------------------------------------#
# Importaciones necesarias
#----------------------------------------------------------------------------------------------------------------#

from multiprocessing.dummy import Manager
from django.db import models
from django.db.models import Q

#----------------------------------------------------------------------------------------------------------------#
# Managers
#----------------------------------------------------------------------------------------------------------------#

class UsuarioManager(models.Manager):
    # Permite crear un nuevo Usuario.
    def crear_usuario(
                    self, 
                    nombreUsuario, 
                    contraUsuario, 
                    nombresUsuario, 
                    apellidosUsuario, 
                    rutUsuario, 
                    correoUsuario, 
                    celularUsuario, 
                    idCalle, 
                    idJerarquia, 
                    idRol, 
                    idUnidad, 
                    **extra_fields
                ):
        usuario = self.create(
            usuario                 = nombreUsuario,
            contraseña              = contraUsuario,
            nombres                 = nombresUsuario,
            apellidos               = apellidosUsuario,
            rut                     = rutUsuario,
            correo                  = correoUsuario,
            celular                 = celularUsuario,
            calle_id_calle          = idCalle,
            jerarquia_id_jerarquia  = idJerarquia,
            rol_id_rol              = idRol,
            unidad_id_unidad        = idUnidad,
            **extra_fields
        )
        return usuario
    # Usuario
    def traer_datos_usuario(self, username, password):
        return self.filter(
            usuario     = username,
            contraseña  = password
        ).values_list()

    def usuario_exists(self, username, password):
        return self.filter(
            usuario     = username,
            contraseña  = password
        ).exists()


class TareaManager(models.Manager):
    # Permite crear una nueva tarea.
    def crear_tarea(self, nombreTarea, descTarea, fechaInicio, fechaPlazo, idUsuario, idFlujo, **extra_fields):
        tarea = self.create(
            tarea               = nombreTarea,
            descripcion         = descTarea,
            fecha_inicio        = fechaInicio,
            fecha_plazo         = fechaPlazo,
            usuario_id_usuario  = idUsuario,
            flujo_id_flujo      = idFlujo,
            **extra_fields
        )
        return tarea
    # Trae las tareas que corresponden al usuario solicitado.
    def tareas_usuarios(self, id_usuario):
        return self.filter(usuario_id_usuario_id = id_usuario)
    # Trae la tarea solicitada.
    def tareas_id(self, id_tarea):
        return self.filter(id_tarea = id_tarea)


class FlujoManager(models.Manager):
    # Permite crear un nuevo flujo.
    def crear_flujo(self, nombreFlujo, descFlujo, idEstado, **extra_fields):
        flujo = self.create(
            nombre_flujo        = nombreFlujo,
            descripcion         = descFlujo,
            estado_id_estado    = idEstado,
            **extra_fields
        )
        return flujo


class RolManager(models.Manager):
    
    def is_rol_nombre(self, rol_id):
        return self.all().filter(
            Q(rol="Funcionario") | Q(rol="Diseñador de Procesos") | Q(rol="Administrador")
        ).filter(
            id_rol = rol_id
        ).exists()

    def crear_rol(self, nombreRol, **extra_fields):
        rol = self.create(
            rol = nombreRol,
            **extra_fields,
        )
        return rol

    def traer_datos_rol(self):
        return self.all()

class JerarquiaManager(models.Manager):

    def crear_jerarquia(self, nombreJerarquia, **extra_fields):
        jerarquia = self.create(
            jerarquia = nombreJerarquia,
            **extra_fields,
        )
        return jerarquia

    def traer_datos_jerarquia(self):
        return self.all()

class UnidadManager(models.Manager):

    def crear_unidad(self, nombreUnidad, **extra_fields):
        unidad = self.create(
            unidad = nombreUnidad,
            **extra_fields,
        )
        return unidad

    def traer_datos_unidad(self):
        return self.all()