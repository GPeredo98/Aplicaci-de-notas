from django import forms
from django.contrib.auth.models import User
from notas.models.materia import Materia


class FormMateria(forms.ModelForm):
    nombre = forms.CharField(label='Nombre', max_length=3000, widget=forms.TextInput(
        attrs={
            'id': 'txtNombre',
            'class': 'fadeIn form-control'
        }))
    sigla = forms.CharField(label='Sigla', max_length=5, widget=forms.TextInput(
        attrs={
            'id': 'txtSigla',
            'class': 'fadeIn form-control'
        }))

    docente = forms.ModelChoiceField(label='Docente', queryset=User.objects.filter(groups__name='Docentes'),
                                     empty_label='Escoja un docente...', show_hidden_initial=True,
                                     initial='Escoga un docente', widget=forms.Select(
            attrs={
                'id': 'txtDocente',
                'class': 'fadeIn form-control'
            }))

    estudiantes = forms.ModelMultipleChoiceField(label='Estudiantes', required=False, queryset=User.objects.filter(groups__name='Estudiantes'),
                                             initial='Escoga un alumno', widget=forms.SelectMultiple(
            attrs={
                'id': 'txtEstudiantes',
                'class': 'fadeIn form-control',
                'multiple': 'true'
            }))


    class Meta:
        model = Materia
        fields = ('nombre', 'sigla', 'docente', 'estudiantes')
