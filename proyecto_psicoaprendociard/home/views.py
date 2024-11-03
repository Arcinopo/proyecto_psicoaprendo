from django.shortcuts import render
from .forms import ContactoForm
# Create your views here.
def home_view(request):
    return render(request,"home/home.html")

def alfanumerico(request):
    return render(request, 'home/alfanumerico.html')

def figuras_colores(request):
    return render(request, 'home/figuras_colores.html')

def cuentos(request):
    return render(request, 'home/cuentos.html')

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