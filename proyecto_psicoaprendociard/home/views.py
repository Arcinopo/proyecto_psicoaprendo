from django.shortcuts import redirect, render,get_object_or_404
from django.contrib import messages
import os
from django.contrib.auth.decorators import login_required
from home.models import Estudiante, Profesor
from .forms import EstudianteForm, ProfesorForm
from django.http import JsonResponse

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


@login_required
def ver_rendimiento_estudiantes(request):
    profesor = request.user.profesor
    estudiantes = profesor.estudiantes.all()  # Obtener todos los estudiantes del profesor
    return render(request, 'home/rendimiento_estudiantes.html', {'estudiantes': estudiantes})


@login_required
def registrar_estudiante(request):
    if request.method == 'POST':
        form = EstudianteForm(request.POST)
        if form.is_valid():
            estudiante = form.save(commit=False)
            estudiante.profesor = request.user.profesor  # Asigna el profesor actual si está autenticado
            estudiante.save()
            return redirect('registrar_estudiante')  # Cambia a la URL a donde redirigir después de guardar
    else:
        form = EstudianteForm()

    return render(request, 'home/registrar_estudiante.html', {'form': form})

@login_required
def gestionar_estudiante(request):
    # Obtener el ID del estudiante que se quiere editar (si lo hay)
    edit_id = request.GET.get('edit_id')
    estudiante = None
    if edit_id:
        # Intenta obtener el estudiante, y maneja el caso si no existe
        try:
            estudiante = Estudiante.objects.get(id=edit_id, profesor=request.user.profesor)
        except Estudiante.DoesNotExist:
            messages.error(request, 'Estudiante no encontrado.')
            return redirect('gestionar_estudiante')

    if request.method == 'POST':
        # Eliminar estudiante
        if 'delete_id' in request.POST:
            delete_id = request.POST['delete_id']
            try:
                estudiante_a_eliminar = Estudiante.objects.get(id=delete_id, profesor=request.user.profesor)
                estudiante_a_eliminar.delete()
                messages.success(request, 'Estudiante eliminado con éxito.')
            except Estudiante.DoesNotExist:
                messages.error(request, 'Estudiante no encontrado o no tienes permiso para eliminarlo.')
            return redirect('gestionar_estudiante')

        # Crear o editar estudiante
        form = EstudianteForm(request.POST, instance=estudiante)
        if form.is_valid():
            nuevo_estudiante = form.save(commit=False)
            nuevo_estudiante.profesor = request.user.profesor
            nuevo_estudiante.save()
            if edit_id:
                messages.success(request, 'Estudiante actualizado con éxito.')
            else:
                messages.success(request, 'Estudiante registrado con éxito.')
            return redirect('gestionar_estudiante')
    else:
        form = EstudianteForm(instance=estudiante)

    estudiantes = Estudiante.objects.filter(profesor=request.user.profesor)
    return render(request, 'home/gestionar_estudiante.html', {
        'form': form,
        'estudiantes': estudiantes,
        'estudiante': estudiante
    })


@login_required
def editar_perfil_profesor(request):
    try:
        profesor = request.user.profesor
    except Profesor.DoesNotExist:
        profesor = Profesor(user=request.user)

    if request.method == 'POST':
        form = ProfesorForm(request.POST, instance=profesor)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirige a la página principal o a otra página
    else:
        form = ProfesorForm(instance=profesor)

    return render(request, 'home/editar_perfil_profesor.html', {'form': form})