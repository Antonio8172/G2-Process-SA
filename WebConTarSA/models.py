# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Calle(models.Model):
    id_calle = models.BigAutoField(primary_key=True)
    calle = models.CharField(max_length=50)
    comuna_id_comuna = models.ForeignKey('Comuna', models.DO_NOTHING, db_column='comuna_id_comuna')

    class Meta:
        managed = False
        db_table = 'calle'


class Ciudad(models.Model):
    id_ciudad = models.BigAutoField(primary_key=True)
    ciudad = models.CharField(max_length=50)
    region_id_region = models.ForeignKey('Region', models.DO_NOTHING, db_column='region_id_region')

    class Meta:
        managed = False
        db_table = 'ciudad'


class Comuna(models.Model):
    id_comuna = models.BigAutoField(primary_key=True)
    comuna = models.CharField(max_length=50)
    ciudad_id_ciudad = models.ForeignKey(Ciudad, models.DO_NOTHING, db_column='ciudad_id_ciudad')

    class Meta:
        managed = False
        db_table = 'comuna'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200, blank=True, null=True)
    action_flag = models.IntegerField()
    change_message = models.TextField(blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField(blank=True, null=True)
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Estado(models.Model):
    id_estado = models.BigAutoField(primary_key=True)
    estado = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'estado'


class Flujo(models.Model):
    id_flujo = models.BigAutoField(primary_key=True)
    nombre_flujo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=1024)
    estado_id_estado = models.ForeignKey(Estado, models.DO_NOTHING, db_column='estado_id_estado')

    class Meta:
        managed = False
        db_table = 'flujo'


class Jerarquia(models.Model):
    id_jerarquia = models.BigAutoField(primary_key=True)
    jerarquia = models.CharField(max_length=50)

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

    class Meta:
        managed = False
        db_table = 'rol'


class Tarea(models.Model):
    id_tarea = models.BigAutoField(primary_key=True)
    tarea = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=1024)
    fecha_inicio = models.DateField()
    fecha_plazo = models.DateField()
    porcentaje_cumplido = models.BigIntegerField()
    reporte = models.CharField(max_length=1024, blank=True, null=True)
    aprobacion = models.CharField(max_length=1, blank=True, null=True)
    justificacion = models.CharField(max_length=1024, blank=True, null=True)
    estado_id_estado = models.ForeignKey(Estado, models.DO_NOTHING, db_column='estado_id_estado')
    usuario_id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuario_id_usuario')
    flujo_id_flujo = models.ForeignKey(Flujo, models.DO_NOTHING, db_column='flujo_id_flujo', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tarea'


class Unidad(models.Model):
    id_unidad = models.BigAutoField(primary_key=True)
    unidad = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'unidad'


class Usuario(models.Model):
    id_usuario = models.BigAutoField(primary_key=True)
    usuario = models.CharField(max_length=50)
    contraseña = models.CharField(max_length=50)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    rut = models.CharField(max_length=10)
    correo = models.CharField(max_length=50)
    celular = models.CharField(max_length=12)
    calle_id_calle = models.ForeignKey(Calle, models.DO_NOTHING, db_column='calle_id_calle')
    jerarquia_id_jerarquia = models.ForeignKey(Jerarquia, models.DO_NOTHING, db_column='jerarquia_id_jerarquia')
    rol_id_rol = models.ForeignKey(Rol, models.DO_NOTHING, db_column='rol_id_rol')
    unidad_id_unidad = models.ForeignKey(Unidad, models.DO_NOTHING, db_column='unidad_id_unidad')

    class Meta:
        managed = False
        db_table = 'usuario'
