#----------------------------------------------------------------------------------------------------------------#
# Importaciones necesarias
#----------------------------------------------------------------------------------------------------------------#

from django.urls import path
from . import views

#----------------------------------------------------------------------------------------------------------------#
# Nombre de la aplicación
#----------------------------------------------------------------------------------------------------------------#

app_name = 'AppWebHome'

#----------------------------------------------------------------------------------------------------------------#
# URLs
#----------------------------------------------------------------------------------------------------------------#

urlpatterns = [
    
    # Principales
    path('',                            views.HomeListView.as_view(),           name = 'home'),
    path('login/',                      views.LoginView.as_view(),              name = 'login'),
    path('logout/',                     views.LogoutView.as_view(),             name = 'logout'),
    
    # Usuarios
    path('administrador/',              views.AdministradorView.as_view(),      name = 'administrador'),
    path('funcionario/',                views.FuncionarioView.as_view(),        name = 'funcionario'),
    path('diseñador/',                  views.DiseñadorView.as_view(),          name = 'diseñador'),
    path('perfil/',                     views.PerfilListView.as_view(),         name = 'perfil'),
    
    # CRUDs
        #tarea
    path('ver-tareas/',                     views.VerTareaView.as_view(),                       name = 'verTareas'),
    path('crud_tarea/',                     views.CRUDTareaView.as_view(),                      name = 'crudTarea'),
    path('crear-tarea/',                    views.TareaCreateView.as_view(),                    name = 'crearTarea'),
    path('detalle-tarea/<int:pk>/',         views.TareaDetailView.as_view(),                    name = 'detalleTarea'),
    path('borrar/<int:pk>/',  views.TareaDetailView.eliminar_tarea,               name = 'borrarTarea'),
        #flujo
    path('ver-flujos/',                     views.FlujoListView.as_view(),                      name = 'verFlujos'),
    path('crud_flujo/',                     views.CRUDFlujoView.as_view(),                      name = 'crudFlujo'),
    path('crear-flujo/',                    views.FlujoCreateView.as_view(),                    name = 'crearFlujo'),
    path('detalle-flujo/<int:pk>/',         views.FlujoDetailView.as_view(),                    name = 'detalleFlujo'),
        #jerarquía
    path('crud_jerarquia/',                     views.CRUDJerarquiaView.as_view(),              name = 'crudJerarquia'),
    path('crear-jerarquia/',                    views.JerarquiaCreateView.as_view(),            name = 'crearJerarquia'),
    path('crear-jerarquia/borrar/<int:id>',     views.JerarquiaCreateView.eliminar_jerarquia,   name = 'borrarJerarquia'),
        #rol
    path('crud_rol/',                           views.CRUDRolView.as_view(),                    name = 'crudRol'),
    path('crear-rol/',                          views.RolCreateView.as_view(),                  name = 'crearRol'),
    path('crear-rol/borrar/<int:id>',           views.RolCreateView.eliminar_rol,               name = 'borrarRol'),
        #unidad
    path('crud_unidad/',                    views.CRUDUnidadView.as_view(),                     name = 'crudUnidad'),
    path('crear-unidad/',                   views.UnidadCreateView.as_view(),                   name = 'crearUnidad'),
    path('crear-unidad/borrar/<int:id>',    views.UnidadCreateView.eliminar_unidad,             name = 'borrarUnidad'),
        #usuario
    path('ver-usuarios/',                   views.UsuarioListView.as_view(),        name = 'verUsuarios'),
    path('crud_usuario/',                   views.CRUDUsuarioView.as_view(),        name = 'crudUsuario'),
    path('crear-usuario/',                  views.UsuarioCreateView.as_view(),      name = 'crearUsuario'),
    path('detalle-usuario/<int:pk>',        views.UsuarioDetailView.as_view(),      name = 'detalleUsuario'),
    path('borrrar/<int:pk>/',  views.UsuarioDetailView.eliminar_usuario,               name = 'borrarUsuario'),

    # Prueba/Test
    path('prueba/',                     views.PruebaView.as_view(),             name = 'prueba'),

]