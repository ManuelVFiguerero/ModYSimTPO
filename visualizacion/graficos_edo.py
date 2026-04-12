"""Graficos reutilizables para metodos de EDO."""

from __future__ import annotations

import plotly.graph_objects as go

from core.utils.resultados import ODEResult


def grafico_trayectoria_edo(resultado: ODEResult) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[p.t for p in resultado.pasos], y=[p.y for p in resultado.pasos], mode="lines+markers", name="Aproximacion"))
    if any(p.y_exacto is not None for p in resultado.pasos):
        fig.add_trace(go.Scatter(x=[p.t for p in resultado.pasos], y=[p.y_exacto for p in resultado.pasos], mode="lines", name="Solucion exacta"))
    fig.update_layout(title=f"Trayectoria - {resultado.metodo}", xaxis_title="t", yaxis_title="y")
    return fig
