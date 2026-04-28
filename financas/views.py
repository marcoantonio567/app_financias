from decimal import Decimal

from django.db.models import DecimalField, Sum, Value
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from financas.forms import LancamentoForm
from financas.models import Lancamento


def lancamentos_view(request):
    if request.method == "POST":
        form = LancamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("financas:lancamentos")
    else:
        form = LancamentoForm()

    total_output_field = DecimalField(max_digits=12, decimal_places=2)
    total_entradas = (
        Lancamento.objects.filter(tipo=Lancamento.Tipo.ENTRADA).aggregate(
            total=Coalesce(
                Sum("valor"),
                Value(0, output_field=total_output_field),
                output_field=total_output_field,
            )
        )["total"]
    )
    total_saidas = (
        Lancamento.objects.filter(tipo=Lancamento.Tipo.SAIDA).aggregate(
            total=Coalesce(
                Sum("valor"),
                Value(0, output_field=total_output_field),
                output_field=total_output_field,
            )
        )["total"]
    )
    total_entradas = total_entradas.quantize(Decimal("0.01"))
    total_saidas = total_saidas.quantize(Decimal("0.01"))
    saldo = (total_entradas - total_saidas).quantize(Decimal("0.01"))

    ultimos = Lancamento.objects.all()[:20]

    return render(
        request,
        "financas/lancamentos.html",
        {
            "form": form,
            "ultimos": ultimos,
            "total_entradas": total_entradas,
            "total_saidas": total_saidas,
            "saldo": saldo,
        },
    )


def historico_view(request):
    qs = Lancamento.objects.all()
    paginator = Paginator(qs, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "financas/historico.html",
        {
            "page_obj": page_obj,
        },
    )
