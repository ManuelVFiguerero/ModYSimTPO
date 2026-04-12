"""Metodos de integracion numerica deterministica."""

from __future__ import annotations

from core.utils.metricas import error_absoluto, error_relativo
from core.utils.parser_funciones import expression_to_callable
from core.utils.resultados import IntegrationResult, IntegrationSample
from core.utils.validaciones import validar_intervalo, validar_subintervalos

_GAUSS_LEGENDRE_TABLA: dict[int, tuple[tuple[float, float], ...]] = {
    2: ((-0.5773502691896257, 1.0), (0.5773502691896257, 1.0)),
    3: ((-0.7745966692414834, 0.5555555555555556), (0.0, 0.8888888888888888), (0.7745966692414834, 0.5555555555555556)),
    4: ((-0.8611363115940526, 0.34785484513745385), (-0.33998104358485626, 0.6521451548625461), (0.33998104358485626, 0.6521451548625461), (0.8611363115940526, 0.34785484513745385)),
    5: ((-0.906179845938664, 0.23692688505618908), (-0.5384693101056831, 0.47862867049936647), (0.0, 0.5688888888888889), (0.5384693101056831, 0.47862867049936647), (0.906179845938664, 0.23692688505618908)),
}


def _build_result(
    metodo: str,
    valor: float,
    muestras: list[IntegrationSample],
    valor_exacto: float | None = None,
    metadatos: dict | None = None,
) -> IntegrationResult:
    err_abs = error_absoluto(valor, valor_exacto) if valor_exacto is not None else None
    err_rel = error_relativo(valor, valor_exacto) if valor_exacto is not None else None
    return IntegrationResult(
        metodo=metodo,
        valor_aproximado=valor,
        valor_exacto=valor_exacto,
        error_absoluto=err_abs,
        error_relativo=err_rel,
        muestras=muestras,
        mensaje="Integracion completada.",
        metadatos=metadatos or {},
    )


def trapecio_compuesto(f_expr: str, a: float, b: float, n: int, valor_exacto: float | None = None, angle_mode: str | None = None) -> IntegrationResult:
    validar_intervalo(a, b)
    validar_subintervalos(n, 1)
    f = expression_to_callable(f_expr, ("x",), angle_mode=angle_mode)
    h = (b - a) / n
    muestras: list[IntegrationSample] = []
    suma = 0.0
    for i in range(n + 1):
        x_i = a + i * h
        peso = 0.5 if i in (0, n) else 1.0
        fx = f(x_i)
        aporte = peso * fx
        suma += aporte
        muestras.append(IntegrationSample(i, x_i, fx, peso, aporte))
    return _build_result("trapecio_compuesto", h * suma, muestras, valor_exacto, {"n": n, "h": h})


def simpson_13_compuesto(f_expr: str, a: float, b: float, n: int, valor_exacto: float | None = None, angle_mode: str | None = None) -> IntegrationResult:
    validar_intervalo(a, b)
    if n < 2 or n % 2 != 0:
        raise ValueError("Para Simpson 1/3, n debe ser par y mayor o igual a 2.")
    f = expression_to_callable(f_expr, ("x",), angle_mode=angle_mode)
    h = (b - a) / n
    muestras: list[IntegrationSample] = []
    suma = 0.0
    for i in range(n + 1):
        x_i = a + i * h
        if i in (0, n):
            peso = 1.0
        else:
            peso = 4.0 if i % 2 == 1 else 2.0
        fx = f(x_i)
        aporte = peso * fx
        suma += aporte
        muestras.append(IntegrationSample(i, x_i, fx, peso, aporte))
    return _build_result("simpson_13_compuesto", (h / 3.0) * suma, muestras, valor_exacto, {"n": n, "h": h})


def simpson_38_compuesto(f_expr: str, a: float, b: float, n: int, valor_exacto: float | None = None, angle_mode: str | None = None) -> IntegrationResult:
    validar_intervalo(a, b)
    if n < 3 or n % 3 != 0:
        raise ValueError("Para Simpson 3/8, n debe ser multiplo de 3 y mayor o igual a 3.")
    f = expression_to_callable(f_expr, ("x",), angle_mode=angle_mode)
    h = (b - a) / n
    muestras: list[IntegrationSample] = []
    suma = 0.0
    for i in range(n + 1):
        x_i = a + i * h
        if i in (0, n):
            peso = 1.0
        else:
            peso = 2.0 if i % 3 == 0 else 3.0
        fx = f(x_i)
        aporte = peso * fx
        suma += aporte
        muestras.append(IntegrationSample(i, x_i, fx, peso, aporte))
    return _build_result("simpson_38_compuesto", (3.0 * h / 8.0) * suma, muestras, valor_exacto, {"n": n, "h": h})


def rectangulo_medio_compuesto(f_expr: str, a: float, b: float, n: int, valor_exacto: float | None = None, angle_mode: str | None = None) -> IntegrationResult:
    validar_intervalo(a, b)
    validar_subintervalos(n, 1)
    f = expression_to_callable(f_expr, ("x",), angle_mode=angle_mode)
    h = (b - a) / n
    muestras: list[IntegrationSample] = []
    suma = 0.0
    for i in range(n):
        x_i = a + (i + 0.5) * h
        fx = f(x_i)
        aporte = fx
        suma += aporte
        muestras.append(IntegrationSample(i, x_i, fx, 1.0, aporte))
    return _build_result("rectangulo_medio_compuesto", h * suma, muestras, valor_exacto, {"n": n, "h": h})


def cuadratura_gauss_legendre(f_expr: str, a: float, b: float, orden: int = 3, valor_exacto: float | None = None, angle_mode: str | None = None) -> IntegrationResult:
    validar_intervalo(a, b)
    if orden not in _GAUSS_LEGENDRE_TABLA:
        raise ValueError("Orden no soportado. Usa 2, 3, 4 o 5.")
    f = expression_to_callable(f_expr, ("x",), angle_mode=angle_mode)
    c1 = (b - a) / 2.0
    c2 = (a + b) / 2.0
    suma = 0.0
    muestras: list[IntegrationSample] = []
    for indice, (xi, wi) in enumerate(_GAUSS_LEGENDRE_TABLA[orden], start=1):
        x_real = c1 * xi + c2
        fx = f(x_real)
        aporte = wi * fx
        suma += aporte
        muestras.append(IntegrationSample(indice, x_real, fx, wi, aporte))
    return _build_result("gauss_legendre", c1 * suma, muestras, valor_exacto, {"orden": orden})
