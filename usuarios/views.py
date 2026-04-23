from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CadastroUsuarioForm, LoginForm


def login(request):
    if request.user.is_authenticated:
        return redirect("dashboard:index")

    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        auth_login(request, user)
        messages.success(request, f"Bem-vindo(a), {user.username}!")
        return redirect("dashboard:index")

    if request.method == "POST":
        messages.error(request, "Usuário ou senha inválidos.")

    return render(request, "usuarios/login.html", {"form": form})


@login_required
def logout(request):
    auth_logout(request)
    messages.info(request, "Você saiu do sistema.")
    return redirect("usuarios:login")


@login_required
def cadastrar(request):
    form = CadastroUsuarioForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Usuário cadastrado com sucesso.")
        return redirect("dashboard:index")

    return render(request, "usuarios/cadastrar.html", {"form": form})
