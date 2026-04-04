from django.shortcuts import render


# Create your views here.
def cadastrar(request):
    if request.method == 'GET':
        return render(request, 'usuarios/cadastrar.html')

    if request.method == 'POST':
        return render(request, 'usuarios/cadastrar.html')


def login(request):
    if request.method == 'GET':
        return render(request, 'usuarios/login.html')

    if request.method == 'POST':
        return render(request, 'usuarios/login.html')
