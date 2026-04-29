import json
from datetime import date, timedelta
from decimal import Decimal
from urllib.parse import urlencode

from django.db.models.deletion import ProtectedError
from django.db.models import DecimalField, Sum, Value
from django.db.models.functions import Coalesce
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from financas.forms import CategoriaForm, LancamentoForm, PessoaForm, PinForm
from financas.models import Categoria, Lancamento, Pessoa


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

    ultimos = Lancamento.objects.select_related("categoria", "pessoa").all()[:20]

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


def _parse_month_param(value: str | None) -> date | None:
    if not value:
        return None
    try:
        year_text, month_text = value.split("-")
        year = int(year_text)
        month = int(month_text)
        if 1 <= month <= 12:
            return date(year, month, 1)
    except (ValueError, TypeError):
        return None
    return None


def _month_end(day: date) -> date:
    if day.month == 12:
        next_month = date(day.year + 1, 1, 1)
    else:
        next_month = date(day.year, day.month + 1, 1)
    return next_month - timedelta(days=1)


def dashboard_view(request):
    if not request.session.get("pin_ok"):
        return _pin_redirect(request)

    month_param = request.GET.get("mes")
    month_start = _parse_month_param(month_param)
    if month_start:
        end_date = _month_end(month_start)
    else:
        end_date = timezone.localdate()
    start_date = end_date - timedelta(days=29)

    qs = Lancamento.objects.filter(data__range=(start_date, end_date))

    total_output_field = DecimalField(max_digits=12, decimal_places=2)
    total_entradas = (
        qs.filter(tipo=Lancamento.Tipo.ENTRADA).aggregate(
            total=Coalesce(
                Sum("valor"),
                Value(0, output_field=total_output_field),
                output_field=total_output_field,
            )
        )["total"]
    )
    total_saidas = (
        qs.filter(tipo=Lancamento.Tipo.SAIDA).aggregate(
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

    days = [start_date + timedelta(days=offset) for offset in range(30)]
    entradas_por_dia = {day: Decimal("0.00") for day in days}
    saidas_por_dia = {day: Decimal("0.00") for day in days}

    for row in qs.values("data", "tipo").annotate(total=Sum("valor")).order_by("data"):
        day = row["data"]
        if day not in entradas_por_dia:
            continue
        if row["tipo"] == Lancamento.Tipo.ENTRADA:
            entradas_por_dia[day] = row["total"] or Decimal("0.00")
        else:
            saidas_por_dia[day] = row["total"] or Decimal("0.00")

    labels = [day.strftime("%d/%m") for day in days]
    entradas_series = [float(entradas_por_dia[day]) for day in days]
    saidas_series = [float(saidas_por_dia[day]) for day in days]
    saldo_series = [float(entradas_por_dia[day] - saidas_por_dia[day]) for day in days]

    month_options = []
    cursor = date(end_date.year, end_date.month, 1)
    for _ in range(12):
        month_options.append(
            {
                "value": cursor.strftime("%Y-%m"),
                "label": cursor.strftime("%m/%Y"),
            }
        )
        cursor = (cursor - timedelta(days=1)).replace(day=1)

    selected_month = month_start.strftime("%Y-%m") if month_start else ""

    return render(
        request,
        "financas/dashboard.html",
        {
            "total_entradas": total_entradas,
            "total_saidas": total_saidas,
            "saldo": saldo,
            "labels_json": json.dumps(labels),
            "entradas_json": json.dumps(entradas_series),
            "saidas_json": json.dumps(saidas_series),
            "saldo_json": json.dumps(saldo_series),
            "start_date": start_date,
            "end_date": end_date,
            "month_options": month_options,
            "selected_month": selected_month,
        },
    )


def historico_view(request):
    if not request.session.get("pin_ok"):
        return _pin_redirect(request)

    qs = Lancamento.objects.select_related("categoria", "pessoa").all()
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


def administrativo_view(request):
    if not request.session.get("pin_ok"):
        return _pin_redirect(request)

    categoria_form = CategoriaForm(prefix="categoria")
    pessoa_form = PessoaForm(prefix="pessoa")
    if request.method == "POST":
        form_type = request.POST.get("form_type") or "categoria"
        if form_type == "pessoa":
            pessoa_form = PessoaForm(request.POST, prefix="pessoa")
            if pessoa_form.is_valid():
                pessoa_form.save()
                messages.success(request, "Pessoa cadastrada com sucesso.")
                return redirect("financas:administrativo")
        else:
            categoria_form = CategoriaForm(request.POST, prefix="categoria")
            if categoria_form.is_valid():
                categoria_form.save()
                messages.success(request, "Categoria cadastrada com sucesso.")
                return redirect("financas:administrativo")

    categorias = Categoria.objects.all()
    pessoas = Pessoa.objects.all()

    return render(
        request,
        "financas/administrativo.html",
        {
            "categoria_form": categoria_form,
            "pessoa_form": pessoa_form,
            "categorias": categorias,
            "pessoas": pessoas,
        },
    )


@require_POST
def excluir_categoria_view(request, pk: int):
    if not request.session.get("pin_ok"):
        return _pin_redirect(request)

    categoria = get_object_or_404(Categoria, pk=pk)
    try:
        categoria.delete()
        messages.success(request, "Categoria excluída com sucesso.")
    except ProtectedError:
        messages.error(
            request, "Não foi possível excluir: existe lançamento associado a esta categoria."
        )
    return redirect("financas:administrativo")


@require_POST
def excluir_pessoa_view(request, pk: int):
    if not request.session.get("pin_ok"):
        return _pin_redirect(request)

    pessoa = get_object_or_404(Pessoa, pk=pk)
    try:
        pessoa.delete()
        messages.success(request, "Pessoa excluída com sucesso.")
    except ProtectedError:
        messages.error(
            request, "Não foi possível excluir: existe lançamento associado a esta pessoa."
        )
    return redirect("financas:administrativo")


@require_POST
def excluir_lancamento_view(request, pk: int):
    next_url = request.POST.get("next") or ""
    if not request.session.get("pin_ok"):
        redirect_to = next_url
        if not (
            redirect_to
            and url_has_allowed_host_and_scheme(
                redirect_to,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            )
        ):
            redirect_to = reverse("financas:historico")
        url = reverse("financas:senha")
        return redirect(f"{url}?{urlencode({'next': redirect_to})}")

    form = PinForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Senha incorreta. Transação não excluída.")
        if next_url and url_has_allowed_host_and_scheme(
            next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
        ):
            return redirect(next_url)
        return redirect("financas:historico")

    lancamento = get_object_or_404(Lancamento, pk=pk)
    lancamento.delete()
    messages.success(request, "Transação excluída com sucesso.")

    if next_url and url_has_allowed_host_and_scheme(
        next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return redirect(next_url)
    return redirect("financas:historico")


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
