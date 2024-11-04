from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import ContactoForm
import os

# Vista para la página de inicio
def home_view(request):
    return render(request, "home/home.html")

# Vista para la sección de animales
def animales(request):
    # Lista de animales con sus nombres y rutas de imagen y sonido
    animales = [
        {'nombre': 'perro', 'imagen': 'images/perro.png', 'sonido': 'sounds/perro.mp3', 'nombre_sonido': 'sounds/nombre_perro.mp3'},
        {'nombre': 'gato', 'imagen': 'images/gato.png', 'sonido': 'sounds/gato.mp3', 'nombre_sonido': 'sounds/nombre_gato.mp3'},
        # Añade los demás animales aquí
    ]
    return render(request, 'home/animales.html', {'animales': animales})

# Vista para la sección alfanumérica
def alfanumerico(request):
    return render(request, 'home/alfanumerico.html')

# Vista para la sección de figuras y colores
def figuras_colores(request):
    return render(request, 'home/figuras_colores.html')

# Vista para cuentos
def cuentos(request):
    return render(request, 'home/cuentos.html')

# Vista para el formulario de contacto
def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mensaje enviado exitosamente')
            return redirect('contacto')
    else:
        form = ContactoForm()
    return render(request, 'home/contacto.html', {'form': form})
