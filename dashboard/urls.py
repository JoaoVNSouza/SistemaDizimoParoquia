from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.index, name="index"),
    path("historico/<int:pk>/", views.historico_fiel, name="historico"),
    path("relatorio/", views.relatorio, name="relatorio"),
]
