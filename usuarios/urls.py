from django.urls import path
from . import views

app_name = "usuarios"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("cadastrar/", views.cadastrar, name="cadastrar"),
]
