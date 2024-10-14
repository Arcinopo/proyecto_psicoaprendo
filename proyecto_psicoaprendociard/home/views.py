from django.shortcuts import render

# Create your views here.
def home_view(request):
    return render(request,"home\home.html")

def alfanumerico(request):
    return render(request, 'home/alfanumerico.html')

def figuras_colores(request):
    return render(request, 'home/figuras_colores.html')

def cuentos(request):
    return render(request, 'home/cuentos.html')

def contacto(request):
    return render(request, 'home/contacto.html')