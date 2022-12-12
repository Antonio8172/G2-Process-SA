#----------------------------------------------------------------------------------------------------------------#
# Importaciones necesarias
#----------------------------------------------------------------------------------------------------------------#

from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse

from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO
import datetime

class Login():

# Mensaje de alerta por si existen problemas con el login.
    def problemas_login(self): 
        messages.error(self.request, 'No se ha podido iniciar sesión')
        return HttpResponseRedirect(reverse('AppWebHome:login'))

# Autenticación de usuario al loguearse.
    def login_autenticacion(self, usuario, nomUsuario, contraseña):
        # Si el usuario no existe manda un mensaje de alerta, de lo contrario continúa.
        if not usuario:
            return Login.problemas_login(self)

        rol_id = Usuario.objects.traer_datos_usuario(nomUsuario, contraseña)[0][10]
        is_rol = Rol.objects.is_rol_nombre(rol_id)
        # Si el rol del usuario no existe en la base de datos manda un mensaje de alerta, de lo contrario continúa.
        if not is_rol:
            return Login.problemas_login(self)
        
        autUsuario = authenticate(username=nomUsuario, password=contraseña)
        # Si la autenticación del usuario es negada manda un mensaje de alerta, de lo contrario continúa.
        if autUsuario is None:
            return Login.problemas_login(self)

        login(self.request, autUsuario) # Guarda la información para no tener que loguearse en cada instante.

        rol       = self.request.user.rol_id_rol.rol
        jerarquia = self.request.user.jerarquia_id_jerarquia.jerarquia

        if rol == 'Diseñador de Procesos':
            rol = 'diseñador'

        redirect_to = 'AppWebHome:'+rol.lower() # Se guarda en una variable la redirección dependiendo del rol.

        if rol == 'Funcionario':
            messages.success(self.request,'Ha iniciado sesión como '+ jerarquia)

        else:
            messages.success(self.request,'Ha iniciado sesión como '+ rol)

        return HttpResponseRedirect(reverse(redirect_to))

# Verificación de los permisos según el rol para ingresar a ciertas páginas.
    def verificar_permisos_rol(permiso, request):
        if permiso == 'Diseñador de Procesos':
            permiso = 'diseñador'

        redirect_to = 'AppWebHome:'+permiso.lower() # Se guarda en una variable la redirección dependiendo del rol.

        messages.warning(request, 'No posees los permisos necesarios para ingresar a esta página')
        return HttpResponseRedirect(reverse(redirect_to))

# Cerrado de sesión con su respectivo mensaje de alerta y redirección.
    def cerrar_sesion(sel, request):
        logout(request)
        messages.success(request, 'Se ha cerrado la sesión correctamente.')
        return HttpResponseRedirect(reverse('AppWebHome:login'))


class ModificacionesModelos():

# Editar perfil de usuario.
    def editar_perfil(request):
        id_usuario    = request.POST['id_usuario']
        nomUsuario    = request.POST['usuario']
        contraUsuario = request.POST['contra']
        nombres       = request.POST['nombres']
        apellidos     = request.POST['apellidos']
        rut           = request.POST['rut']
        correo        = request.POST['correo']
        celular       = request.POST['celular']
        id_calle      = request.POST['calle']

        usuario = Usuario.objects.get(id_usuario=id_usuario)

        usuario.usuario           = nomUsuario
        usuario.contraseña        = contraUsuario
        usuario.nombres           = nombres
        usuario.apellidos         = apellidos
        usuario.rut               = rut
        usuario.correo            = correo
        usuario.celular           = celular 
        usuario.calle_id_calle_id = id_calle

        usuario.save()
        return HttpResponseRedirect(reverse('AppWebHome:perfil'))

# Crear Tarea
    def crear_tarea(datos, id_user, idFlujo):
        idUsuario   = Usuario(id_user)
        idEstado    = Estado(2)
        tareaCreada = Tarea.objects.crear_tarea(
                                        datos['tarea'],
                                        datos['descripcion'],
                                        datos['fecha_inicio'],
                                        datos['fecha_plazo'],
                                        idUsuario,
                                        idFlujo,
                                        porcentaje_cumplido = 0,
                                        estado_id_estado    = idEstado,)
        return tareaCreada

# Editar tarea
    def editar_tarea(request):
        id_tarea           = request.POST['id_tarea']
        nomTarea           = request.POST[ 'tarea']
        descripcion        = request.POST['descripcion']
        fecha_inicio       = request.POST['fecha_inicio']
        fecha_plazo        = request.POST['fecha_plazo']
        usuario_id_usuario = request.POST['id_usuario']
        id_flujo           = request.POST['flujo_id_flujo']

        tarea = Tarea.objects.get(id_tarea=id_tarea)

        tarea.tarea                 = nomTarea
        tarea.descripcion           = descripcion
        tarea.fecha_inicio          = fecha_inicio
        tarea.fecha_plazo           = fecha_plazo
        tarea.usuario_id_usuario_id = usuario_id_usuario
        tarea.flujo_id_flujo_id     = id_flujo

        tarea.save()
        return HttpResponseRedirect('/detalle-tarea/'+id_tarea+'/')

# Edición del porcentaje de cumplimiento de la tarea.
    def editar_porcentaje_tarea(tarea, porcentajeActual):
        tarea.porcentaje_cumplido = porcentajeActual
        return tarea.save()

# Borrar tarea
    def borrar_tarea(request, pk):
        tarea = Tarea.objects.get(id_tarea=pk)
        tarea.delete()
        messages.success(request, 'La tarea se ha borrado con éxito.')
        return HttpResponseRedirect(reverse('AppWebHome:verTareas')+"?page=1")

# Reportar tarea
    def reportar_problema(request):
        id_tarea = request.POST['id_tarea']
        reporte  = request.POST['reporte']

        tarea = Tarea.objects.get(id_tarea=id_tarea)

        tarea.reporte               = reporte
        tarea.usuario_id_usuario_id = 42

        tarea.save()
        Correo.notificar_reporte(tarea.usuario_id_usuario_id, tarea)
        messages.success(request, 'Tu reporte se ha enviado con éxito.')
        return HttpResponseRedirect(reverse('AppWebHome:verTareas')+"?page=1")
# Crear Flujo
    def crear_flujo(datos, idEstado):
        flujoCreado = Flujo.objects.crear_flujo(
                                        datos['nombre_flujo'],
                                        datos['descripcion'],
                                        idEstado,)
        return flujoCreado

# Editar flujo
    def editar_flujo(request):
        id_flujo         = request.POST['id_flujo']
        nomflujo         = request.POST['nombre_flujo']
        descripcion      = request.POST['descripcion']
        estado_id_estado = request.POST['estado_id_estado']

        flujo = Flujo.objects.get(id_flujo=id_flujo)

        flujo.nombre_flujo        = nomflujo
        flujo.descripcion         = descripcion
        flujo.estado_id_estado_id = estado_id_estado

        flujo.save()
        return HttpResponseRedirect('/detalle-flujo/'+id_flujo+'/')

# Borrar flujo
    def borrar_flujo(request, pk):
        flujo = Flujo.objects.get(id_flujo=pk)
        flujo.delete()
        messages.success(request, 'El flujo se ha borrado con éxito')
        return HttpResponseRedirect(reverse('AppWebHome:verFlujos'))

# Crear Jerarquía
    def crear_jerarquia(datos):
        jerarquiaCreada = Jerarquia.objects.crear_jerarquia(datos['jerarquia'],)
        return jerarquiaCreada

# Borrar Jerarquía
    def borrar_jerarquia(request, id):
        jerarquia = Jerarquia.objects.get(id_jerarquia=id)
        jerarquia.delete()
        messages.success(request, 'La jerarquía se ha borrado con éxito')
        return HttpResponseRedirect(reverse('AppWebHome:crearJerarquia'))

# Crear Rol
    def crear_rol(datos):
        rolCreado = Rol.objects.crear_rol(datos['rol'],)
        return rolCreado

# Borrar Rol
    def borrar_rol(request, id):
        rol = Rol.objects.get(id_rol=id)
        rol.delete()
        messages.success(request, 'El rol se ha borrado con éxito')
        return HttpResponseRedirect(reverse('AppWebHome:crearRol'))

# Crear Unidad
    def crear_unidad(datos):
        unidadCreada = Unidad.objects.crear_unidad(datos['unidad'])
        return unidadCreada

# Borrar Unidad
    def borrar_unidad(request, id):
        unidad = Unidad.objects.get(id_unidad=id)
        unidad.delete()
        messages.success(request, 'La unidad se ha borrado con éxito')
        return HttpResponseRedirect(reverse('AppWebHome:crearUnidad'))

# Crear Usuario
    def crear_usuario(datos, idCalle, idJerarquia, idRol, idUnidad):
        usuarioCreado = Usuario.objects.crear_usuario(
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
            is_active = 1,)
        return usuarioCreado

# Editar Usuario
    def editar_usuario(request):
        id_usuario    = request.POST['id_usuario']
        nomUsuario    = request.POST['usuario']
        contraUsuario = request.POST['contra']
        nombres       = request.POST['nombres']
        apellidos     = request.POST['apellidos']
        rut           = request.POST['rut']
        correo        = request.POST['correo']
        celular       = request.POST['celular']
        id_calle      = request.POST['calle']
        id_rol        = request.POST['rol']
        id_unidad     = request.POST['unidad']
        id_jerarquia  = request.POST['jerarquia']

        usuario = Usuario.objects.get(id_usuario=id_usuario)

        usuario.usuario                   = nomUsuario
        usuario.contraseña                = contraUsuario
        usuario.nombres                   = nombres
        usuario.apellidos                 = apellidos
        usuario.rut                       = rut
        usuario.correo                    = correo
        usuario.celular                   = celular 
        usuario.calle_id_calle_id         = id_calle
        usuario.rol_id_rol_id             = id_rol
        usuario.unidad_id_unidad_id       = id_unidad
        usuario.jerarquia_id_jerarquia_id = id_jerarquia

        usuario.save()
        return HttpResponseRedirect('/detalle-usuario/'+id_usuario+'/')

# Borrar Usuario
    def borrar_usuario(request, pk):
        usuario = Usuario.objects.get(id_usuario=pk)
        usuario.delete()
        messages.success(request, 'El usuario se ha borrado con éxito')
        return HttpResponseRedirect(reverse('AppWebHome:verUsuarios'))


class OperacionesFechas():

# Operación para obtener la fecha actual según el sistema.
    def fecha_actual():
        ahora       = datetime.datetime.now()
        fechaActual = ahora.date()
        return fechaActual

# Operación para obtener la diferencia de días entre la fecha actual y la fecha final de la tarea.
    def diferencia_dias(fechaFinal):
        diferenciaDias = fechaFinal - OperacionesFechas.fecha_actual()
        return diferenciaDias.days

# Operación para obtener el porcentaje actual de cada tarea.
    def porcentaje_actual(fechaInicio, fechaFinal):
        # 100 % en cantidad de días desde el inicio hasta el final de la tarea.
        total = fechaFinal - fechaInicio  
        total = total.days
        # % actual en cantidad de días desde el inicio de la tarea.
        actual = OperacionesFechas.fecha_actual() - fechaInicio 
        actual = actual.days
        # Dependiendo del porcentaje actual se guarda el porcentaje actual en entero.
        if actual <= 0:
            porcActual = 0

        elif actual < total:
            porcActual = (actual*100)/total

        else:
            porcActual = 100

        return int(porcActual)


class OperacionesPaginas():

# Cálculos para obtener los índices de las páginas para la correspondiente y correcta paginación.
    def calcular_indice_inicio(pagina):
        indicePagina = (pagina-1)*9
        return indicePagina
    def calcular_indice_final(pagina):
        indicePagina = (pagina)*9
        return indicePagina


class FuncionesTareas():

# Obtención de una lista de tareas dependiendo del rol y ordenadas por el id de la tarea.
    def lista_tareas_rol(self):
        rol = self.request.user.rol_id_rol.rol
        # Si no es administrador devuelve sólo las tareas que le corresponden al usuario conectado.
        if rol != 'Administrador':
            datos = Tarea.objects.tareas_usuarios(self.request.user.id_usuario).order_by('-id_tarea')
        else:
            datos = Tarea.objects.all().order_by('-id_tarea')
        return datos
    
# Obtención de un diccionario con las listas de la diferencia de días y el porcentaje actual de la paginación correspondiente
    def dict_dd_pa(self):
        tareas = FuncionesTareas.lista_tareas_rol(self)
        
        pagina = int(self.request.GET['page'])
        indiceInicio = OperacionesPaginas.calcular_indice_inicio(pagina)
        indiceFinal  = OperacionesPaginas.calcular_indice_final(pagina)
        
        dictDdPa = {'dd':[], 'pa':[]} # Se crea el diccionario que se modificará posteriormente.

        dd = []
        pa = []
        i  = 0
        # Para cada tarea se guardan la diferencia de días y el porcentaje actual hasta el indice final de la paginación correspondiente.
        for t in tareas:
            if i < indiceFinal:
                fechaInicio  = t.fecha_inicio
                fechaPlazo   = t.fecha_plazo
                porcCumplido = t.porcentaje_cumplido
                porcActual   = OperacionesFechas.porcentaje_actual(fechaInicio, fechaPlazo)
                # Se agrega a la lista 'dd' el valor de la diferencia de días.
                dd.append(OperacionesFechas.diferencia_dias(fechaPlazo))
                # Se agrega a la lista 'pa' el valor del porcentaje actual, y dependiendon de
                # si el porcentaje actual es menor que el valor de la base de datos, lo guarda.
                if porcCumplido < porcActual:
                    pa.append(porcActual)
                    ModificacionesModelos.editar_porcentaje_tarea(t, porcActual)
                else:
                    pa.append(porcCumplido)
                i = i+1

        i = indiceInicio
        # Se eliminan de la lista los valores desde el inicio hasta el indice inicial de la paginación correspondiente.
        del dd[0:i]
        del pa[0:i]

        dictDdPa['dd'] = dd
        dictDdPa['pa'] = pa

        return dictDdPa


class CantidadTareas():

# Obtención de la información correspondiente a la cantidad de tareas de acuerdo al color.
    def color_RGY():
        tareas       = Tarea.objects.all()
        dictCantidad = {'Rojas': 0, 'Verdes': 0, 'Amarillas': 0} # Se define el diccionario para su posterior modificación.

        for t in tareas:
            fechaPlazo   = t.fecha_plazo
            dd           = int(OperacionesFechas.diferencia_dias(fechaPlazo))

            if (dd < 0):
                dictCantidad['Rojas']     += 1

            elif (dd >= 7):
                dictCantidad['Verdes']    += 1

            else:
                dictCantidad['Amarillas'] += 1

        return dictCantidad

# Obtención de la información correspondiente a la cantidad de tareas de acuerdo al color por unidad.
    def unidad_color_RGY():
        tareas       = Tarea.objects.all()
        unidades     = Unidad.objects.all()
        dictCantidad = {}
        i            = 0
        # Se define el diccionario para su posterior modificación.
        for u in unidades:
            dictCantidad[i] = {"Unidad": u.unidad,"Rojas": 0, "Verdes": 0, "Amarillas": 0, 'numero': ''}
            if i % 2 == 0:
                dictCantidad[i]["numero"] = 'par'
            else:
                dictCantidad[i]["numero"] = 'impar'
            i += 1

        for t in tareas:
            usuario = t.usuario_id_usuario
            unidad  = str(usuario.unidad_id_unidad.unidad)

            fechaPlazo = t.fecha_plazo
            dd         = int(OperacionesFechas.diferencia_dias(fechaPlazo))
            i          = 0

            for i in range(len(dictCantidad)):
                if (dictCantidad[i]["Unidad"] == unidad):
                    if (dd < 0):
                        dictCantidad[i]["Rojas"]     += 1
                    elif (dd >= 7):
                        dictCantidad[i]["Verdes"]    += 1
                    else:
                        dictCantidad[i]["Amarillas"] += 1
                    break
                    
                i+= 1

        return dictCantidad

# Obtención de la información correspondiente a la cantidad de tareas de acuerdo a la jerarquía.
    def jerarquia():
        tareas     = Tarea.objects.all()
        jerarquias = Jerarquia.objects.all()

        dictCantidad = {}
        i=0
        # Se define el diccionario para su posterior modificación.
        for j in jerarquias:
            dictCantidad[i] = {"Jerarquia": j.jerarquia,"Cantidad": 0, 'numero': ''}
            if i % 2 == 0:
                dictCantidad[i]["numero"] = 'par'
            else:
                dictCantidad[i]["numero"] = 'impar'
            i += 1

        for t in tareas:
            usuario   = t.usuario_id_usuario
            jerarquia = str(usuario.jerarquia_id_jerarquia.jerarquia)
            i = 0

            for i in range(len(dictCantidad)):
                if (dictCantidad[i]["Jerarquia"] == jerarquia):
                    dictCantidad[i]["Cantidad"] += 1
                    break
                i+= 1

        return dictCantidad


class Correo():

# Se notifica al usuario que se le ha asignado una nueva tarea.
    def notificar_nueva_tarea(idUsuario):
        usuario = Usuario.objects.get(id_usuario=idUsuario)
        correo = usuario.correo

        template = get_template('correos-templates/correoNuevaTarea.html')
        content = template.render()

        email = EmailMultiAlternatives(
            'Tienes una nueva tarea asignada.',
            'Descripción de prueba',
            settings.EMAIL_HOST_USER,
            [correo]
        )
        email.attach_alternative(content, 'text/html')
        return email.send()

    def notificar_reporte(idUsuario, tarea):
        context = {
            'tarea'  : tarea
        }
        usuario = Usuario.objects.get(id_usuario=idUsuario)
        correo = usuario.correo

        template = get_template('correos-templates/reporteTarea.html')
        content = template.render(context)

        email = EmailMultiAlternatives(
            'Reportaron una tarea.',
            'Descripción de prueba',
            settings.EMAIL_HOST_USER,
            [correo]
        )
        email.attach_alternative(content, 'text/html')
        return email.send()


class Html2Pdf():

# Renderización de una plantilla en HTML para poder descargarla en PDF posteriormente.
    def render_2_pdf(template_src, context_dict={}):
        template = get_template(template_src)
        html = template.render(context_dict)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return None