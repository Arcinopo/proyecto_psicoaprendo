from django.db import models
from django.contrib.auth.models import User

class Profesor(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profesor'
    )
    nombre = models.CharField(max_length=50, null=True, blank=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    especialidad = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre or self.user.username  # Utilizar el nombre de usuario si no hay nombre


class Estudiante(models.Model):
    profesor = models.ForeignKey(
        Profesor, related_name="estudiantes", on_delete=models.CASCADE
    )
    nombre = models.CharField(max_length=50)
    edad = models.PositiveIntegerField()  # Se especifica el valor positivo para evitar negativos

    def __str__(self):
        return self.nombre


class Prueba(models.Model):
    estudiante = models.ForeignKey(
        Estudiante, related_name="pruebas", on_delete=models.CASCADE
    )
    tipo_prueba = models.CharField(
        max_length=50, choices=[("Sonido", "Sonido"), ("Imagen", "Imagen")], default="Sonido"
    )
    aciertos = models.PositiveIntegerField(default=0)
    intentos = models.PositiveIntegerField(default=0)
    porcentaje_aciertos = models.FloatField(default=0.0)
    fecha = models.DateTimeField(auto_now_add=True)

    def calcular_porcentaje_aciertos(self):
        if self.intentos > 0:
            self.porcentaje_aciertos = (self.aciertos / self.intentos) * 100
        else:
            self.porcentaje_aciertos = 0
        self.save(update_fields=['porcentaje_aciertos'])

    def __str__(self):
        return f"{self.tipo_prueba} - {self.estudiante.nombre} - {self.fecha.strftime('%Y-%m-%d')}"
