"""Parser seguro y reutilizable para expresiones matematicas."""

from __future__ import annotations

import math
from typing import Callable, Iterable, Sequence

import sympy as sp

from .errores import ExpressionParseError, ValidationError

ALLOWED_NAMES = {
    "sin": sp.sin,
    "cos": sp.cos,
    "tan": sp.tan,
    "asin": sp.asin,
    "acos": sp.acos,
    "atan": sp.atan,
    "exp": sp.exp,
    "log": sp.log,
    "sqrt": sp.sqrt,
    "abs": sp.Abs,
    "pi": sp.pi,
    "e": sp.E,
}


def _normalizar_modo_angular(angle_mode: str | None) -> str:
    if angle_mode is None:
        return "radianes"
    normalizado = angle_mode.strip().lower()
    if normalizado not in {"radianes", "grados"}:
        raise ValidationError("Modo angular invalido. Usa 'radianes' o 'grados'.")
    return normalizado


def parse_expression(expr: str, variables: Sequence[str]) -> sp.Expr:
    """Parsea una expresion de forma segura con SymPy."""
    if not expr or not expr.strip():
        raise ExpressionParseError("La expresion no puede estar vacia.")

    simbolos = {nombre: sp.Symbol(nombre) for nombre in variables}
    try:
        parsed = sp.sympify(expr, locals={**ALLOWED_NAMES, **simbolos})
    except Exception as exc:  # noqa: BLE001
        raise ExpressionParseError(f"No se pudo interpretar la expresion: {exc}") from exc

    extra = parsed.free_symbols - set(simbolos.values())
    if extra:
        nombres = ", ".join(sorted(str(simbolo) for simbolo in extra))
        raise ExpressionParseError(f"La expresion contiene variables no permitidas: {nombres}.")
    return parsed


def expression_to_callable(
    expr: str,
    variables: Sequence[str],
    angle_mode: str | None = None,
) -> Callable[..., float]:
    """Convierte una expresion a una funcion evaluable."""
    parsed = parse_expression(expr, variables)
    symbols = [sp.Symbol(nombre) for nombre in variables]
    modo = _normalizar_modo_angular(angle_mode)

    if modo == "grados":
        modules = {
            "sin": lambda x: math.sin(math.radians(x)),
            "cos": lambda x: math.cos(math.radians(x)),
            "tan": lambda x: math.tan(math.radians(x)),
            "asin": lambda x: math.degrees(math.asin(x)),
            "acos": lambda x: math.degrees(math.acos(x)),
            "atan": lambda x: math.degrees(math.atan(x)),
            "exp": math.exp,
            "log": math.log,
            "sqrt": math.sqrt,
            "Abs": abs,
        }
        compiled = sp.lambdify(symbols, parsed, modules=[modules, "math"])
    else:
        compiled = sp.lambdify(symbols, parsed, modules=["math"])

    def wrapper(*args: float) -> float:
        try:
            valor = compiled(*args)
        except Exception as exc:  # noqa: BLE001
            raise ExpressionParseError(f"No se pudo evaluar la expresion: {exc}") from exc
        try:
            return float(valor)
        except (TypeError, ValueError) as exc:
            raise ExpressionParseError("La expresion no devolvio un numero real.") from exc

    return wrapper


def evaluate_expression(
    expr: str,
    variables: dict[str, float],
    angle_mode: str | None = None,
) -> float:
    """Evalua una expresion a partir de variables nombradas."""
    ordered_names = tuple(variables.keys())
    function = expression_to_callable(expr, ordered_names, angle_mode=angle_mode)
    return function(*[variables[name] for name in ordered_names])


def derive_expression(expr: str, variable: str = "x") -> str:
    """Deriva simbolicamente una expresion respecto de una variable."""
    parsed = parse_expression(expr, [variable])
    symbol = sp.Symbol(variable)
    derivada = sp.diff(parsed, symbol)
    return str(sp.simplify(derivada))


def interpolate_polynomial_expression(puntos: Iterable[tuple[float, float]]) -> str:
    """Construye el polinomio interpolante de Lagrange como expresion simbolica."""
    x = sp.Symbol("x")
    lista = list(puntos)
    poly = sp.interpolate(lista, x)
    return str(sp.expand(poly))
