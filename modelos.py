"""Fachada de compatibilidad sobre el nuevo nucleo modular."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import NormalDist
from typing import List, Sequence, Tuple

from core.metodos_numericos.aitken import aitken_delta_cuadrado as _aitken_delta_cuadrado
from core.metodos_numericos.aitken import aitken_desde_punto_fijo as _aitken_desde_punto_fijo
from core.metodos_numericos.edo import runge_kutta_4 as _runge_kutta_4
from core.metodos_numericos.integracion import (
    cuadratura_gauss_legendre as _cuadratura_gauss_legendre,
    rectangulo_medio_compuesto as _rectangulo_medio_compuesto,
    simpson_13_compuesto as _simpson_13_compuesto,
    simpson_38_compuesto as _simpson_38_compuesto,
    trapecio_compuesto as _trapecio_compuesto,
)
from core.metodos_numericos.interpolacion import (
    diferencia_central as _diferencia_central,
    interpolacion_lagrange as _interpolacion_lagrange,
)
from core.metodos_numericos.monte_carlo import integracion_montecarlo as _integracion_montecarlo
from core.metodos_numericos.raices import (
    biseccion as _biseccion,
    newton_raphson as _newton_raphson,
    punto_fijo as _punto_fijo,
)
from core.utils.parser_funciones import evaluate_expression

_ANGULAR_MODE = "radianes"


@dataclass
class FixedPointStep:
    iteracion: int
    x_anterior: float
    x_actual: float
    error: float


@dataclass
class FixedPointResult:
    convergio: bool
    aproximacion: float
    pasos: List[FixedPointStep]


@dataclass
class BisectionStep:
    iteracion: int
    a: float
    b: float
    c: float
    fc: float
    error_intervalo: float


@dataclass
class BisectionResult:
    convergio: bool
    aproximacion: float
    pasos: List[BisectionStep]


@dataclass
class NewtonStep:
    iteracion: int
    x_anterior: float
    x_actual: float
    error: float
    fx_actual: float


@dataclass
class NewtonResult:
    convergio: bool
    aproximacion: float
    pasos: List[NewtonStep]


@dataclass
class RK4Step:
    paso: int
    t: float
    y: float


@dataclass
class AitkenStep:
    iteracion: int
    xn: float
    xn1: float
    xn2: float
    x_aitken: float
    error: float


@dataclass
class AitkenResult:
    convergio: bool
    aproximacion: float
    pasos: List[AitkenStep]


@dataclass
class MonteCarloResult:
    estimacion: float
    desvio_muestral: float
    error_estandar: float
    ic_bajo: float
    ic_alto: float
    confianza: float
    n: int
    muestras_transformadas: List[float] | None = None


def set_angular_mode(mode: str) -> None:
    global _ANGULAR_MODE
    _ANGULAR_MODE = mode


def get_angular_mode() -> str:
    return _ANGULAR_MODE


def evaluar_expresion(expr: str, angle_mode: str | None = None, **variables: float) -> float:
    return evaluate_expression(expr, variables, angle_mode=angle_mode or _ANGULAR_MODE)


def interpolacion_lagrange(puntos: Sequence[Tuple[float, float]], x_eval: float) -> float:
    return _interpolacion_lagrange(list(puntos), x_eval).valor_interpolado


def biseccion(f_expr: str, a: float, b: float, tolerancia: float = 1e-6, max_iter: int = 100) -> BisectionResult:
    resultado = _biseccion(f_expr, a, b, tolerancia, max_iter, angle_mode=_ANGULAR_MODE)
    pasos = [
        BisectionStep(
            iteracion=paso.iteracion,
            a=paso.detalles["a"],
            b=paso.detalles["b"],
            c=paso.aproximacion,
            fc=paso.detalles["f_aprox"],
            error_intervalo=paso.error_absoluto,
        )
        for paso in resultado.iteraciones
    ]
    return BisectionResult(resultado.convergio, resultado.aproximacion, pasos)


def metodo_punto_fijo(g_expr: str, x0: float, tolerancia: float = 1e-6, max_iter: int = 100) -> FixedPointResult:
    resultado = _punto_fijo(g_expr, x0, tolerancia, max_iter, angle_mode=_ANGULAR_MODE)
    pasos = [
        FixedPointStep(
            iteracion=paso.iteracion,
            x_anterior=paso.detalles["x_anterior"],
            x_actual=paso.aproximacion,
            error=paso.error_absoluto,
        )
        for paso in resultado.iteraciones
    ]
    return FixedPointResult(resultado.convergio, resultado.aproximacion, pasos)


def newton_raphson(f_expr: str, df_expr: str, x0: float, tolerancia: float = 1e-6, max_iter: int = 100) -> NewtonResult:
    resultado = _newton_raphson(f_expr, x0, df_expr, tolerancia, max_iter, angle_mode=_ANGULAR_MODE)
    pasos = [
        NewtonStep(
            iteracion=paso.iteracion,
            x_anterior=paso.detalles["x_anterior"],
            x_actual=paso.aproximacion,
            error=paso.error_absoluto,
            fx_actual=paso.detalles["f_aprox"],
        )
        for paso in resultado.iteraciones
    ]
    return NewtonResult(resultado.convergio, resultado.aproximacion, pasos)


def diferencia_central(f_expr: str, x: float, h: float = 1e-4) -> float:
    return _diferencia_central(f_expr, x, h, angle_mode=_ANGULAR_MODE)


def trapecio_compuesto(f_expr: str, a: float, b: float, n: int) -> float:
    return _trapecio_compuesto(f_expr, a, b, n, angle_mode=_ANGULAR_MODE).valor_aproximado


def simpson_13_compuesto(f_expr: str, a: float, b: float, n: int) -> float:
    return _simpson_13_compuesto(f_expr, a, b, n, angle_mode=_ANGULAR_MODE).valor_aproximado


def simpson_38_compuesto(f_expr: str, a: float, b: float, n: int) -> float:
    return _simpson_38_compuesto(f_expr, a, b, n, angle_mode=_ANGULAR_MODE).valor_aproximado


def rectangulo_medio_compuesto(f_expr: str, a: float, b: float, n: int) -> float:
    return _rectangulo_medio_compuesto(f_expr, a, b, n, angle_mode=_ANGULAR_MODE).valor_aproximado


def cuadratura_gauss_legendre(f_expr: str, a: float, b: float, orden: int = 3) -> float:
    return _cuadratura_gauss_legendre(f_expr, a, b, orden, angle_mode=_ANGULAR_MODE).valor_aproximado


def gauss_legendre_cuadratura(f_expr: str, a: float, b: float, orden: int = 3) -> float:
    return cuadratura_gauss_legendre(f_expr, a, b, orden)


def integracion_montecarlo(
    f_expr: str,
    a: float,
    b: float,
    n: int,
    confianza: float = 0.95,
    seed: int | None = None,
    angle_mode: str | None = None,
) -> MonteCarloResult:
    resultado = _integracion_montecarlo(f_expr, a, b, n, confianza, seed, angle_mode=angle_mode or _ANGULAR_MODE)
    return MonteCarloResult(
        estimacion=resultado.estimacion,
        desvio_muestral=resultado.desvio_muestral,
        error_estandar=resultado.error_estandar,
        ic_bajo=resultado.ic_bajo,
        ic_alto=resultado.ic_alto,
        confianza=resultado.confianza,
        n=len(resultado.puntos),
        muestras_transformadas=[p.aporte for p in resultado.puntos],
    )


def intervalo_confianza_normal(media: float, desvio_muestral: float, n: int, confianza: float = 0.95) -> tuple[float, float]:
    if n < 2:
        raise ValueError("n debe ser mayor o igual a 2 para intervalo de confianza.")
    if not (0 < confianza < 1):
        raise ValueError("La confianza debe estar entre 0 y 1.")
    error_estandar = desvio_muestral / (n ** 0.5)
    z = NormalDist().inv_cdf(0.5 + confianza / 2.0)
    margen = z * error_estandar
    return media - margen, media + margen


def aitken_delta_cuadrado(secuencia: Sequence[float]) -> float:
    return _aitken_delta_cuadrado(list(secuencia))


def aitken_desde_punto_fijo(g_expr: str, x0: float, tolerancia: float = 1e-6, max_iter: int = 100) -> AitkenResult:
    resultado = _aitken_desde_punto_fijo(g_expr, x0, tolerancia, max_iter, angle_mode=_ANGULAR_MODE)
    pasos = [
        AitkenStep(
            iteracion=paso.iteracion,
            xn=paso.detalles["xn"],
            xn1=paso.detalles["xn1"],
            xn2=paso.detalles["xn2"],
            x_aitken=paso.aproximacion,
            error=paso.error_absoluto,
        )
        for paso in resultado.iteraciones
    ]
    return AitkenResult(resultado.convergio, resultado.aproximacion, pasos)


def runge_kutta_4(ode_expr: str, t0: float, y0: float, h: float, pasos: int) -> List[RK4Step]:
    resultado = _runge_kutta_4(ode_expr, t0, y0, h, pasos, angle_mode=_ANGULAR_MODE)
    return [RK4Step(paso=paso.paso, t=paso.t, y=paso.y) for paso in resultado.pasos]


def crecimiento_logistico(r: float, k: float, x0: float, pasos: int) -> List[float]:
    if pasos < 1:
        raise ValueError("El numero de pasos debe ser mayor o igual a 1.")
    if k == 0:
        raise ValueError("K no puede ser cero.")
    serie = [x0]
    actual = x0
    for _ in range(pasos):
        actual = r * actual * (1 - actual / k)
        serie.append(actual)
    return serie


class MetodosNumericos:
    """Wrapper orientado a objetos para consumo legado."""

    biseccion = staticmethod(biseccion)
    punto_fijo = staticmethod(metodo_punto_fijo)
    newton_raphson = staticmethod(newton_raphson)
    lagrange = staticmethod(interpolacion_lagrange)
    diferencia_central = staticmethod(diferencia_central)
    aitken_accelerator = staticmethod(aitken_delta_cuadrado)
    aitken_punto_fijo = staticmethod(aitken_desde_punto_fijo)
    runge_kutta_4 = staticmethod(runge_kutta_4)
    trapecio = staticmethod(trapecio_compuesto)
    simpson_13 = staticmethod(simpson_13_compuesto)
    simpson_38 = staticmethod(simpson_38_compuesto)
    rectangulo_medio = staticmethod(rectangulo_medio_compuesto)
    gauss_legendre = staticmethod(cuadratura_gauss_legendre)
    montecarlo = staticmethod(integracion_montecarlo)
    set_modo_angular = staticmethod(set_angular_mode)
