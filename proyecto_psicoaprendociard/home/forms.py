
from django import forms
from .models import Estudiante, Profesor

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['nombre', 'edad']

class ProfesorForm(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = ['especialidad', 'telefono']