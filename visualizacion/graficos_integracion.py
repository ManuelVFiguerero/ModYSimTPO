"""Graficos reutilizables para integracion numerica."""

from __future__ import annotations

import plotly.graph_objects as go

from core.utils.parser_funciones import expression_to_callable


def grafico_integrando(expr: str, a: float, b: float, angle_mode: str | None = None) -> go.Figure:
    f = expression_to_callable(expr, ("x",), angle_mode=angle_mode)
    xs = [a + (b - a) * i / 300 for i in range(301)]
    ys = [f(x) for x in xs]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", name="f(x)"))
    fig.add_hline(y=0, line_dash="dash")
    fig.update_layout(title="Integrando en el intervalo", xaxis_title="x", yaxis_title="f(x)")
    return fig
