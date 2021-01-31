from django import forms
from django.contrib.auth.models import User
from notas.models.nota import Nota


class FormNota(forms.ModelForm):

    primer_parcial = forms.IntegerField(label='Primer parcial', required=False, widget=forms.NumberInput(
        attrs={
            'id': 'txtPrimerParcial',
            'class': 'form-control'
        }
    ), max_value=100, min_value=0)
    segundo_parcial = forms.IntegerField(label='Segundo parcial', required=False, widget=forms.NumberInput(
        attrs={
            'id': 'txtSegundoParcial',
            'class': 'form-control'
        }
    ), max_value=100, min_value=0)
    examen_final = forms.IntegerField(label='Examen final', required=False, widget=forms.NumberInput(
        attrs={
            'id': 'txtExamenFinal',
            'class': 'form-control'
        }
    ), max_value=100, min_value=0)
    controles = forms.IntegerField(label='Controles', required=False, widget=forms.NumberInput(
        attrs={
            'id': 'txtControles',
            'class': 'form-control'
        }
    ), max_value=100, min_value=0)
    practicos = forms.IntegerField(label='Practicos', required=False, widget=forms.NumberInput(
        attrs={
            'id': 'txtPracticos',
            'class': 'form-control'
        }
    ), max_value=100, min_value=0)
    estudiante = forms.ModelChoiceField(label='Estudiante', required=False,
                                        queryset=User.objects.filter(groups__name='Estudiantes'),
                                        initial='Elija un estudiante')

    class Meta:
        model = Nota
        fields = ('primer_parcial', 'segundo_parcial', 'examen_final', 'controles', 'practicos', 'estudiante')