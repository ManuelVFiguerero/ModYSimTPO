"""Graficos reutilizables para interpolacion."""

from __future__ import annotations

import plotly.graph_objects as go

from core.metodos_numericos.interpolacion import interpolacion_lagrange


def grafico_lagrange(puntos: list[tuple[float, float]], x_eval: float) -> go.Figure:
    xs_datos = [p[0] for p in puntos]
    x_min, x_max = min(xs_datos), max(xs_datos)
    margen = (x_max - x_min) * 0.2 if x_max > x_min else 1.0
    xs = [x_min - margen + (x_max - x_min + 2 * margen) * i / 200 for i in range(201)]
    ys = [interpolacion_lagrange(puntos, x).valor_interpolado for x in xs]
    valor = interpolacion_lagrange(puntos, x_eval).valor_interpolado

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", name="Polinomio interpolante"))
    fig.add_trace(go.Scatter(x=xs_datos, y=[p[1] for p in puntos], mode="markers", name="Nodos"))
    fig.add_trace(go.Scatter(x=[x_eval], y=[valor], mode="markers", name="Evaluacion"))
    fig.update_layout(title="Interpolacion de Lagrange", xaxis_title="x", yaxis_title="y")
    return fig
