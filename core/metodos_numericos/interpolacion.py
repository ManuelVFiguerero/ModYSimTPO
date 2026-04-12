"""Metodos de interpolacion y derivacion numerica."""

from __future__ import annotations

from core.utils.parser_funciones import expression_to_callable, interpolate_polynomial_expression
from core.utils.resultados import InterpolationResult
from core.utils.validaciones import validar_puntos_interpolacion


def interpolacion_lagrange(
    puntos: list[tuple[float, float]],
    x_eval: float,
) -> InterpolationResult:
    """Evalua el polinomio interpolante de Lagrange."""
    validar_puntos_interpolacion(puntos)

    resultado = 0.0
    n = len(puntos)
    for i in range(n):
        xi, yi = puntos[i]
        termino = yi
        for j in range(n):
            if i == j:
                continue
            xj, _ = puntos[j]
            termino *= (x_eval - xj) / (xi - xj)
        resultado += termino

    return InterpolationResult(
        metodo="lagrange",
        valor_interpolado=resultado,
        x_eval=x_eval,
        puntos=list(puntos),
        mensaje="Interpolacion completada.",
        metadatos={"polinomio": interpolate_polynomial_expression(puntos)},
    )


def diferencia_central(
    f_expr: str,
    x: float,
    h: float = 1e-4,
    angle_mode: str | None = None,
) -> float:
    """Aproxima la derivada primera mediante diferencia central."""
    if h <= 0:
        raise ValueError("h debe ser mayor a cero.")
    f = expression_to_callable(f_expr, ("x",), angle_mode=angle_mode)
    return (f(x + h) - f(x - h)) / (2.0 * h)
