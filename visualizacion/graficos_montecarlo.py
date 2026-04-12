"""Graficos reutilizables para Monte Carlo."""

from __future__ import annotations

import plotly.graph_objects as go

from core.utils.resultados import MonteCarloResult


def histograma_montecarlo(resultado: MonteCarloResult) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=[p.aporte for p in resultado.puntos], nbinsx=40, name="Aportes"))
    fig.add_vline(x=resultado.estimacion, line_dash="dash", line_color="green")
    fig.update_layout(title="Distribucion de aportes Monte Carlo", xaxis_title="Aporte", yaxis_title="Frecuencia")
    return fig
