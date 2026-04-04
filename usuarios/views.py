from django.shortcuts import render, HttpResponse


# Create your views here.
def cadastrar(request):
    return HttpResponse('Cadastrar')


def login(request):
    return HttpResponse('Login')
