from django.contrib import admin
from .models import Fiel


@admin.register(Fiel)
class FielAdmin(admin.ModelAdmin):
    list_display = ("nome", "cpf", "telefone", "cidade", "ativo", "data_cadastro")
    list_filter = ("ativo", "cidade")
    search_fields = ("nome", "cpf", "email")
    ordering = ("nome",)
