"""Helpers para usar el laboratorio desde notebooks."""

from __future__ import annotations

from core.metodos_numericos.edo import euler, heun, runge_kutta_4
from core.metodos_numericos.integracion import cuadratura_gauss_legendre, simpson_13_compuesto, simpson_38_compuesto, trapecio_compuesto
from core.metodos_numericos.interpolacion import interpolacion_lagrange
from core.metodos_numericos.monte_carlo import estimar_pi_geometrico, integracion_montecarlo
from core.metodos_numericos.raices import biseccion, newton_raphson, punto_fijo
from core.metodos_numericos.sistemas_lineales import eliminacion_gauss

__all__ = [
    "biseccion",
    "punto_fijo",
    "newton_raphson",
    "interpolacion_lagrange",
    "trapecio_compuesto",
    "simpson_13_compuesto",
    "simpson_38_compuesto",
    "cuadratura_gauss_legendre",
    "integracion_montecarlo",
    "estimar_pi_geometrico",
    "euler",
    "heun",
    "runge_kutta_4",
    "eliminacion_gauss",
]
