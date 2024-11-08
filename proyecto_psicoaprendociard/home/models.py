from django.contrib.auth.models import User
from django.db import models

# Create your models here.
# Modelo para almacenar información adicional del profesor
class Profesor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nombre

# Modelo de Estudiante
class Estudiante(models.Model):
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name="estudiantes")
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.profesor.nombre}"

# Modelo de Prueba para almacenar el rendimiento del estudiante
class Prueba(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name="pruebas")
    fecha_prueba = models.DateTimeField(auto_now_add=True)
    porcentaje_aciertos = models.DecimalField(max_digits=5, decimal_places=2, help_text="Porcentaje de aciertos en la prueba")

    def __str__(self):
        return f"Prueba de {self.estudiante.nombre} - {self.porcentaje_aciertos}% aciertos"
