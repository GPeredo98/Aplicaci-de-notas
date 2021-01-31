from django import forms
from django.contrib.auth.models import User, Group
from django.core.validators import MaxValueValidator, MinValueValidator


class UsersForm(forms.ModelForm):
    username = forms.CharField(label='Usuario', widget=forms.TextInput(
        attrs={
            'id': 'txtUsername',
            'class': 'form-control'
        }
    ))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(
        attrs={
            'id': 'txtPassword',
            'class': 'form-control'
        }
    ))
    first_name = forms.CharField(label='Nombre', widget=forms.TextInput(
        attrs={
            'id': 'txtUsername',
            'class': 'form-control'
        }
    ))
    last_name = forms.CharField(label='Apellido', widget=forms.TextInput(
        attrs={
            'id': 'txtApellido',
            'class': 'form-control'
        }
    ))
    email = forms.EmailField(label='Correo', widget=forms.TextInput(
        attrs={
            'id': 'txtCorreo',
            'class': 'form-control'
        }
    ))
    group = forms.ModelChoiceField(label='Rol', queryset=Group.objects.all(), initial='Especifique su rol')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'group')