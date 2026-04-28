from django.db import models
from django.utils import timezone


class Lancamento(models.Model):
    class Tipo(models.TextChoices):
        ENTRADA = "E", "Entrada"
        SAIDA = "S", "Saída"

    tipo = models.CharField(max_length=1, choices=Tipo.choices)
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data = models.DateField(default=timezone.localdate)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data", "-criado_em"]

    def __str__(self) -> str:
        return f"{self.get_tipo_display()} - {self.descricao} - {self.valor}"
