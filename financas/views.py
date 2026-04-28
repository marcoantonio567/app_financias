from decimal import Decimal
from urllib.parse import urlencode

from django.db.models import DecimalField, Sum, Value
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.shortcuts import redirect, render

from financas.forms import LancamentoForm, PinForm
from financas.models import Lancamento


def _pin_redirect(request):
    next_url = request.get_full_path()
    url = reverse("financas:senha")
    return redirect(f"{url}?{urlencode({'next': next_url})}")


def lancamentos_view(request):
    if not request.session.get("pin_ok"):
        return _pin_redirect(request)

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
    if not request.session.get("pin_ok"):
        return _pin_redirect(request)

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


def senha_view(request):
    if request.session.get("pin_ok"):
        return redirect("financas:lancamentos")

    next_url = request.GET.get("next") or ""
    if request.method == "POST":
        form = PinForm(request.POST)
        if form.is_valid():
            request.session["pin_ok"] = True
            request.session.set_expiry(0)
            redirect_to = request.POST.get("next") or ""
            if redirect_to and url_has_allowed_host_and_scheme(
                redirect_to, allowed_hosts={request.get_host()}, require_https=request.is_secure()
            ):
                return redirect(redirect_to)
            return redirect("financas:lancamentos")
    else:
        form = PinForm()

    return render(
        request,
        "financas/senha.html",
        {
            "form": form,
            "next": next_url,
        },
    )
