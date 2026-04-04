from django.urls import path
from usuarios import views

urlpatterns = [
    path('cadastrar', views.cadastrar, name='cadastrar'),
    path('login', views.login, name='login'),
]
