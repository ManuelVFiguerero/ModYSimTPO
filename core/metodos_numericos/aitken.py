"""Aceleracion de convergencia por Aitken."""

from __future__ import annotations

from core.utils.metricas import error_absoluto, error_relativo_aproximado
from core.utils.parser_funciones import expression_to_callable
from core.utils.resultados import RootIteration, SequenceAccelerationResult
from core.utils.validaciones import validar_max_iter, validar_tolerancia


def aitken_delta_cuadrado(secuencia: list[float]) -> float:
    """Aplica delta-cuadrado de Aitken usando los ultimos tres terminos."""
    if len(secuencia) < 3:
        raise ValueError("Se requieren al menos tres terminos consecutivos.")
    x0, x1, x2 = secuencia[-3:]
    denominador = x2 - 2.0 * x1 + x0
    if abs(denominador) < 1e-14:
        raise ValueError("No se puede aplicar Aitken: denominador cercano a cero.")
    return x0 - ((x1 - x0) ** 2) / denominador


def aitken_desde_punto_fijo(g_expr: str, x0: float, tolerancia: float = 1e-6, max_iter: int = 100, angle_mode: str | None = None) -> SequenceAccelerationResult:
    """Acelera una iteracion de punto fijo mediante Aitken."""
    validar_tolerancia(tolerancia)
    validar_max_iter(max_iter)
    g = expression_to_callable(g_expr, ("x",), angle_mode=angle_mode)

    iteraciones: list[RootIteration] = []
    xn = x0
    anterior = None
    for iteracion in range(1, max_iter + 1):
        xn1 = g(xn)
        xn2 = g(xn1)
        denominador = xn2 - 2.0 * xn1 + xn
        if abs(denominador) < 1e-14:
            raise ValueError("No se puede aplicar Aitken: denominador cercano a cero.")
        x_hat = xn - ((xn1 - xn) ** 2) / denominador
        base_error = error_absoluto(x_hat, anterior) if anterior is not None else error_absoluto(x_hat, xn)
        iteraciones.append(
            RootIteration(
                iteracion=iteracion,
                aproximacion=x_hat,
                error_absoluto=base_error,
                error_relativo=error_relativo_aproximado(x_hat, anterior if anterior is not None else xn),
                detalles={"xn": xn, "xn1": xn1, "xn2": xn2},
            )
        )
        if anterior is not None and base_error < tolerancia:
            return SequenceAccelerationResult("aitken", True, x_hat, iteraciones, "Metodo convergente.", {"tolerancia": tolerancia})
        anterior = x_hat
        xn = xn1

    return SequenceAccelerationResult("aitken", False, anterior if anterior is not None else x0, iteraciones, "Se alcanzo el maximo de iteraciones.", {"tolerancia": tolerancia})
