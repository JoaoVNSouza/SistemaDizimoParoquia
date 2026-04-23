from django.contrib import admin
from .models import Dizimo


@admin.register(Dizimo)
class DizimoAdmin(admin.ModelAdmin):
    list_display = ("fiel", "valor", "referencia", "data_pagamento", "forma_pagamento", "pago")
    list_filter = ("pago", "forma_pagamento", "data_pagamento")
    search_fields = ("fiel__nome", "fiel__cpf")
    autocomplete_fields = ("fiel",)
    date_hierarchy = "data_pagamento"
