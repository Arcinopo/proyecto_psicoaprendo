from django.shortcuts import redirect, render,get_object_or_404
from django.contrib import messages
import os
from django.contrib.auth.decorators import login_required
from home.models import Estudiante, Profesor, Prueba
from .forms import EstudianteForm, ProfesorForm, SeleccionarEstudianteForm
from django.http import JsonResponse
import random
from django.templatetags.static import static

# Vista para la página de inicio
def home_view(request):
    # Lista de nombres de archivos de imagen
    imagenes = [f'galeria{i}.png' for i in range(1, 13)]  # galeria1.png hasta galeria12.png
    return render(request, "home/home.html",{'imagenes': imagenes})

# Vista para la sección de animales
def animales(request):
    # Lista de animales con sus nombres y rutas de imagen y sonido
    animales = [
        {'nombre': 'gato', 'imagen': 'images/gato.png', 'sonido': 'sounds/gato.mp3', 'nombre_sonido': 'sounds/nombre_gato.mp3'},
        {'nombre': 'vaca', 'imagen': 'images/vaca.png', 'sonido': 'sounds/vaca.mp3', 'nombre_sonido': 'sounds/nombre_vaca.mp3'},
        {'nombre': 'caballo', 'imagen': 'images/caballo.png', 'sonido': 'sounds/caballo.mp3', 'nombre_sonido': 'sounds/nombre_caballo.mp3'},
        {'nombre': 'elefante', 'imagen': 'images/elefante.png', 'sonido': 'sounds/elefante.mp3', 'nombre_sonido': 'sounds/nombre_elefante.mp3'},
        {'nombre': 'perro', 'imagen': 'images/perro.png', 'sonido': 'sounds/perro.mp3', 'nombre_sonido': 'sounds/nombre_perro.mp3'},
        # puedo añadir más animales
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

# Vista para contactos
def contacto(request):
    return render(request, 'home/contacto.html')

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


###################################################################################

@login_required
def prueba_view(request):
    resultado = None
    mensaje_resultado = None
    tipo_prueba = random.choice(['Sonido', 'Imagen'])
    opciones_respuesta = []
    archivo_prueba = None

    # Mantener el estudiante seleccionado y el contador de preguntas en la sesión
    if request.method == 'POST' and 'estudiante' in request.POST:
        form = SeleccionarEstudianteForm(request.POST)
        if form.is_valid():
            estudiante = form.cleaned_data['estudiante']
            request.session['estudiante_id'] = estudiante.id
            request.session['preguntas_respondidas'] = 0  # Contador de preguntas
            request.session['aciertos'] = 0  # Contador de aciertos
            # Limpiar cualquier dato anterior de respuesta en la sesión
            request.session.pop('respuesta_correcta', None)
            request.session.pop('archivo_prueba', None)
            request.session.pop('opciones_respuesta', None)
        else:
            estudiante = None
    else:
        estudiante_id = request.session.get('estudiante_id')
        estudiante = Estudiante.objects.get(id=estudiante_id) if estudiante_id else None
        form = SeleccionarEstudianteForm()

    # Si hay un estudiante seleccionado, generar una nueva pregunta solo si es necesario
    if estudiante and request.session.get('preguntas_respondidas', 0) < 5:
        # Generar nueva pregunta solo si no existe una activa en la sesión
        if 'respuesta_correcta' not in request.session: 
            if tipo_prueba == 'Sonido':
                sonidos = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'ñ', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'x', 'y', 'z',
                           'gato', 'perro', 'caballo', 'vaca', 'elefante', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
                respuesta_correcta = random.choice(sonidos)
                archivo_prueba = static(f'sounds/{respuesta_correcta}.mp3')
                # Generar opciones sin incluir la respuesta correcta, luego agregarla manualmente
                opciones_respuesta = random.sample([sonido for sonido in sonidos if sonido != respuesta_correcta], 4)
            elif tipo_prueba == 'Imagen':
                imagenes = ['gato', 'perro', 'caballo', 'elefante', 'vaca']
                respuesta_correcta = random.choice(imagenes)
                archivo_prueba = static(f'images/{respuesta_correcta}.png')
                opciones_respuesta = random.sample([imagen for imagen in imagenes if imagen != respuesta_correcta], 2)

            # Añadir la respuesta correcta a las opciones y mezclarlas
            opciones_respuesta.append(respuesta_correcta)
            random.shuffle(opciones_respuesta)

            # Guardar en la sesión para asegurar consistencia en la misma pregunta
            request.session['respuesta_correcta'] = respuesta_correcta
            request.session['archivo_prueba'] = archivo_prueba
            request.session['opciones_respuesta'] = opciones_respuesta
        else:
            # Recuperar la pregunta actual de la sesión si ya fue generada
            respuesta_correcta = request.session['respuesta_correcta']
            archivo_prueba = request.session['archivo_prueba']
            opciones_respuesta = request.session['opciones_respuesta']

    # Procesar la respuesta del estudiante
    if request.method == 'POST' and 'respuesta_estudiante' in request.POST:
        respuesta_estudiante = request.POST.get('respuesta_estudiante')

        # Comparar con la respuesta correcta almacenada en la sesión
        if respuesta_estudiante == request.session['respuesta_correcta']:
            resultado = 'correcto'
            mensaje_resultado = "¡Respuesta correcta!"
            request.session['aciertos'] += 1
        else:
            resultado = 'incorrecto'
            mensaje_resultado = "Respuesta incorrecta. Intenta de nuevo."

        # Incrementar el contador de preguntas y eliminar los datos de la pregunta actual
        request.session['preguntas_respondidas'] += 1
        del request.session['respuesta_correcta']
        del request.session['archivo_prueba']
        del request.session['opciones_respuesta']

        # Si se alcanzan 5 preguntas, guardar los resultados y redirigir a gestionar_estudiante
        if request.session['preguntas_respondidas'] >= 5:
            aciertos = request.session['aciertos']
            prueba, created = Prueba.objects.get_or_create(
                estudiante=estudiante, tipo_prueba=tipo_prueba
            )
            prueba.intentos += 5  # Total de preguntas realizadas
            prueba.aciertos += aciertos  # Total de aciertos en la sesión
            prueba.calcular_porcentaje_aciertos()

            # Limpiar datos de la sesión para la próxima vez
            del request.session['estudiante_id']
            del request.session['preguntas_respondidas']
            del request.session['aciertos']

            # Redirigir a gestionar_estudiante para ver el rendimiento
            return redirect('gestionar_estudiante')

    context = {
        'form': form,
        'estudiante': estudiante,
        'tipo_prueba': tipo_prueba,
        'archivo_prueba': archivo_prueba,
        'resultado': resultado,
        'mensaje_resultado': mensaje_resultado,
        'opciones_respuesta': opciones_respuesta
    }
    return render(request, 'home/prueba.html', context)