#----------------------------------------------------------------------------------------------------------------#
# Importaciones necesarias
#----------------------------------------------------------------------------------------------------------------#

from cProfile import label
from dataclasses import fields
from pyexpat import model
from django import forms
from .models import *

#----------------------------------------------------------------------------------------------------------------#
# Formularios
#----------------------------------------------------------------------------------------------------------------#

class LoginForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'usuario',
            'contraseña'
        ]
        widgets = {
            'usuario'           : forms.TextInput(attrs={
                'class'       : 'form-login',
                'placeholder' : 'Nombre de usuario',
                'style'       : 'width: 168px;',
                'required'    : 'true',
            }),
            'contraseña'        : forms.PasswordInput(attrs={
                'class'       : 'form-login',
                'placeholder' : 'Contraseña',
                'style'       : 'width: 168px;',
                'required'    : 'true',
            })
        }

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'usuario',
            'contraseña',
            'nombres',
            'apellidos',
            'rut',
            'correo',
            'celular',
        ]
        widgets = {
            'usuario'               : forms.TextInput(attrs={
                'class'         : 'form-control',
                'placeholder'   : 'Nombre de Usuario',
                'width'         : '300px',
                'required'      : 'true',
            }),
            'contraseña'            : forms.TextInput(attrs={
                'class'         : 'form-control',
                'placeholder'   : 'Contraseña',
                'width'         : '300px',
                'required'      : 'true',
            }),
            'nombres'               : forms.TextInput(attrs={
                'class'         : 'form-control',
                'placeholder'   : 'Primer y Segundo Nombre',
                'width'         : '300px',
                'required'      : 'true',
            }),
            'apellidos'             : forms.TextInput(attrs={
                'class'         : 'form-control',
                'placeholder'   : 'Apellido Paterno y Materno',
                'width'         : '300px',
                'required'      : 'true',
            }),
            'rut'                   : forms.TextInput(attrs={
                'class'         : 'form-control',
                'placeholder'   : '12345678-9',
                'width'         : '300px',
                'required'      : 'true',
            }),
            'correo'                : forms.TextInput(attrs={
                'class'         : 'form-control',
                'placeholder'   : 'NombreApellido@gmail.com',
                'width'         : '300px',
                'required'      : 'true',
            }),
            'celular'               : forms.TextInput(attrs={
                'class'         : 'form-control',
                'placeholder'   : '+56987654321',
                'width'         : '300px',
                'required'      : 'true',
            }),

        }


class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = [
            'tarea',
            'descripcion',
            'fecha_inicio',
            'fecha_plazo',
        ]
        widgets = {
            'tarea'                      : forms.TextInput(attrs={
                'class'     : 'form-control',
                'width'     : '300px',
                'required'  : 'true',
            }),
            'descripcion'                : forms.Textarea(attrs={
                'class'     : 'form-control',
                'cols'      : '43',
                'rows'      : '4',
                'style'     : 'resize: none; font-family: monospace;',
                'required'  : 'true',
            }),
            'fecha_inicio'               : forms.DateInput(format=('%d-%m-%Y'), attrs={
                'class'     : 'form-control',
                'type'      : 'date',
                'required'  : 'true',
            }),
            'fecha_plazo'                : forms.DateInput(format=('%d-%m-%Y'), attrs={
                'class'     : 'form-control',
                'type'      : 'date',
                'required'  : 'true',
            }),
        }

class FlujoForm(forms.ModelForm):
    class Meta:
        model = Flujo
        fields = [
            'nombre_flujo',
            'descripcion',
        ]
        widgets = {
            'nombre_flujo'              : forms.TextInput(attrs={
                'class'     : 'form-control',
                'width'     : '300px',
                'required'  : 'true',
            }),
            'descripcion'               :forms.Textarea(attrs={
                'class'     : 'form-control',
                'cols'      : '43',
                'rows'      : '4',
                'style'     : 'resize: none; font-family: monospace;',
                'required'  : 'true',
            }),
        }


class JerarquiaForm(forms.ModelForm):
    class Meta:
        model = Jerarquia
        fields = [
            'jerarquia',
        ]
        widgets = {
            'jerarquia' : forms.TextInput(attrs={
                'class'     : 'form-control',
                'width'     : '300px',
                'required'  : 'true',
            })
        }
        
class RolForm(forms.ModelForm):
    class Meta:
        model = Rol
        fields = [
            'rol',
        ]
        widgets = {
            'rol' : forms.TextInput(attrs={
                'class'     : 'form-control',
                'width'     : '300px',
                'required'  : 'true',
            })
        }

class UnidadForm(forms.ModelForm):
    class Meta:
        model = Unidad
        fields = [
            'unidad',
        ]
        widgets = {
            'unidad' : forms.TextInput(attrs={
                'class'     : 'form-control',
                'width'     : '300px',
                'required'  : 'true',
            })
        }
