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
    path('panel-control/',              views.PanelControlView.as_view(),       name = 'panelControl'),


    # Usuarios
    path('administrador/',              views.AdministradorView.as_view(),      name = 'administrador'),
    path('funcionario/',                views.FuncionarioView.as_view(),        name = 'funcionario'),
    path('diseñador/',                  views.DiseñadorView.as_view(),          name = 'diseñador'),

    # Perfil de Usuario
    path('perfil/',                     views.PerfilListView.as_view(),         name = 'perfil'),
    path('editar-perfil/',              views.PerfilListView.editar_perfil,     name = 'editarPerfil'),

    # CRUDs

        #usuario
    path('ver-usuarios/',                   views.UsuarioListView.as_view(),            name = 'verUsuarios'),
    path('crud_usuario/',                   views.CRUDUsuarioView.as_view(),            name = 'crudUsuario'),
    path('crear-usuario/',                  views.UsuarioCreateView.as_view(),          name = 'crearUsuario'),
    path('detalle-usuario/<int:pk>/',       views.UsuarioDetailView.as_view(),          name = 'detalleUsuario'),
    path('borrar-usuario/<int:pk>/',        views.UsuarioDetailView.eliminar_usuario,   name = 'borrarUsuario'),
    path('editar-usuario/',                 views.UsuarioDetailView.editar_usuario,     name = 'editarUsuario'),

        #tarea
    path('ver-tareas/',                     views.VerTareaView.as_view(),                       name = 'verTareas'),
    path('crud_tarea/',                     views.CRUDTareaView.as_view(),                      name = 'crudTarea'),
    path('crear-tarea/',                    views.TareaCreateView.as_view(),                    name = 'crearTarea'),
    path('detalle-tarea/<int:pk>/',         views.TareaDetailView.as_view(),                    name = 'detalleTarea'),
    path('borrar-tarea/<int:pk>/',          views.TareaDetailView.eliminar_tarea,               name = 'borrarTarea'),
    path('editar-tarea/',                   views.TareaDetailView.editar_tarea,                 name = 'editarTarea'),

        #flujo
    path('ver-flujos/',                     views.FlujoListView.as_view(),                      name = 'verFlujos'),
    path('crud_flujo/',                     views.CRUDFlujoView.as_view(),                      name = 'crudFlujo'),
    path('crear-flujo/',                    views.FlujoCreateView.as_view(),                    name = 'crearFlujo'),
    path('detalle-flujo/<int:pk>/',         views.FlujoDetailView.as_view(),                    name = 'detalleFlujo'),
    path('borrar-flujo/<int:pk>/',          views.FlujoDetailView.eliminar_flujo,               name = 'borrarFlujo'),
    path('editar-flujo/',                   views.FlujoDetailView.editar_flujo,                 name = 'editarFlujo'),

        #jerarquía
    path('crud_jerarquia/',                     views.CRUDJerarquiaView.as_view(),              name = 'crudJerarquia'),
    path('crear-jerarquia/',                    views.JerarquiaCreateView.as_view(),            name = 'crearJerarquia'),
    path('crear-jerarquia/borrar/<int:id>',     views.JerarquiaCreateView.eliminar_jerarquia,   name = 'borrarJerarquia'),
    # path('editar-jerarquia/',                   views.JerarquiaCreateView.editar_jerarquia,    name = 'editarJerarquia'),

        #rol
    path('crud_rol/',                           views.CRUDRolView.as_view(),                    name = 'crudRol'),
    path('crear-rol/',                          views.RolCreateView.as_view(),                  name = 'crearRol'),
    path('crear-rol/borrar/<int:id>',           views.RolCreateView.eliminar_rol,               name = 'borrarRol'),
    # path('editar-rol/',                         views.RolCreateView.editar_rol,                name = 'editarRol'),

        #unidad
    path('crud_unidad/',                    views.CRUDUnidadView.as_view(),                     name = 'crudUnidad'),
    path('crear-unidad/',                   views.UnidadCreateView.as_view(),                   name = 'crearUnidad'),
    path('crear-unidad/borrar/<int:id>',    views.UnidadCreateView.eliminar_unidad,             name = 'borrarUnidad'),
    # path('editar-unidad/',                   views.UnidadCreateView.editar_unidad,             name = 'editarUnidad'),

]