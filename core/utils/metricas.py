"""Metricas y utilidades numericas compartidas."""

from __future__ import annotations

from typing import Optional


def error_absoluto(actual: float, referencia: float) -> float:
    """Calcula el error absoluto entre dos valores."""
    return abs(actual - referencia)


def error_relativo(actual: float, referencia: float) -> Optional[float]:
    """Calcula el error relativo si la referencia es no nula."""
    if referencia == 0:
        return None
    return abs(actual - referencia) / abs(referencia)


def error_relativo_aproximado(actual: float, anterior: float) -> Optional[float]:
    """Calcula el error relativo aproximado entre iteraciones."""
    if actual == 0:
        return None
    return abs(actual - anterior) / abs(actual)
