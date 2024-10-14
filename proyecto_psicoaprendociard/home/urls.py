from django.urls import path
from .views import home_view, alfanumerico, figuras_colores, cuentos, contacto

urlpatterns = [
    path('', home_view, name='home'),
    path('alfanumerico/', alfanumerico, name='alfanumerico'),
    path('figuras_colores/', figuras_colores, name='figuras_colores'),
    path('cuentos/', cuentos, name='cuentos'),
    path('contacto/', contacto, name='contacto'),
]
