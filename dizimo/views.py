from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404

from fieis.models import Fiel

from .forms import DizimoForm
from .models import Dizimo


@login_required
def listar(request):
    qs = Dizimo.objects.select_related("fiel").all()

    fiel_id = request.GET.get("fiel")
    mes = request.GET.get("mes")
    ano = request.GET.get("ano")
    status = request.GET.get("status")

    if fiel_id:
        qs = qs.filter(fiel_id=fiel_id)
    if mes:
        qs = qs.filter(referencia__month=mes)
    if ano:
        qs = qs.filter(referencia__year=ano)
    if status == "pago":
        qs = qs.filter(pago=True)
    elif status == "pendente":
        qs = qs.filter(pago=False)

    total = qs.aggregate(total=Sum("valor"))["total"] or 0

    paginator = Paginator(qs, 20)
    page_obj = paginator.get_page(request.GET.get("page"))

    contexto = {
        "page_obj": page_obj,
        "fieis": Fiel.objects.filter(ativo=True),
        "total": total,
        "filtros": {
            "fiel": fiel_id or "",
            "mes": mes or "",
            "ano": ano or "",
            "status": status or "",
        },
        "meses": [(i, f"{i:02d}") for i in range(1, 13)],
    }
    return render(request, "dizimo/listar.html", contexto)


@login_required
def registrar(request):
    form = DizimoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pagamento registrado com sucesso.")
        return redirect("dizimo:listar")
    return render(request, "dizimo/form.html", {"form": form, "titulo": "Registrar Dízimo"})


@login_required
def editar(request, pk):
    dizimo = get_object_or_404(Dizimo, pk=pk)
    form = DizimoForm(request.POST or None, instance=dizimo)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pagamento atualizado com sucesso.")
        return redirect("dizimo:listar")
    return render(request, "dizimo/form.html", {
        "form": form,
        "titulo": "Editar Dízimo",
        "dizimo": dizimo,
    })


@login_required
def excluir(request, pk):
    dizimo = get_object_or_404(Dizimo, pk=pk)
    if request.method == "POST":
        dizimo.delete()
        messages.success(request, "Pagamento excluído com sucesso.")
        return redirect("dizimo:listar")
    return render(request, "dizimo/excluir.html", {"dizimo": dizimo})


@login_required
def comprovante(request, pk):
    dizimo = get_object_or_404(Dizimo.objects.select_related("fiel"), pk=pk)
    return render(request, "dizimo/comprovante.html", {"dizimo": dizimo})


@login_required
def marcar_pago(request, pk):
    dizimo = get_object_or_404(Dizimo, pk=pk)
    if request.method == "POST":
        dizimo.pago = not dizimo.pago
        dizimo.save(update_fields=["pago"])
        estado = "pago" if dizimo.pago else "pendente"
        messages.success(request, f"Dízimo marcado como {estado}.")
    return redirect("dizimo:listar")
