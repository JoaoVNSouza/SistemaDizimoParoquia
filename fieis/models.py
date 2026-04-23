from django.db import models


class Fiel(models.Model):
    nome = models.CharField("Nome completo", max_length=150)
    cpf = models.CharField("CPF", max_length=14, unique=True)
    data_nascimento = models.DateField("Data de nascimento", null=True, blank=True)
    telefone = models.CharField("Telefone", max_length=20, blank=True)
    email = models.EmailField("E-mail", blank=True)

    rua = models.CharField("Rua", max_length=150, blank=True)
    numero = models.CharField("Número", max_length=10, blank=True)
    bairro = models.CharField("Bairro", max_length=100, blank=True)
    cidade = models.CharField("Cidade", max_length=100, blank=True, default="Itaquiraí")

    data_cadastro = models.DateTimeField("Data de cadastro", auto_now_add=True)
    ativo = models.BooleanField("Ativo", default=True)

    class Meta:
        verbose_name = "Fiel"
        verbose_name_plural = "Fiéis"
        ordering = ["nome"]

    def __str__(self):
        return self.nome

    @property
    def endereco_completo(self):
        partes = [self.rua, self.numero, self.bairro, self.cidade]
        return ", ".join([p for p in partes if p])
