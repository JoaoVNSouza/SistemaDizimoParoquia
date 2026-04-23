from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import FielForm
from .models import Fiel


@login_required
def listar(request):
    busca = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()

    qs = Fiel.objects.all()
    if busca:
        qs = qs.filter(Q(nome__icontains=busca) | Q(cpf__icontains=busca))
    if status == "ativo":
        qs = qs.filter(ativo=True)
    elif status == "inativo":
        qs = qs.filter(ativo=False)

    paginator = Paginator(qs, 15)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "fieis/listar.html", {
        "page_obj": page_obj,
        "busca": busca,
        "status": status,
    })


@login_required
def cadastrar(request):
    form = FielForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Fiel cadastrado com sucesso.")
        return redirect("fieis:listar")

    return render(request, "fieis/form.html", {"form": form, "titulo": "Cadastrar Fiel"})


@login_required
def editar(request, pk):
    fiel = get_object_or_404(Fiel, pk=pk)
    form = FielForm(request.POST or None, instance=fiel)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Fiel atualizado com sucesso.")
        return redirect("fieis:detalhar", pk=fiel.pk)

    return render(request, "fieis/form.html", {
        "form": form,
        "titulo": f"Editar Fiel — {fiel.nome}",
        "fiel": fiel,
    })


@login_required
def detalhar(request, pk):
    fiel = get_object_or_404(Fiel, pk=pk)
    pagamentos = fiel.dizimos.all().order_by("-data_pagamento")
    total = pagamentos.aggregate(total=Sum("valor"))["total"] or 0
    return render(request, "fieis/detalhar.html", {
        "fiel": fiel,
        "pagamentos": pagamentos,
        "total": total,
    })


@login_required
def excluir(request, pk):
    fiel = get_object_or_404(Fiel, pk=pk)
    qtd_pagamentos = fiel.dizimos.count()
    tem_pagamentos = qtd_pagamentos > 0

    if request.method == "POST":
        if tem_pagamentos:
            messages.error(
                request,
                "Não é possível excluir este fiel pois há pagamentos vinculados. "
                "Você pode marcá-lo como inativo.",
            )
            return redirect("fieis:excluir", pk=fiel.pk)

        fiel.delete()
        messages.success(request, "Fiel excluído com sucesso.")
        return redirect("fieis:listar")

    return render(request, "fieis/excluir.html", {
        "fiel": fiel,
        "qtd_pagamentos": qtd_pagamentos,
        "tem_pagamentos": tem_pagamentos,
    })


@login_required
@require_POST
def inativar(request, pk):
    fiel = get_object_or_404(Fiel, pk=pk)
    fiel.ativo = False
    fiel.save(update_fields=["ativo"])
    messages.success(request, f"Fiel '{fiel.nome}' marcado como inativo.")
    return redirect("fieis:listar")
