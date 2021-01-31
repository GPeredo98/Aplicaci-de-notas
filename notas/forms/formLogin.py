from django import forms


class FormLogin(forms.Form):
    username = forms.CharField(label='Nombre de usuario', max_length=300, widget=forms.TextInput(
        attrs={
            'id': 'txtUsername',
            'class': 'fadeIn form-control',
            'placeholder': 'Usuario'
        }
    ))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(
        attrs={
            'id': 'txtPassword',
            'class': 'fadeIn form-control',
            'placeholder': 'Contraseña'
        }
    ))

    class Meta:
        fields = ('username', 'password')
