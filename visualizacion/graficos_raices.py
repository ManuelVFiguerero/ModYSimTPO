"""Graficos reutilizables para metodos de raices."""

from __future__ import annotations

import plotly.graph_objects as go

from core.utils.parser_funciones import expression_to_callable
from core.utils.resultados import RootResult


def grafico_convergencia_raices(resultado: RootResult) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=[paso.iteracion for paso in resultado.iteraciones],
            y=[paso.error_absoluto for paso in resultado.iteraciones],
            mode="lines+markers",
            name="Error absoluto",
        )
    )
    fig.update_layout(title=f"Convergencia - {resultado.metodo}", xaxis_title="Iteracion", yaxis_title="Error absoluto")
    return fig


def grafico_funcion_raiz(expr: str, aproximacion: float, xmin: float, xmax: float, angle_mode: str | None = None) -> go.Figure:
    f = expression_to_callable(expr, ("x",), angle_mode=angle_mode)
    xs = [xmin + (xmax - xmin) * i / 300 for i in range(301)]
    ys = [f(x) for x in xs]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", name="f(x)"))
    fig.add_hline(y=0, line_dash="dash")
    fig.add_vline(x=aproximacion, line_dash="dot")
    fig.update_layout(title="Funcion y raiz aproximada", xaxis_title="x", yaxis_title="f(x)")
    return fig
