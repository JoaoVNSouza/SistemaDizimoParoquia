from datetime import date
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from dizimo.models import Dizimo
from fieis.models import Fiel


def _grafico_arrecadacao_mensal(ano):
    """Gráfico de barras com total arrecadado por mês no ano informado."""
    dados = (
        Dizimo.objects.filter(pago=True, referencia__year=ano)
        .annotate(mes=TruncMonth("referencia"))
        .values("mes")
        .annotate(total=Sum("valor"))
        .order_by("mes")
    )

    meses_map = {d["mes"].month: float(d["total"] or 0) for d in dados}
    labels = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
              "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    valores = [meses_map.get(i, 0.0) for i in range(1, 13)]

    try:
        import plotly.graph_objects as go
        fig = go.Figure(data=[go.Bar(
            x=labels, y=valores,
            marker_color="#0d6efd",
            text=[f"R$ {v:,.2f}" for v in valores],
            textposition="auto",
        )])
        fig.update_layout(
            title=f"Arrecadação mensal — {ano}",
            xaxis_title="Mês",
            yaxis_title="Total (R$)",
            template="plotly_white",
            height=400,
            margin=dict(l=40, r=20, t=60, b=40),
            autosize=True,
        )
        return fig.to_html(
            full_html=False,
            include_plotlyjs="cdn",
            config={"responsive": True, "displayModeBar": False},
            default_width="100%",
        )
    except ImportError:
        # Fallback caso plotly não esteja instalado
        linhas = "".join(
            f"<tr><td>{l}</td><td class='text-end'>R$ {v:,.2f}</td></tr>"
            for l, v in zip(labels, valores)
        )
        return (
            "<table class='table table-sm'><thead><tr><th>Mês</th>"
            "<th class='text-end'>Total</th></tr></thead><tbody>"
            f"{linhas}</tbody></table>"
        )


@login_required
def index(request):
    hoje = timezone.now().date()

    total_mes = (
        Dizimo.objects.filter(
            pago=True,
            data_pagamento__year=hoje.year,
            data_pagamento__month=hoje.month,
        ).aggregate(total=Sum("valor"))["total"]
        or Decimal("0")
    )

    total_ano = (
        Dizimo.objects.filter(pago=True, data_pagamento__year=hoje.year)
        .aggregate(total=Sum("valor"))["total"]
        or Decimal("0")
    )

    qtd_fieis_ativos = Fiel.objects.filter(ativo=True).count()

    # Inadimplentes: fiéis ativos sem dízimo pago referente ao mês atual
    fieis_com_pagamento_mes = Dizimo.objects.filter(
        pago=True,
        referencia__year=hoje.year,
        referencia__month=hoje.month,
    ).values_list("fiel_id", flat=True)

    inadimplentes = Fiel.objects.filter(ativo=True).exclude(
        id__in=fieis_com_pagamento_mes
    )

    ultimos_pagamentos = (
        Dizimo.objects.select_related("fiel")
        .order_by("-data_pagamento", "-criado_em")[:10]
    )

    grafico_html = _grafico_arrecadacao_mensal(hoje.year)

    contexto = {
        "hoje": hoje,
        "total_mes": total_mes,
        "total_ano": total_ano,
        "qtd_fieis_ativos": qtd_fieis_ativos,
        "qtd_inadimplentes": inadimplentes.count(),
        "inadimplentes": inadimplentes[:10],
        "ultimos_pagamentos": ultimos_pagamentos,
        "grafico_html": grafico_html,
    }
    return render(request, "dashboard/index.html", contexto)


@login_required
def historico_fiel(request, pk):
    fiel = get_object_or_404(Fiel, pk=pk)
    pagamentos = fiel.dizimos.all().order_by("-data_pagamento")
    total = pagamentos.aggregate(total=Sum("valor"))["total"] or Decimal("0")
    return render(request, "dashboard/historico.html", {
        "fiel": fiel,
        "pagamentos": pagamentos,
        "total": total,
    })


@login_required
def relatorio(request):
    ano = int(request.GET.get("ano") or date.today().year)
    mes = request.GET.get("mes")

    qs = Dizimo.objects.select_related("fiel").filter(pago=True, referencia__year=ano)
    if mes:
        qs = qs.filter(referencia__month=int(mes))

    total = qs.aggregate(total=Sum("valor"))["total"] or Decimal("0")

    return render(request, "dashboard/relatorio.html", {
        "pagamentos": qs.order_by("-data_pagamento"),
        "ano": ano,
        "mes": mes,
        "total": total,
        "meses": [(i, f"{i:02d}") for i in range(1, 13)],
    })
