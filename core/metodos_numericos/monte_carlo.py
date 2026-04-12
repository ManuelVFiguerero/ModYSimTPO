"""Metodos de simulacion estocastica por Monte Carlo."""

from __future__ import annotations

import math
import random
from statistics import NormalDist

from core.utils.parser_funciones import expression_to_callable
from core.utils.resultados import MonteCarloPoint, MonteCarloResult
from core.utils.validaciones import validar_confianza, validar_intervalo, validar_muestras


def integracion_montecarlo(
    f_expr: str,
    a: float,
    b: float,
    n: int,
    confianza: float = 0.95,
    seed: int | None = None,
    angle_mode: str | None = None,
) -> MonteCarloResult:
    """Estima una integral definida por muestreo uniforme."""
    validar_intervalo(a, b)
    validar_muestras(n, 2)
    validar_confianza(confianza)

    rng = random.Random(seed)
    f = expression_to_callable(f_expr, ("x",), angle_mode=angle_mode)
    ancho = b - a
    aportes: list[float] = []
    puntos: list[MonteCarloPoint] = []
    for indice in range(1, n + 1):
        x = rng.uniform(a, b)
        fx = f(x)
        aporte = ancho * fx
        aportes.append(aporte)
        puntos.append(MonteCarloPoint(indice, x, fx, aporte))

    media = sum(aportes) / n
    varianza = sum((valor - media) ** 2 for valor in aportes) / (n - 1)
    desvio = math.sqrt(varianza)
    error_estandar = desvio / math.sqrt(n)
    z = NormalDist().inv_cdf(0.5 + confianza / 2.0)
    margen = z * error_estandar

    return MonteCarloResult(
        metodo="integracion_montecarlo",
        estimacion=media,
        desvio_muestral=desvio,
        error_estandar=error_estandar,
        ic_bajo=media - margen,
        ic_alto=media + margen,
        confianza=confianza,
        puntos=puntos,
        mensaje="Estimacion Monte Carlo completada.",
        metadatos={"n": n, "intervalo": [a, b], "seed": seed},
    )


def estimar_pi_geometrico(n: int, seed: int | None = None) -> MonteCarloResult:
    """Estima pi usando puntos aleatorios en el cuadrado unidad."""
    validar_muestras(n, 10)
    rng = random.Random(seed)
    exitos = 0
    puntos: list[MonteCarloPoint] = []
    aportes: list[float] = []
    for indice in range(1, n + 1):
        x = rng.random()
        y = rng.random()
        dentro = 1.0 if x * x + y * y <= 1.0 else 0.0
        exitos += int(dentro)
        aporte = 4.0 * dentro
        aportes.append(aporte)
        puntos.append(MonteCarloPoint(indice, x, y, aporte))

    media = sum(aportes) / n
    varianza = sum((valor - media) ** 2 for valor in aportes) / (n - 1)
    desvio = math.sqrt(varianza)
    error_estandar = desvio / math.sqrt(n)
    z = NormalDist().inv_cdf(0.975)
    margen = z * error_estandar

    return MonteCarloResult(
        metodo="monte_carlo_pi",
        estimacion=media,
        desvio_muestral=desvio,
        error_estandar=error_estandar,
        ic_bajo=media - margen,
        ic_alto=media + margen,
        confianza=0.95,
        puntos=puntos,
        mensaje="Estimacion geometrica de pi completada.",
        metadatos={"n": n, "proporcion_exitos": exitos / n, "seed": seed},
    )
