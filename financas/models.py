from django.db import models
from django.utils import timezone


class Categoria(models.Model):
    nome = models.CharField(max_length=80, unique=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self) -> str:
        return self.nome


class Pessoa(models.Model):
    nome = models.CharField(max_length=120, unique=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self) -> str:
        return self.nome


class Lancamento(models.Model):
    class Tipo(models.TextChoices):
        ENTRADA = "E", "Entrada"
        SAIDA = "S", "Saída"

    tipo = models.CharField(max_length=1, choices=Tipo.choices)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT, related_name="lancamentos"
    )
    pessoa = models.ForeignKey(Pessoa, on_delete=models.PROTECT, related_name="lancamentos")
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data = models.DateField(default=timezone.localdate)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data", "-criado_em"]

    def __str__(self) -> str:
        return f"{self.get_tipo_display()} - {self.descricao} - {self.valor}"
