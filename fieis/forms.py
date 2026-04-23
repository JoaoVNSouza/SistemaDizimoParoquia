from django import forms
from .models import Fiel
import re


class FielForm(forms.ModelForm):
    class Meta:
        model = Fiel
        fields = [
            "nome", "cpf", "data_nascimento", "telefone", "email",
            "rua", "numero", "bairro", "cidade", "ativo"
        ]
        widgets = {
            "data_nascimento": forms.DateInput(
                attrs={"type": "date", "class": "form-control"},
                format="%Y-%m-%d"
            ),
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "cpf": forms.TextInput(attrs={"class": "form-control", "placeholder": "000.000.000-00"}),
            "telefone": forms.TextInput(attrs={"class": "form-control", "placeholder": "(00) 00000-0000"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "email@exemplo.com"}),
            "rua": forms.TextInput(attrs={"class": "form-control"}),
            "numero": forms.TextInput(attrs={"class": "form-control"}),
            "bairro": forms.TextInput(attrs={"class": "form-control"}),
            "cidade": forms.TextInput(attrs={"class": "form-control"}),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf", "")
        cpf_limpo = re.sub(r"[^0-9]", "", cpf)

        if len(cpf_limpo) != 11:
            raise forms.ValidationError("CPF deve ter 11 dígitos.")

        return f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"

    def clean_telefone(self):
        telefone = self.cleaned_data.get("telefone", "")
        numeros = re.sub(r"[^0-9]", "", telefone)

        if len(numeros) < 10:
            raise forms.ValidationError("Telefone deve ter pelo menos 10 dígitos.")

        return numeros
