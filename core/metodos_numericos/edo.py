"""Metodos numericos para ecuaciones diferenciales ordinarias."""

from __future__ import annotations

from core.utils.metricas import error_absoluto
from core.utils.parser_funciones import expression_to_callable
from core.utils.resultados import ODEResult, ODEStep
from core.utils.validaciones import validar_max_iter, validar_paso


def _resolver_edo(
    ode_expr: str,
    h: float,
    pasos: int,
    solucion_exacta_expr: str | None,
    angle_mode: str | None,
):
    validar_paso(h)
    validar_max_iter(pasos)
    f = expression_to_callable(ode_expr, ("t", "y"), angle_mode=angle_mode)
    exacta = expression_to_callable(solucion_exacta_expr, ("t",), angle_mode=angle_mode) if solucion_exacta_expr else None
    return f, exacta


def euler(ode_expr: str, t0: float, y0: float, h: float, pasos: int, solucion_exacta_expr: str | None = None, angle_mode: str | None = None) -> ODEResult:
    """Resuelve un PVI por Euler explicito."""
    f, exacta = _resolver_edo(ode_expr, h, pasos, solucion_exacta_expr, angle_mode)
    t = t0
    y = y0
    y_exacto = exacta(t) if exacta else None
    tabla = [ODEStep(0, t, y, y_exacto, error_absoluto(y, y_exacto) if y_exacto is not None else None)]
    for paso in range(1, pasos + 1):
        y = y + h * f(t, y)
        t = t + h
        y_exacto = exacta(t) if exacta else None
        tabla.append(ODEStep(paso, t, y, y_exacto, error_absoluto(y, y_exacto) if y_exacto is not None else None))
    return ODEResult("euler", tabla, "Integracion completada.", {"h": h, "pasos": pasos})


def heun(ode_expr: str, t0: float, y0: float, h: float, pasos: int, solucion_exacta_expr: str | None = None, angle_mode: str | None = None) -> ODEResult:
    """Resuelve un PVI por el metodo de Heun."""
    f, exacta = _resolver_edo(ode_expr, h, pasos, solucion_exacta_expr, angle_mode)
    t = t0
    y = y0
    y_exacto = exacta(t) if exacta else None
    tabla = [ODEStep(0, t, y, y_exacto, error_absoluto(y, y_exacto) if y_exacto is not None else None)]
    for paso in range(1, pasos + 1):
        predictor = y + h * f(t, y)
        y = y + h * (f(t, y) + f(t + h, predictor)) / 2.0
        t = t + h
        y_exacto = exacta(t) if exacta else None
        tabla.append(ODEStep(paso, t, y, y_exacto, error_absoluto(y, y_exacto) if y_exacto is not None else None))
    return ODEResult("heun", tabla, "Integracion completada.", {"h": h, "pasos": pasos})


def runge_kutta_4(ode_expr: str, t0: float, y0: float, h: float, pasos: int, solucion_exacta_expr: str | None = None, angle_mode: str | None = None) -> ODEResult:
    """Resuelve un PVI por RK4 clasico."""
    f, exacta = _resolver_edo(ode_expr, h, pasos, solucion_exacta_expr, angle_mode)
    t = t0
    y = y0
    y_exacto = exacta(t) if exacta else None
    tabla = [ODEStep(0, t, y, y_exacto, error_absoluto(y, y_exacto) if y_exacto is not None else None)]
    for paso in range(1, pasos + 1):
        k1 = f(t, y)
        k2 = f(t + h / 2.0, y + h * k1 / 2.0)
        k3 = f(t + h / 2.0, y + h * k2 / 2.0)
        k4 = f(t + h, y + h * k3)
        y = y + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
        t = t + h
        y_exacto = exacta(t) if exacta else None
        tabla.append(ODEStep(paso, t, y, y_exacto, error_absoluto(y, y_exacto) if y_exacto is not None else None))
    return ODEResult("runge_kutta_4", tabla, "Integracion completada.", {"h": h, "pasos": pasos})
