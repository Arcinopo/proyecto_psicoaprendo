from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', login_required(views.home_view), name='home'),
    path('alfanumerico/', login_required(views.alfanumerico), name='alfanumerico'),
    path('figuras_colores/', login_required(views.figuras_colores), name='figuras_colores'),
    path('animales/', login_required(views.animales), name='animales'),
    path('gestionar_estudiante/', views.gestionar_estudiante, name='gestionar_estudiante'),
    path('editar_perfil/', views.editar_perfil_profesor, name='editar_perfil_profesor'),
    ]
