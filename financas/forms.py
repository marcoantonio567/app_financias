from django import forms

from financas.models import Lancamento


class LancamentoForm(forms.ModelForm):
    class Meta:
        model = Lancamento
        fields = ["tipo", "descricao", "valor", "data"]
        labels = {
            "tipo": "Tipo",
            "descricao": "Descrição",
            "valor": "Valor (R$)",
            "data": "Data",
        }
        widgets = {
            "tipo": forms.Select(attrs={"class": "field"}),
            "descricao": forms.TextInput(
                attrs={"class": "field", "placeholder": "Ex.: Salário, Aluguel"}
            ),
            "valor": forms.NumberInput(
                attrs={
                    "class": "field",
                    "step": "0.01",
                    "min": "0",
                    "inputmode": "decimal",
                    "placeholder": "0,00",
                }
            ),
            "data": forms.DateInput(attrs={"class": "field", "type": "date"}),
        }
