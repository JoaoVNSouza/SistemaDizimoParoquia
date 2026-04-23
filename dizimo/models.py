from django.db import models
from fieis.models import Fiel


class Dizimo(models.Model):
    class FormaPagamento(models.TextChoices):
        DINHEIRO = "DINHEIRO", "Dinheiro"
        PIX = "PIX", "PIX"
        CARTAO = "CARTAO", "Cartão"

    fiel = models.ForeignKey(
        Fiel, on_delete=models.PROTECT, related_name="dizimos", verbose_name="Fiel"
    )
    valor = models.DecimalField("Valor", max_digits=10, decimal_places=2)
    data_pagamento = models.DateField("Data de pagamento")
    referencia = models.DateField("Referência (mês/ano)")
    forma_pagamento = models.CharField(
        "Forma de pagamento",
        max_length=20,
        choices=FormaPagamento.choices,
        default=FormaPagamento.DINHEIRO,
    )
    pago = models.BooleanField("Pago", default=True)
    observacao = models.TextField("Observação", blank=True)
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)

    class Meta:
        verbose_name = "Dízimo"
        verbose_name_plural = "Dízimos"
        ordering = ["-data_pagamento", "-criado_em"]

    def __str__(self):
        return f"{self.fiel.nome} — R$ {self.valor} ({self.referencia:%m/%Y})"

    @property
    def referencia_formatada(self):
        return self.referencia.strftime("%m/%Y")
