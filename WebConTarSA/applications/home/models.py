#----------------------------------------------------------------------------------------------------------------#
# Importaciones necesarias
#----------------------------------------------------------------------------------------------------------------#

from django.db import models
from .managers import *

#----------------------------------------------------------------------------------------------------------------#
# Modelos
#----------------------------------------------------------------------------------------------------------------#


class Calle(models.Model):
    id_calle            = models.BigAutoField(primary_key=True)
    calle               = models.CharField(max_length=50)
    comuna_id_comuna    = models.ForeignKey('Comuna', models.DO_NOTHING, db_column='comuna_id_comuna')

    class Meta:
        managed = False
        db_table = 'calle'

class Ciudad(models.Model):
    id_ciudad           = models.BigAutoField(primary_key=True)
    ciudad              = models.CharField(max_length=50)
    region_id_region    = models.ForeignKey('Region', models.DO_NOTHING, db_column='region_id_region')

    class Meta:
        managed = False
        db_table = 'ciudad'

class Comuna(models.Model):
    id_comuna           = models.BigAutoField(primary_key=True)
    comuna              = models.CharField(max_length=50)
    ciudad_id_ciudad    = models.ForeignKey(Ciudad, models.DO_NOTHING, db_column='ciudad_id_ciudad')

    class Meta:
        managed = False
        db_table = 'comuna'

class Estado(models.Model):
    id_estado   = models.BigAutoField(primary_key=True)
    estado      = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'estado'

class Flujo(models.Model):
    id_flujo            = models.BigAutoField(primary_key=True)
    nombre_flujo        = models.CharField(max_length=50)
    descripcion         = models.CharField(max_length=1024)
    estado_id_estado    = models.ForeignKey(Estado, models.DO_NOTHING, db_column='estado_id_estado')

    objects = FlujoManager()

    def init(self,  id_flujo):
       self.id_flujo= id_flujo

    class Meta:
        managed = False
        db_table = 'flujo'

class Jerarquia(models.Model):
    id_jerarquia    = models.BigAutoField(primary_key=True)
    jerarquia       = models.CharField(max_length=50)

    objects = JerarquiaManager()

    def init(self,  id_jerarquia):
       self.id_jerarquia= id_jerarquia

    class Meta:
        managed = False
        db_table = 'jerarquia'

class Region(models.Model):
    id_region = models.BigAutoField(primary_key=True)
    region = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'region'

class Rol(models.Model):
    id_rol = models.BigAutoField(primary_key=True)
    rol = models.CharField(max_length=50)

    objects = RolManager()

    def init(self,  id_rol):
       self.id_rol= id_rol

    class Meta:
        managed = False
        db_table = 'rol'

class Tarea(models.Model):
    id_tarea                = models.BigAutoField(primary_key=True)
    tarea                   = models.CharField(max_length=50)
    descripcion             = models.CharField(max_length=1024)
    fecha_inicio            = models.DateField()
    fecha_plazo             = models.DateField()
    porcentaje_cumplido     = models.BigIntegerField()
    reporte                 = models.CharField(max_length=1024, blank=True, null=True)
    aprobacion              = models.CharField(max_length=1, blank=True, null=True)
    justificacion           = models.CharField(max_length=1024, blank=True, null=True)
    estado_id_estado        = models.ForeignKey(Estado, models.DO_NOTHING, db_column='estado_id_estado')
    usuario_id_usuario      = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuario_id_usuario')
    flujo_id_flujo          = models.ForeignKey(Flujo, models.DO_NOTHING, db_column='flujo_id_flujo', blank=True, null=True)

    objects = TareaManager()

    class Meta:
        managed = False
        db_table = 'tarea'

class Unidad(models.Model):
    id_unidad   = models.BigAutoField(primary_key=True)
    unidad      = models.CharField(max_length=50)

    objects     = UnidadManager()

    def init(self,  id_unidad):
       self.id_unidad= id_unidad

    class Meta:
        managed = False
        db_table = 'unidad'


class Usuario(models.Model):
    id_usuario              = models.BigAutoField(primary_key=True)
    usuario                 = models.CharField(max_length=50)
    contraseña              = models.CharField(max_length=50)
    nombres                 = models.CharField(max_length=50)
    apellidos               = models.CharField(max_length=50)
    rut                     = models.CharField(max_length=10)
    correo                  = models.CharField(max_length=50)
    celular                 = models.CharField(max_length=12)
    calle_id_calle          = models.ForeignKey(Calle, models.DO_NOTHING, db_column='calle_id_calle')
    jerarquia_id_jerarquia  = models.ForeignKey(Jerarquia, models.DO_NOTHING, db_column='jerarquia_id_jerarquia')
    rol_id_rol              = models.ForeignKey(Rol, models.DO_NOTHING, db_column='rol_id_rol')
    unidad_id_unidad        = models.ForeignKey(Unidad, models.DO_NOTHING, db_column='unidad_id_unidad')
    is_active           = models.BooleanField()
    is_authenticated    = True

    objects = UsuarioManager()

    def init(self,  id_usuario):
       self.id_usuario= id_usuario

    class Meta:
        managed = False
        db_table = 'usuario'

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

