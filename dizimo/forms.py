from datetime import date, datetime

from django import forms

from .models import Dizimo


class DizimoForm(forms.ModelForm):
    class Meta:
        model = Dizimo
        fields = [
            "fiel", "valor", "data_pagamento", "referencia",
            "forma_pagamento", "observacao", "pago",
        ]
        widgets = {
            "fiel": forms.Select(attrs={"class": "form-select"}),
            "valor": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01", "min": "0"}
            ),
            "data_pagamento": forms.DateInput(
                attrs={"type": "date", "class": "form-control"},
                format="%Y-%m-%d",
            ),
            "referencia": forms.DateInput(
                attrs={"type": "month", "class": "form-control"},
                format="%Y-%m",
            ),
            "forma_pagamento": forms.Select(attrs={"class": "form-select"}),
            "observacao": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "pago": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["data_pagamento"].input_formats = ["%Y-%m-%d"]
        self.fields["referencia"].input_formats = ["%Y-%m", "%Y-%m-%d"]

    def clean_valor(self):
        valor = self.cleaned_data.get("valor")
        if valor is None or valor <= 0:
            raise forms.ValidationError("Valor deve ser maior que zero.")
        return valor

    def clean_referencia(self):
        referencia = self.cleaned_data.get("referencia")
        if isinstance(referencia, datetime):
            referencia = referencia.date()
        if isinstance(referencia, date):
            return referencia.replace(day=1)
        return referencia
