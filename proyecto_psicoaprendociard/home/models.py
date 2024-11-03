from django.db import models

# Create your models here.
class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

class Cuento(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_publicacion = models.DateField()

class FiguraColor(models.Model):
    figura = models.CharField(max_length=50)
    color = models.CharField(max_length=50)