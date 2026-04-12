"""Funciones de validacion de entradas para metodos numericos."""

from __future__ import annotations

from typing import Iterable, Sequence

from .errores import ValidationError


def validar_tolerancia(tolerancia: float) -> None:
    if tolerancia <= 0:
        raise ValidationError("La tolerancia debe ser mayor a cero.")


def validar_max_iter(max_iter: int) -> None:
    if max_iter <= 0:
        raise ValidationError("El maximo de iteraciones debe ser mayor a cero.")


def validar_intervalo(a: float, b: float) -> None:
    if a >= b:
        raise ValidationError("El intervalo debe cumplir a < b.")


def validar_subintervalos(n: int, minimo: int = 1) -> None:
    if n < minimo:
        raise ValidationError(f"n debe ser mayor o igual a {minimo}.")


def validar_paso(h: float) -> None:
    if h <= 0:
        raise ValidationError("El paso debe ser mayor a cero.")


def validar_puntos_interpolacion(puntos: Sequence[tuple[float, float]]) -> None:
    if len(puntos) < 2:
        raise ValidationError("Se necesitan al menos dos puntos para interpolar.")
    xs = [x for x, _ in puntos]
    if len(set(xs)) != len(xs):
        raise ValidationError("Los valores de x deben ser distintos.")


def validar_dimension_sistema(matriz: Sequence[Sequence[float]], vector: Sequence[float]) -> None:
    if not matriz or not vector:
        raise ValidationError("La matriz y el vector no pueden estar vacios.")
    filas = len(matriz)
    if filas != len(vector):
        raise ValidationError("La matriz y el vector deben tener dimensiones compatibles.")
    for fila in matriz:
        if len(fila) != filas:
            raise ValidationError("La matriz del sistema debe ser cuadrada.")


def validar_confianza(confianza: float) -> None:
    if not (0 < confianza < 1):
        raise ValidationError("La confianza debe estar entre 0 y 1.")


def validar_muestras(n: int, minimo: int = 2) -> None:
    if n < minimo:
        raise ValidationError(f"La cantidad de muestras debe ser al menos {minimo}.")


def validar_iterable_no_vacio(valores: Iterable[float], minimo: int, mensaje: str) -> list[float]:
    lista = list(valores)
    if len(lista) < minimo:
        raise ValidationError(mensaje)
    return lista
