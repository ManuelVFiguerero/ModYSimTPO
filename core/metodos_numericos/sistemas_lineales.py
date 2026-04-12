"""Resolucion de sistemas lineales."""

from __future__ import annotations

from core.utils.resultados import LinearSystemResult
from core.utils.validaciones import validar_dimension_sistema


def eliminacion_gauss(matriz: list[list[float]], vector: list[float]) -> LinearSystemResult:
    """Resuelve Ax=b mediante eliminacion gaussiana con pivoteo parcial."""
    validar_dimension_sistema(matriz, vector)
    n = len(matriz)
    a = [fila[:] for fila in matriz]
    b = vector[:]

    for k in range(n):
        pivote = max(range(k, n), key=lambda i: abs(a[i][k]))
        if abs(a[pivote][k]) < 1e-14:
            raise ValueError("El sistema es singular o casi singular.")
        if pivote != k:
            a[k], a[pivote] = a[pivote], a[k]
            b[k], b[pivote] = b[pivote], b[k]
        for i in range(k + 1, n):
            factor = a[i][k] / a[k][k]
            for j in range(k, n):
                a[i][j] -= factor * a[k][j]
            b[i] -= factor * b[k]

    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        suma = sum(a[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (b[i] - suma) / a[i][i]

    residuo = []
    for fila, termino in zip(matriz, vector):
        residuo.append(sum(coef * xi for coef, xi in zip(fila, x)) - termino)

    return LinearSystemResult("eliminacion_gauss", x, residuo, "Sistema resuelto.", {"dimension": n})
