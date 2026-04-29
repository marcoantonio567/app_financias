from django import forms
from django.conf import settings

from financas.models import Categoria, Lancamento


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


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nome"]
        labels = {
            "nome": "Nome da categoria",
        }
        widgets = {
            "nome": forms.TextInput(
                attrs={"class": "field", "placeholder": "Ex.: Alimentação, Transporte"}
            ),
        }


class PinForm(forms.Form):
    pin = forms.CharField(
        label="Senha (6 dígitos)",
        min_length=6,
        max_length=6,
        widget=forms.PasswordInput(
            attrs={
                "class": "field",
                "inputmode": "numeric",
                "autocomplete": "one-time-code",
                "pattern": r"\d{6}",
                "placeholder": "••••••",
            }
        ),
    )

    def clean_pin(self):
        pin = self.cleaned_data["pin"]
        if not pin.isdigit() or len(pin) != 6:
            raise forms.ValidationError("Digite uma senha de 6 dígitos.")
        if pin != getattr(settings, "FINANCEIRO_APP_PIN", ""):
            raise forms.ValidationError("Senha incorreta.")
        return pin
