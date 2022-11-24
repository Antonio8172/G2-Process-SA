#----------------------------------------------------------------------------------------------------------------#
# Importaciones necesarias
#----------------------------------------------------------------------------------------------------------------#

from http.client import HTTPResponse
from re import template
from webbrowser import get
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView, FormView, DetailView, View
from .models import *
from .forms import *
from .functions import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import loader

#----------------------------------------------------------------------------------------------------------------#
# Principales
#----------------------------------------------------------------------------------------------------------------#

# Página principal
class HomeListView(ListView):
    model = Usuario
    template_name = "principal/home.html"

# Login
class LoginView(FormView):
    template_name = "principal/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("AppWebHome:home")

    def form_valid(self, form):
        nomUsuario = form.cleaned_data['usuario']
        contraseña = form.cleaned_data['contraseña']

        usuario = Usuario.objects.usuario_exists(nomUsuario, contraseña)

        if(usuario):
            rol_id = Usuario.objects.traer_datos_usuario(nomUsuario, contraseña)[0][10]
            is_rol = Rol.objects.is_rol_nombre(rol_id)

        if(usuario and is_rol):
            autUsuario = authenticate(username=nomUsuario, password=contraseña)

            if(autUsuario is not None):
                login(self.request, autUsuario)
                rol = self.request.user.rol_id_rol.id_rol
                # return super(LoginView, self).form_valid(form)
                if( rol == 4 ):
                    return HttpResponseRedirect(reverse('AppWebHome:prueba'))
                elif( rol == 3 ):
                    return HttpResponseRedirect(reverse('AppWebHome:funcionario'))
                elif( rol == 2 ):
                    return HttpResponseRedirect(reverse('AppWebHome:diseñador'))
                elif( rol == 1 ):
                    return HttpResponseRedirect(reverse('AppWebHome:administrador'))
                else:
                    return HttpResponseRedirect(reverse('AppWebHome:perfil'))
                    
            else:
                return HttpResponseRedirect(reverse('AppWebHome:login'))

        else:
            return HttpResponseRedirect(reverse('AppWebHome:login'))


#----------------------------------------------------------------------------------------------------------------#
# Usuarios
#----------------------------------------------------------------------------------------------------------------#

class AdministradorView(LoginRequiredMixin, TemplateView):
    template_name = "usuario/administrador.html"
    # def get() redireccionar dependiendo del rol

    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------


class FuncionarioView(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = "usuario/funcionario.html"
    context_object_name = "usuario"

class DiseñadorView(LoginRequiredMixin, TemplateView):
    template_name = "usuario/diseñador.html"

class PerfilListView(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = "usuario/perfil.html"
    context_object_name = "usuario"


#----------------------------------------------------------------------------------------------------------------#
# CRUDs
#----------------------------------------------------------------------------------------------------------------#

#-----------------------------#
# crud tareas                 #
#-----------------------------#
class CRUDTareaView(LoginRequiredMixin, TemplateView):
    model               = Tarea
    template_name       = "cruds/crud-tarea/crud_tarea.html"
    context_object_name = "tareas"


class TareaDetailView(LoginRequiredMixin, DetailView):
    model = Tarea
    template_name = "cruds/crud-tarea/detalle-tarea.html"
    context_object_name = "tarea"

    # Obtención de otros datos
    def get_context_data(self, *args, **kwargs):
        context             = super().get_context_data(**kwargs)
        context["usuarios"] = Usuario.objects.traer_datos_usuarios()
        context["flujos"]   = Flujo.objects.traer_datos_flujo()
        tareaActual         = Tarea.objects.tareas_id(self.kwargs.get('pk'))
        opFec   = OperacionesFechas
        for t in tareaActual:
            fechaPlazo = t.fecha_plazo
            context["dd"]   = opFec.diferencia_dias(fechaPlazo)
            
        context["fechaActual"]      = opFec.fecha_actual()
        return context

    def eliminar_tarea(request, pk):
        tarea = Tarea.objects.get(id_tarea=pk)
        tarea.delete()
        return HttpResponseRedirect(reverse('AppWebHome:verTareas')+"?page=1")

class VerTareaView(LoginRequiredMixin, ListView):
    model               = Tarea
    paginate_by         = 9
    template_name       = "cruds/crud-tarea/ver-tarea.html"
    context_object_name = "tareas"

    def get_queryset(self): # llena el context_object_name con los datos que traigo
        rol = self.request.user.rol_id_rol.rol
        # jerar = self.request.user.jerarquia_id_jerarquia.jerarquia

        if rol != 'Administrador':
            datos = Tarea.objects.tareas_usuarios(self.request.user.id_usuario).order_by('-id_tarea')
        else:
            datos = Tarea.objects.all().order_by('-id_tarea')

        return datos

    def get_context_data(self, **kwargs):
        opFec   = OperacionesFechas
        idRol = self.request.user.rol_id_rol.id_rol

        if idRol != 1:
            tareas  = Tarea.objects.tareas_usuarios(self.request.user.id_usuario).order_by('-id_tarea')
        else:
            tareas  = Tarea.objects.all().order_by('-id_tarea')
        
        pagina = int(self.request.GET['page'])
        indiceInicio = OperacionesPaginas.calcular_indice_inicio(pagina)
        indiceFinal = OperacionesPaginas.calcular_indice_final(pagina)
        
        context = super().get_context_data(**kwargs)
        dd = []
        pa = []
        i = 0
        for t in tareas:
            if i < indiceFinal:
                fechaInicio = t.fecha_inicio
                fechaPlazo = t.fecha_plazo
                dd.append(opFec.diferencia_dias(fechaPlazo))
                pa.append(opFec.porcentaje_actual(fechaInicio, fechaPlazo))
                i = i+1
            else:
                nada ="nada"
        i = indiceInicio
        # print(i)
        # print(dd)
        del dd[0:i]
        del pa[0:i]

        # print(dd)
        context["diferenciaDias"]       = dd 
        context["porcentajeActual"]     = pa 
        context["fechaActual"]          = opFec.fecha_actual()
        return context


class TareaCreateView(LoginRequiredMixin, FormView):
    model = Tarea
    form_class      = TareaForm
    template_name   = "cruds/crud-tarea/crear-tarea.html"
    success_url     = reverse_lazy("AppWebHome:crearTarea")

    # Validación del formulario
    def form_valid(self, form):
        idUsuario   = Usuario(self.request.POST.get('id_usuario'))
        idFlujo     = Flujo(self.request.POST.get('flujo_id_flujo'))
        idEstado    = Estado(2)
        datos       = form.cleaned_data
        if idFlujo != None:

            Tarea.objects.crear_tarea(
                datos['tarea'],
                datos['descripcion'],
                datos['fecha_inicio'],
                datos['fecha_plazo'],
                idUsuario,
                idFlujo,
                porcentaje_cumplido = 0,
                estado_id_estado    = idEstado,
                )
            return super(TareaCreateView, self).form_valid(form)

        else:
            return HttpResponseRedirect(reverse('AppWebHome:home'))

    # Formulario inválido
    def form_invalid(self, form):
        self.request.session['acusete'] = 'form inválido'
        return super(TareaCreateView, self).form_invalid(form)

    # Obtención de otros datos
    def get_context_data(self, *args, **kwargs):
        context             = super().get_context_data(**kwargs)
        context["usuarios"] = Usuario.objects.traer_datos_usuarios()
        context["flujos"]   = Flujo.objects.traer_datos_flujo()
        context["tareas"]   = Tarea.objects.all()
        return context



#-----------------------------#
# crud flujos                 #
#-----------------------------#
class CRUDFlujoView(LoginRequiredMixin, TemplateView):
    model           = Flujo
    template_name   = "cruds/crud-flujo/crud_flujo.html"

class FlujoCreateView(LoginRequiredMixin, FormView):
    model           = Flujo
    form_class      = FlujoForm
    template_name   = "cruds/crud-flujo/crear-flujo.html"
    success_url     = reverse_lazy("AppWebHome:crearFlujo")

    # Validación del formulario
    def form_valid(self, form):
        idEstado     = Estado(self.request.POST.get('estado_id_estado'))
        datos        = form.cleaned_data
        if idEstado != None:

            Flujo.objects.crear_flujo(
                datos['nombre_flujo'],
                datos['descripcion'],
                idEstado,
                )
            return super(FlujoCreateView, self).form_valid(form)

        else:
            return HttpResponseRedirect(reverse('AppWebHome:home'))

    # Formulario inválido
    def form_invalid(self, form):
        self.request.session['acusete'] = 'form inválido'
        return super(FlujoCreateView, self).form_invalid(form)

    # Obtención de otros datos
    def get_context_data(self, *args, **kwargs):
        context             = super().get_context_data(**kwargs)
        context["estados"]  = Estado.objects.traer_datos_estado()
        return context

class FlujoListView(LoginRequiredMixin, ListView):
    model               = Flujo
    template_name       = "cruds/crud-flujo/ver-flujos.html"
    context_object_name = "flujos"

    def get_context_data(self, **kwargs):
        opFec                   = OperacionesFechas
        context                 = super().get_context_data(**kwargs)
        context["fechaActual"]  = opFec.fecha_actual()
        return context

class FlujoDetailView(LoginRequiredMixin, DetailView):
    model               = Flujo
    template_name       = "cruds/crud-flujo/detalle-flujo.html"
    context_object_name = "flujo"

    def get_context_data(self, *args, **kwargs):
        opFec                   = OperacionesFechas
        context                 = super().get_context_data(**kwargs)
        context["estados"]      = Estado.objects.traer_datos_estado()
        context["tareas"]      = Tarea.objects.all()
        context["fechaActual"]  = opFec.fecha_actual()
        return context

#-----------------------------#
# crud jerarquías             #
#-----------------------------#
class CRUDJerarquiaView(LoginRequiredMixin, ListView):
    model           = Jerarquia
    template_name   = "cruds/crud-jerarquia/crud_jerarquia.html"
    context_object_name = "jerarquias"

class JerarquiaCreateView(LoginRequiredMixin, FormView):
    model           = Jerarquia
    form_class      = JerarquiaForm
    template_name   = "cruds/crud-jerarquia/crear-jerarquia.html"
    success_url     = reverse_lazy("AppWebHome:crearJerarquia")

    # Validación del formulario
    def form_valid(self, form):
        datos = form.cleaned_data
        Jerarquia.objects.crear_jerarquia(
            datos['jerarquia'],
            )
        return super(JerarquiaCreateView, self).form_valid(form)

    # Formulario inválido
    def form_invalid(self, form):
        self.request.session['acusete'] = 'form inválido'
        return super(JerarquiaCreateView, self).form_invalid(form)

    # Obtención de otros datos
    def get_context_data(self, *args, **kwargs):
        context                 = super().get_context_data(**kwargs)
        opFec                   = OperacionesFechas
        context["fechaActual"]  = opFec.fecha_actual()
        context["jerarquias"]   = Jerarquia.objects.traer_datos_jerarquia()
        return context

    def eliminar_jerarquia(request, id):
        jerarquia = Jerarquia.objects.get(id_jerarquia=id)
        jerarquia.delete()
        return HttpResponseRedirect(reverse('AppWebHome:crearJerarquia'))


#-----------------------------#
# crud roles                  #
#-----------------------------#
class CRUDRolView(LoginRequiredMixin, ListView):
    model           = Rol
    template_name   = "cruds/crud-rol/crud_rol.html"
    context_object_name = "roles"

class RolCreateView(LoginRequiredMixin, FormView):
    model           = Rol
    form_class      = RolForm
    template_name   = "cruds/crud-rol/crear-rol.html"
    success_url     = reverse_lazy("AppWebHome:crearRol")

    # Validación del formulario
    def form_valid(self, form):
        datos = form.cleaned_data
        Rol.objects.crear_rol(
            datos['rol'],
            )
        return super(RolCreateView, self).form_valid(form)

    # Formulario inválido
    def form_invalid(self, form):
        self.request.session['acusete'] = 'form inválido'
        return super(RolCreateView, self).form_invalid(form)

    # Obtención de otros datos
    def get_context_data(self, *args, **kwargs):
        context                 = super().get_context_data(**kwargs)
        opFec                   = OperacionesFechas
        context["fechaActual"]  = opFec.fecha_actual()
        context["roles"]        = Rol.objects.all()
        return context

    def eliminar_rol(request, id):
        rol = Rol.objects.get(id_rol=id)
        rol.delete()
        return HttpResponseRedirect(reverse('AppWebHome:crearRol'))



#-----------------------------#
# crud unidades               #
#-----------------------------#
class CRUDUnidadView(LoginRequiredMixin, ListView):
    model           = Unidad
    template_name   = "cruds/crud-unidad/crud_unidad.html"
    context_object_name = "unidades"

class UnidadCreateView(LoginRequiredMixin, FormView):
    model           = Unidad
    form_class      = UnidadForm
    template_name   = "cruds/crud-unidad/crear-unidad.html"
    success_url     = reverse_lazy("AppWebHome:crearUnidad")

    # Validación del formulario
    def form_valid(self, form):
        datos = form.cleaned_data
        Unidad.objects.crear_unidad(
            datos['unidad'],
            )
        return super(UnidadCreateView, self).form_valid(form)

    # Formulario inválido
    def form_invalid(self, form):
        self.request.session['acusete'] = 'form inválido'
        return super(UnidadCreateView, self).form_invalid(form)

    # Obtención de otros datos
    def get_context_data(self, *args, **kwargs):
        context                 = super().get_context_data(**kwargs)
        opFec                   = OperacionesFechas
        context["fechaActual"]  = opFec.fecha_actual()
        context["unidades"]     = Unidad.objects.traer_datos_unidad()
        return context

    def eliminar_unidad(request, id):
        unidad = Unidad.objects.get(id_unidad=id)
        unidad.delete()
        return HttpResponseRedirect(reverse('AppWebHome:crearUnidad'))

#-----------------------------#
# crud usuarios               #
#-----------------------------#
class CRUDUsuarioView(LoginRequiredMixin, TemplateView):
    model           = Usuario
    template_name   = "cruds/crud-usuario/crud_usuario.html"


class UsuarioCreateView(LoginRequiredMixin, FormView):
    model = Usuario
    form_class = UsuarioForm
    template_name = "cruds/crud-usuario/crear-usuario.html"
    success_url     = reverse_lazy("AppWebHome:crearUsuario")

    # Validación del formulario
    def form_valid(self, form):
        idCalle     = Calle(self.request.POST.get('calle_id_calle'))
        idJerarquia = Jerarquia(self.request.POST.get('jerarquia_id_jerarquia'))
        idRol       = Rol(self.request.POST.get('rol_id_rol'))
        idUnidad    = Unidad(self.request.POST.get('unidad_id_unidad'))
        datos       = form.cleaned_data

        Usuario.objects.crear_usuario(
            datos['usuario'],
            datos['contraseña'],
            datos['nombres'],
            datos['apellidos'],
            datos['rut'],
            datos['correo'],
            datos['celular'],
            idCalle,
            idJerarquia,
            idRol,
            idUnidad,
            is_active = 1,
            )
        return super(UsuarioCreateView, self).form_valid(form)


    # Formulario inválido
    def form_invalid(self, form):
        self.request.session['acusete'] = 'form inválido'
        return super(UsuarioCreateView, self).form_invalid(form)

    # Obtención de otros datos
    def get_context_data(self, *args, **kwargs):
        context                 = super().get_context_data(**kwargs)
        context["calles"]       = Calle.objects.all()
        context["jerarquias"]   = Jerarquia.objects.all()
        context["roles"]        = Rol.objects.all()
        context["unidades"]     = Unidad.objects.all()
        return context


class UsuarioListView(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = "cruds/crud-usuario/ver-usuarios.html"
    context_object_name = "usuarios"

    def get_context_data(self, **kwargs):
        opFec                   = OperacionesFechas
        context                 = super().get_context_data(**kwargs)
        context["fechaActual"]  = opFec.fecha_actual()
        return context


class UsuarioDetailView(LoginRequiredMixin, DetailView):
    model = Usuario
    template_name = "cruds/crud-usuario/detalle-usuario.html"
    context_object_name = "usuario"

    def eliminar_usuario(request, pk):
        usuario = Usuario.objects.get(id_usuario=pk)
        usuario.delete()
        return HttpResponseRedirect(reverse('AppWebHome:verUsuarios'))
#----------------------------------------------------------------------------------------------------------------#
# Prueba/Test
#----------------------------------------------------------------------------------------------------------------#
class PruebaView(LoginRequiredMixin, TemplateView):
    template_name = "prueba/prueba.html"

    def get_context_data(self, *args, **kwargs):
        context             = super().get_context_data(**kwargs)
        context["usuarios"] = Usuario.objects.traer_datos_usuarios()
        context["flujos"]   = Flujo.objects.traer_datos_flujo()
        context["tareas"]   = Tarea.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        id_rol = self.request.user.rol_id_rol.id_rol

        if id_rol != 4:
            messages.warning(request, "No puedes ingresar a esta dirección web") 
            if( id_rol == 3 ):
                return HttpResponseRedirect(reverse('AppWebHome:funcionario'))
            elif( id_rol == 2 ):
                return HttpResponseRedirect(reverse('AppWebHome:diseñador'))
            elif( id_rol == 1 ):
                return HttpResponseRedirect(reverse('AppWebHome:administrador'))
            else:
                return HttpResponseRedirect(reverse('AppWebHome:perfil'))
        return super(PruebaView, self).get(request, *args, **kwargs)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('AppWebHome:login'))