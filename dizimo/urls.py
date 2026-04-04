from django.urls import path
from dizimo import views

urlpatterns = [
    path('', views.index, name='index'),
]
