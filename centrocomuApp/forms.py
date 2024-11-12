from django import forms
from django.contrib.auth.hashers import make_password
from .models import Usuario, CitaPsicologica, Disponibilidad

class RegistroForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar contraseña'}))
    
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'rut', 'calle', 'numero', 'fono', 'email', 'password', 'tipo_usuario']
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    rut = forms.CharField(max_length=10)
    password = forms.CharField(widget=forms.PasswordInput)

class DisponibilidadForm(forms.ModelForm):
    class Meta:
        model = Disponibilidad
        fields = ['fecha', 'hora_inicio', 'hora_fin']

class CitaForm(forms.ModelForm):
    class Meta:
        model = CitaPsicologica
        fields = ['fecha', 'hora', 'motivo']
