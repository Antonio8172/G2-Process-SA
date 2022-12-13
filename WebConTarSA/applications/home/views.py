#----------------------------------------------------------------------------------------------------------------#
# Importaciones necesarias
#----------------------------------------------------------------------------------------------------------------#

from django.urls                import reverse_lazy
from django.views.generic       import TemplateView, ListView, FormView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models    import *
from .forms     import *
from .functions import *

#----------------------------------------------------------------------------------------------------------------#
# Principales
#----------------------------------------------------------------------------------------------------------------#

# Vista de la página principal o home.
class HomeListView(TemplateView):
    template_name = "principal/home.html"

# Vista del login.
class LoginView(FormView):
    template_name = "principal/login.html"
    form_class    = LoginForm
    success_url   = reverse_lazy("AppWebHome:home")
    # Validación del formulario para ingresar al sistema como un usuario.
    def form_valid(self, form):
        nomUsuario = form.cleaned_data['usuario']
        contraseña = form.cleaned_data['contraseña']
        usuario    = Usuario.objects.usuario_exists(nomUsuario, contraseña)
        return Login.login_autenticacion(self, usuario, nomUsuario, contraseña)

# Vista del perfil de Usuario.
class PerfilListView(LoginRequiredMixin, ListView):
    model               = Usuario
    template_name       = "usuario/perfil.html"
    context_object_name = "usuario"
    # Obtención de otros datos.
    def get_context_data(self, *args, **kwargs):
        context             = super().get_context_data(**kwargs)
        context["calles"]   = Calle.objects.all().order_by('calle')
        context["comunas"]  = Comuna.objects.all()
        context["ciudades"] = Ciudad.objects.all()
        context["regiones"] = Region.objects.all()
        return context
    # Permite editar el perfil de usuario.
    def editar_perfil(request):
        return ModificacionesModelos.editar_perfil(request)


class LogoutView(View):
    def get(self, request):
        return Login.cerrar_sesion(self, request)


class PanelControlView(LoginRequiredMixin, ListView):
    model               = Tarea
    template_name       = 'principal/panelControl.html'
    context_object_name = "tareas"
    # Obtención de otros datos
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cantTareas']         = CantidadTareas.color_RGY()
        context['cantUnidades']       = CantidadTareas.unidad_color_RGY()
        context['ultimoCantUnidad']   = len(CantidadTareas.unidad_color_RGY())
        context['cantidadJerarquias'] = CantidadTareas.jerarquia()
        context['ultimoCantJerar']    = len(CantidadTareas.jerarquia())
        return context

class PDFview(TemplateView):
    model               = Tarea
    template_name       = 'PDF/graficos1.html'
    context_object_name = "tareas"
    # Obtención de otros datos
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cantTareas']         = CantidadTareas.color_RGY()
        context['cantUnidades']       = CantidadTareas.unidad_color_RGY()
        context['ultimoCantUnidad']   = len(CantidadTareas.unidad_color_RGY())
        context['cantidadJerarquias'] = CantidadTareas.jerarquia()
        context['ultimoCantJerar']    = len(CantidadTareas.jerarquia())
        return context

class GraficosPDFView(View):
    def get(self, request, *args, **kwargs):
        responsable = request.user.nombres + ' ' + request.user.apellidos
        datos = {
            'responsable'        : responsable,
            'fechaActual'        : OperacionesFechas.fecha_actual(),
            'cantTareas'         : CantidadTareas.color_RGY(),
            'cantUnidades'       : CantidadTareas.unidad_color_RGY(),
            'cantidadJerarquias' : CantidadTareas.jerarquia(),
        }
        pdf = Html2Pdf.render_2_pdf('PDF/graficos1.html', datos)
        return HttpResponse(pdf, content_type='application/pdf')


#----------------------------------------------------------------------------------------------------------------#
# Usuarios
#----------------------------------------------------------------------------------------------------------------#

# Vista del home del administrador.
class AdministradorView(LoginRequiredMixin, TemplateView):
    template_name = "usuario/administrador.html"
    # Sólo permite ingresar a esta página los usuarios con el rol de administrador.
    def get(self, request, *args, **kwargs):
        permiso = request.user.rol_id_rol.rol
        rol     = 'Administrador'
        if permiso == rol:
            return super(AdministradorView, self).get(request, *args, **kwargs)
        else:
            return Login.verificar_permisos_rol(permiso, request)

# Vista del home del funcionario.
class FuncionarioView(LoginRequiredMixin, TemplateView):
    template_name       = "usuario/funcionario.html"
    # Sólo permite ingresar a esta página los usuarios con el rol de funcionario.
    def get(self, request, *args, **kwargs):
        permiso = request.user.rol_id_rol.rol
        rol     = 'Funcionario'
        if permiso == rol:
            return super(FuncionarioView, self).get(request, *args, **kwargs)
        else:
            return Login.verificar_permisos_rol(permiso, request)

# Vista del home del diseñador.
class DiseñadorView(LoginRequiredMixin, TemplateView):
    template_name = "usuario/diseñador.html"
    # Sólo permite ingresar a esta página los usuarios con el rol de Diseñador.
    def get(self, request, *args, **kwargs):
        permiso = request.user.rol_id_rol.rol
        rol     = 'Diseñador de Procesos'
        if permiso == rol:
            return super(DiseñadorView, self).get(request, *args, **kwargs)
        else:
            return Login.verificar_permisos_rol(permiso, request)



#----------------------------------------------------------------------------------------------------------------#
# CRUDs
#----------------------------------------------------------------------------------------------------------------#

#-----------------------------#
# crud usuarios               #
#-----------------------------#

# Vista general del Crud de usuarios.
class CRUDUsuarioView(LoginRequiredMixin, TemplateView):
    template_name   = "cruds/crud-usuario/crud_usuario.html"

# Vista para crear un flujo.
class UsuarioCreateView(LoginRequiredMixin, FormView):
    model           = Usuario
    form_class      = UsuarioForm
    template_name   = "cruds/crud-usuario/crear-usuario.html"
    success_url     = reverse_lazy("AppWebHome:crearUsuario")

    # Validación del formulario y posterior creación del usuario.
    def form_valid(self, form):
        idCalle     = Calle(self.request.POST.get('calle_id_calle'))
        idJerarquia = Jerarquia(self.request.POST.get('jerarquia_id_jerarquia'))
        idRol       = Rol(self.request.POST.get('rol_id_rol'))
        idUnidad    = Unidad(self.request.POST.get('unidad_id_unidad'))
        datos       = form.cleaned_data
        ModificacionesModelos.crear_usuario(datos, idCalle, idJerarquia, idRol, idUnidad)
        return super(UsuarioCreateView, self).form_valid(form)

    # Formulario inválido.
    def form_invalid(self, form):
        self.request.session['acusete'] = 'form inválido'
        return super(UsuarioCreateView, self).form_invalid(form)

    # Obtención de otros datos.
    def get_context_data(self, *args, **kwargs):
        context                 = super().get_context_data(**kwargs)
        context["calles"]       = Calle.objects.all()
        context["jerarquias"]   = Jerarquia.objects.all()
        context["roles"]        = Rol.objects.all()
        context["unidades"]     = Unidad.objects.all()
        return context

# Vista para ver todos los flujos.
class UsuarioListView(LoginRequiredMixin, ListView):
    model               = Usuario
    template_name       = "cruds/crud-usuario/ver-usuarios.html"
    context_object_name = "usuarios"
    # Obtención de otros datos.
    def get_context_data(self, **kwargs):
        context                 = super().get_context_data(**kwargs)
        context["fechaActual"]  = OperacionesFechas.fecha_actual()
        return context

# Vista para ver el detalle del flujo.
class UsuarioDetailView(LoginRequiredMixin, DetailView):
    model               = Usuario
    template_name       = "cruds/crud-usuario/detalle-usuario.html"
    context_object_name = "usuario"

    # Obtención de otros datos.
    def get_context_data(self, **kwargs):
        context               = super().get_context_data(**kwargs)
        context["calles"]     = Calle.objects.all()
        context["jerarquias"] = Jerarquia.objects.all()
        context["roles"]      = Rol.objects.all()
        context["unidades"]   = Unidad.objects.all()
        return context

    # Permite editar el usuario.
    def editar_usuario(request):
        return ModificacionesModelos.editar_usuario(request)

    # Permite eliminar el usuario.
    def eliminar_usuario(request, pk):
        return ModificacionesModelos.borrar_usuario(request, pk)


#-----------------------------#
# crud tareas                 #
#-----------------------------#

# Vista general del Crud de tareas.
class CRUDTareaView(LoginRequiredMixin, TemplateView):
    template_name = "cruds/crud-tarea/crud_tarea.html"

# Vista para crear una tarea.
class TareaCreateView(LoginRequiredMixin, FormView):
    model         = Tarea
    form_class    = TareaForm
    template_name = "cruds/crud-tarea/crear-tarea.html"
    success_url   = reverse_lazy("AppWebHome:crearTarea")

    # Validación del formulario y posterior creación de tarea.
    def form_valid(self, form):
        id_user     = self.request.POST.get('id_usuario')
        idFlujo     = Flujo(self.request.POST.get('flujo_id_flujo'))
        datos       = form.cleaned_data
        if idFlujo != None:
            ModificacionesModelos.crear_tarea(datos, id_user, idFlujo)
            Correo.notificar_nueva_tarea(id_user)
            return super(TareaCreateView, self).form_valid(form)

    # Formulario inválido.
    def form_invalid(self, form):
        self.request.session['acusete'] = 'form inválido'
        return super(TareaCreateView, self).form_invalid(form)

    # Obtención de otros datos.
    def get_context_data(self, *args, **kwargs):
        context             = super().get_context_data(**kwargs)
        context["usuarios"] = Usuario.objects.all()
        context["flujos"]   = Flujo.objects.all()
        context["tareas"]   = Tarea.objects.all()
        return context

# Vista para ver todas las tareas.
class VerTareaView(LoginRequiredMixin, ListView):
    model               = Tarea
    paginate_by         = 9
    template_name       = "cruds/crud-tarea/ver-tarea.html"
    context_object_name = "tareas"

    # Llenado de la información que almacena la variable 'context_object_name'.
    def get_queryset(self):
        return FuncionesTareas.lista_tareas_rol(self)

    # Obtención de otros datos.
    def get_context_data(self, **kwargs):
        context                     = super().get_context_data(**kwargs)
        dictDdPa                    = FuncionesTareas.dict_dd_pa(self)
        context["diferenciaDias"]   = dictDdPa['dd'] 
        context["porcentajeActual"] = dictDdPa['pa']
        context["fechaActual"]      = OperacionesFechas.fecha_actual()
        return context

# Vista para ver el detalle de la tarea.
class TareaDetailView(LoginRequiredMixin, DetailView):
    model               = Tarea
    template_name       = "cruds/crud-tarea/detalle-tarea.html"
    context_object_name = "tarea"

    # Obtención de otros datos.
    def get_context_data(self, *args, **kwargs):
        context             = super().get_context_data(**kwargs)
        tareaActual         = Tarea.objects.tareas_id(self.kwargs.get('pk'))
        for t in tareaActual:
            fechaPlazo         = t.fecha_plazo
            context["dd"]      = OperacionesFechas.diferencia_dias(fechaPlazo)
        context["fechaActual"] = OperacionesFechas.fecha_actual()
        context["usuarios"]    = Usuario.objects.all()
        context["flujos"]      = Flujo.objects.all()
        return context

    # Permite editar la tarea.
    def editar_tarea(request):
        return ModificacionesModelos.editar_tarea(request)

    # Permite eliminar la tarea.
    def eliminar_tarea(request, pk):
        return ModificacionesModelos.borrar_tarea(request, pk)

    def reportar_problema(request):
        return ModificacionesModelos.reportar_problema(request)


#-----------------------------#
# crud flujos                 #
#-----------------------------#

# Vista general del Crud de flujos.
class CRUDFlujoView(LoginRequiredMixin, TemplateView):
    template_name   = "cruds/crud-flujo/crud_flujo.html"

# Vista para crear un flujo.
class FlujoCreateView(LoginRequiredMixin, FormView):
    model           = Flujo
    form_class      = FlujoForm
    template_name   = "cruds/crud-flujo/crear-flujo.html"
    success_url     = reverse_lazy("AppWebHome:crearFlujo")

    # Validación del formulario y posterior creación de flujo.
    def form_valid(self, form):
        idEstado     = Estado(self.request.POST.get('estado_id_estado'))
        datos        = form.cleaned_data
        if idEstado != None:
            ModificacionesModelos.crear_flujo(datos, idEstado)
            return super(FlujoCreateView, self).form_valid(form)

    # Formulario inválido.
    def form_invalid(self, form):
        self.request.session['acusete'] = 'form inválido'
        return super(FlujoCreateView, self).form_invalid(form)

    # Obtención de otros datos.
    def get_context_data(self, *args, **kwargs):
        context             = super().get_context_data(**kwargs)
        context["estados"]  = Estado.objects.all()
        return context

# Vista para ver todos los flujos.
class FlujoListView(LoginRequiredMixin, ListView):
    model               = Flujo
    template_name       = "cruds/crud-flujo/ver-flujos.html"
    context_object_name = "flujos"
    # Obtención de otros datos.
    def get_context_data(self, **kwargs):
        context                = super().get_context_data(**kwargs)
        context["fechaActual"] = OperacionesFechas.fecha_actual()
        return context

# Vista para ver el detalle del flujo.
class FlujoDetailView(LoginRequiredMixin, DetailView):
    model               = Flujo
    template_name       = "cruds/crud-flujo/detalle-flujo.html"
    context_object_name = "flujo"

    # Obtención de otros datos.
    def get_context_data(self, *args, **kwargs):
        context                 = super().get_context_data(**kwargs)
        context["estados"]      = Estado.objects.all()
        context["tareas"]       = Tarea.objects.all()
        context["fechaActual"]  = OperacionesFechas.fecha_actual()
        return context

    # Permite editar el flujo.
    def editar_flujo(request):
        return ModificacionesModelos.editar_flujo(request)

    # Permite eliminar el flujo.
    def eliminar_flujo(request, pk):
        return ModificacionesModelos.borrar_flujo(request, pk)

    # Permite ejecutar el flujo
    def ejecutar_flujo(request, pk):
        return ModificacionesModelos.ejecutar_flujo(request, pk)


#-----------------------------#
# crud jerarquías             #
#-----------------------------#

# Vista general del Crud de jerarquías.
class CRUDJerarquiaView(LoginRequiredMixin, ListView):
    model               = Jerarquia
    template_name       = "cruds/crud-jerarquia/crud_jerarquia.html"
    context_object_name = "jerarquias"

# Vista para crear, editar y borrar una jerarquía.
class JerarquiaCreateView(LoginRequiredMixin, FormView):
    model           = Jerarquia
    form_class      = JerarquiaForm
    template_name   = "cruds/crud-jerarquia/crear-jerarquia.html"
    success_url     = reverse_lazy("AppWebHome:crearJerarquia")

    # Validación del formulario y posterior creación de una jerarquía.
    def form_valid(self, form):
        datos = form.cleaned_data
        ModificacionesModelos.crear_jerarquia(datos)
        return super(JerarquiaCreateView, self).form_valid(form)

    # Formulario inválido.
    def form_invalid(self, form):
        self.request.session['acusete'] = 'form inválido'
        return super(JerarquiaCreateView, self).form_invalid(form)

    # Obtención de otros datos.
    def get_context_data(self, *args, **kwargs):
        context                 = super().get_context_data(**kwargs)
        context["fechaActual"]  = OperacionesFechas.fecha_actual()
        context["jerarquias"]   = Jerarquia.objects.traer_datos_jerarquia()
        return context

    # Eliminación de una jerarquía.
    def eliminar_jerarquia(request, id):
        return ModificacionesModelos.borrar_jerarquia(request, id)


#-----------------------------#
# crud roles                  #
#-----------------------------#

# Vista general del Crud de roles.
class CRUDRolView(LoginRequiredMixin, ListView):
    model               = Rol
    template_name       = "cruds/crud-rol/crud_rol.html"
    context_object_name = "roles"

# Vista para crear, editar y borrar un rol.
class RolCreateView(LoginRequiredMixin, FormView):
    model           = Rol
    form_class      = RolForm
    template_name   = "cruds/crud-rol/crear-rol.html"
    success_url     = reverse_lazy("AppWebHome:crearRol")

    # Validación del formulario y posterior creación del rol.
    def form_valid(self, form):
        datos = form.cleaned_data
        ModificacionesModelos.crear_rol((datos))
        return super(RolCreateView, self).form_valid(form)

    # Formulario inválido.
    def form_invalid(self, form):
        self.request.session['acusete'] = 'form inválido'
        return super(RolCreateView, self).form_invalid(form)

    # Obtención de otros datos.
    def get_context_data(self, *args, **kwargs):
        context                 = super().get_context_data(**kwargs)
        context["fechaActual"]  = OperacionesFechas.fecha_actual()
        context["roles"]        = Rol.objects.all()
        return context

    # Eliminación de un rol.
    def eliminar_rol(request, id):
        return ModificacionesModelos.borrar_rol(request, id)


#-----------------------------#
# crud unidades               #
#-----------------------------#

# Vista general del Crud de unidades.
class CRUDUnidadView(LoginRequiredMixin, ListView):
    model               = Unidad
    template_name       = "cruds/crud-unidad/crud_unidad.html"
    context_object_name = "unidades"

# Vista para crear, editar y borrar una unidad.
class UnidadCreateView(LoginRequiredMixin, FormView):
    model           = Unidad
    form_class      = UnidadForm
    template_name   = "cruds/crud-unidad/crear-unidad.html"
    success_url     = reverse_lazy("AppWebHome:crearUnidad")

    # Validación del formulario y posterior creación de la unidad.
    def form_valid(self, form):
        datos = form.cleaned_data
        ModificacionesModelos.crear_unidad(datos)
        return super(UnidadCreateView, self).form_valid(form)

    # Formulario inválido.
    def form_invalid(self, form):
        self.request.session['acusete'] = 'form inválido'
        return super(UnidadCreateView, self).form_invalid(form)

    # Obtención de otros datos.
    def get_context_data(self, *args, **kwargs):
        context                 = super().get_context_data(**kwargs)
        context["fechaActual"]  = OperacionesFechas.fecha_actual()
        context["unidades"]     = Unidad.objects.traer_datos_unidad()
        return context

    # Eliminación de una unidad.
    def eliminar_unidad(request, id):
        return ModificacionesModelos.borrar_unidad(request, id)