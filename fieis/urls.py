from django.urls import path
from . import views

app_name = "fieis"

urlpatterns = [
    path("", views.listar, name="listar"),
    path("cadastrar/", views.cadastrar, name="cadastrar"),
    path("editar/<int:pk>/", views.editar, name="editar"),
    path("detalhar/<int:pk>/", views.detalhar, name="detalhar"),
    path("excluir/<int:pk>/", views.excluir, name="excluir"),
    path("inativar/<int:pk>/", views.inativar, name="inativar"),
]
