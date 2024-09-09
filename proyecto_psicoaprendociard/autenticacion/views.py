from django.shortcuts import render

# Create your views here.
def login_view(request):
    return render(request,'autenticacion/login.html')

def registro_view(request):
    return render(request,'autenticacion/registro.html')