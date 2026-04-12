"""Servidor Flask – API REST para el laboratorio de métodos numéricos."""

from __future__ import annotations

import math
import os
from dataclasses import asdict
from typing import Any

from flask import Flask, jsonify, render_template, request

from core.metodos_numericos.aitken import aitken_desde_punto_fijo
from core.metodos_numericos.edo import euler, heun, runge_kutta_4
from core.metodos_numericos.integracion import (
    cuadratura_gauss_legendre,
    rectangulo_medio_compuesto,
    simpson_13_compuesto,
    simpson_38_compuesto,
    trapecio_compuesto,
)
from core.metodos_numericos.interpolacion import diferencia_central, interpolacion_lagrange
from core.metodos_numericos.monte_carlo import estimar_pi_geometrico, integracion_montecarlo
from core.metodos_numericos.raices import biseccion, newton_raphson, punto_fijo
from core.metodos_numericos.sistemas_lineales import eliminacion_gauss
from core.utils.parser_funciones import expression_to_callable

_BASE = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(_BASE, "web", "templates"),
    static_folder=os.path.join(_BASE, "web", "static"),
)

# ---------------------------------------------------------------------------
#  Helpers
# ---------------------------------------------------------------------------

def _safe(obj: Any) -> Any:
    """Convierte valores no-JSON (NaN, Inf) a None para serialización segura."""
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    if isinstance(obj, dict):
        return {k: _safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_safe(v) for v in obj]
    return obj


def _json_ok(data: dict) -> tuple:
    return jsonify(_safe(data)), 200


def _json_err(msg: str, code: int = 400) -> tuple:
    return jsonify({"error": str(msg)}), code


def _body() -> dict:
    return request.get_json(force=True)


# ---------------------------------------------------------------------------
#  Página principal
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


# ---------------------------------------------------------------------------
#  RAÍCES
# ---------------------------------------------------------------------------

@app.route("/api/raices/biseccion", methods=["POST"])
def api_biseccion():
    try:
        d = _body()
        r = biseccion(d["f_expr"], float(d["a"]), float(d["b"]),
                       float(d.get("tolerancia", 1e-6)),
                       int(d.get("max_iter", 100)))
        return _json_ok({
            "convergio": r.convergio,
            "aproximacion": r.aproximacion,
            "mensaje": r.mensaje,
            "iteraciones": [asdict(p) for p in r.iteraciones],
        })
    except Exception as exc:
        return _json_err(exc)


@app.route("/api/raices/punto-fijo", methods=["POST"])
def api_punto_fijo():
    try:
        d = _body()
        r = punto_fijo(d["g_expr"], float(d["x0"]),
                       float(d.get("tolerancia", 1e-6)),
                       int(d.get("max_iter", 100)))
        return _json_ok({
            "convergio": r.convergio,
            "aproximacion": r.aproximacion,
            "mensaje": r.mensaje,
            "iteraciones": [asdict(p) for p in r.iteraciones],
        })
    except Exception as exc:
        return _json_err(exc)


@app.route("/api/raices/newton-raphson", methods=["POST"])
def api_newton():
    try:
        d = _body()
        r = newton_raphson(d["f_expr"], float(d["x0"]),
                           d.get("df_expr") or None,
                           float(d.get("tolerancia", 1e-6)),
                           int(d.get("max_iter", 100)))
        return _json_ok({
            "convergio": r.convergio,
            "aproximacion": r.aproximacion,
            "mensaje": r.mensaje,
            "iteraciones": [asdict(p) for p in r.iteraciones],
        })
    except Exception as exc:
        return _json_err(exc)


@app.route("/api/raices/aitken", methods=["POST"])
def api_aitken():
    try:
        d = _body()
        r = aitken_desde_punto_fijo(d["g_expr"], float(d["x0"]),
                                     float(d.get("tolerancia", 1e-6)),
                                     int(d.get("max_iter", 100)))
        return _json_ok({
            "convergio": r.convergio,
            "aproximacion": r.aproximacion,
            "mensaje": r.mensaje,
            "iteraciones": [asdict(p) for p in r.iteraciones],
        })
    except Exception as exc:
        return _json_err(exc)


# ---------------------------------------------------------------------------
#  INTERPOLACIÓN
# ---------------------------------------------------------------------------

@app.route("/api/interpolacion/lagrange", methods=["POST"])
def api_lagrange():
    try:
        d = _body()
        puntos = [(float(p[0]), float(p[1])) for p in d["puntos"]]
        r = interpolacion_lagrange(puntos, float(d["x_eval"]))
        return _json_ok({
            "valor_interpolado": r.valor_interpolado,
            "mensaje": r.mensaje,
            "polinomio": r.metadatos.get("polinomio", ""),
            "puntos": puntos,
            "x_eval": float(d["x_eval"]),
        })
    except Exception as exc:
        return _json_err(exc)


@app.route("/api/interpolacion/derivada-central", methods=["POST"])
def api_derivada_central():
    try:
        d = _body()
        valor = diferencia_central(d["f_expr"], float(d["x"]),
                                    float(d.get("h", 1e-4)))
        return _json_ok({"derivada": valor, "mensaje": f"f'({d['x']}) ≈ {valor:.10f}"})
    except Exception as exc:
        return _json_err(exc)


# ---------------------------------------------------------------------------
#  INTEGRACIÓN
# ---------------------------------------------------------------------------

def _api_integracion(metodo_fn, d):
    valor_exacto = float(d["valor_exacto"]) if d.get("valor_exacto") not in (None, "", "null") else None
    r = metodo_fn(d["f_expr"], float(d["a"]), float(d["b"]),
                  int(d["n"]), valor_exacto)
    return _json_ok({
        "valor_aproximado": r.valor_aproximado,
        "valor_exacto": r.valor_exacto,
        "error_absoluto": r.error_absoluto,
        "error_relativo": r.error_relativo,
        "mensaje": r.mensaje,
        "muestras": [asdict(m) for m in r.muestras],
    })


@app.route("/api/integracion/trapecio", methods=["POST"])
def api_trapecio():
    try:
        return _api_integracion(trapecio_compuesto, _body())
    except Exception as exc:
        return _json_err(exc)


@app.route("/api/integracion/simpson13", methods=["POST"])
def api_simpson13():
    try:
        return _api_integracion(simpson_13_compuesto, _body())
    except Exception as exc:
        return _json_err(exc)


@app.route("/api/integracion/simpson38", methods=["POST"])
def api_simpson38():
    try:
        return _api_integracion(simpson_38_compuesto, _body())
    except Exception as exc:
        return _json_err(exc)


@app.route("/api/integracion/rectangulo", methods=["POST"])
def api_rectangulo():
    try:
        return _api_integracion(rectangulo_medio_compuesto, _body())
    except Exception as exc:
        return _json_err(exc)


@app.route("/api/integracion/gauss-legendre", methods=["POST"])
def api_gauss():
    try:
        d = _body()
        valor_exacto = float(d["valor_exacto"]) if d.get("valor_exacto") not in (None, "", "null") else None
        r = cuadratura_gauss_legendre(d["f_expr"], float(d["a"]), float(d["b"]),
                                       int(d.get("n", 3)), valor_exacto)
        return _json_ok({
            "valor_aproximado": r.valor_aproximado,
            "valor_exacto": r.valor_exacto,
            "error_absoluto": r.error_absoluto,
            "error_relativo": r.error_relativo,
            "mensaje": r.mensaje,
            "muestras": [asdict(m) for m in r.muestras],
        })
    except Exception as exc:
        return _json_err(exc)


# ---------------------------------------------------------------------------
#  MONTE CARLO
# ---------------------------------------------------------------------------

@app.route("/api/montecarlo/integral", methods=["POST"])
def api_mc_integral():
    try:
        d = _body()
        r = integracion_montecarlo(d["f_expr"], float(d["a"]), float(d["b"]),
                                    int(d.get("n", 5000)),
                                    float(d.get("confianza", 0.95)),
                                    int(d["seed"]) if d.get("seed") else None)
        return _json_ok({
            "estimacion": r.estimacion,
            "desvio_muestral": r.desvio_muestral,
            "error_estandar": r.error_estandar,
            "ic_bajo": r.ic_bajo,
            "ic_alto": r.ic_alto,
            "confianza": r.confianza,
            "mensaje": r.mensaje,
            "aportes": [p.aporte for p in r.puntos],
        })
    except Exception as exc:
        return _json_err(exc)


@app.route("/api/montecarlo/pi", methods=["POST"])
def api_mc_pi():
    try:
        d = _body()
        r = estimar_pi_geometrico(int(d.get("n", 10000)),
                                   int(d["seed"]) if d.get("seed") else None)
        return _json_ok({
            "estimacion": r.estimacion,
            "desvio_muestral": r.desvio_muestral,
            "error_estandar": r.error_estandar,
            "ic_bajo": r.ic_bajo,
            "ic_alto": r.ic_alto,
            "confianza": r.confianza,
            "mensaje": r.mensaje,
            "aportes": [p.aporte for p in r.puntos],
        })
    except Exception as exc:
        return _json_err(exc)


# ---------------------------------------------------------------------------
#  EDO
# ---------------------------------------------------------------------------

def _api_edo(metodo_fn, d):
    sol = d.get("solucion_exacta") or None
    r = metodo_fn(d["ode_expr"], float(d["t0"]), float(d["y0"]),
                  float(d["h"]), int(d["pasos"]), sol)
    return _json_ok({
        "mensaje": r.mensaje,
        "pasos": [asdict(p) for p in r.pasos],
    })


@app.route("/api/edo/euler", methods=["POST"])
def api_euler():
    try:
        return _api_edo(euler, _body())
    except Exception as exc:
        return _json_err(exc)


@app.route("/api/edo/heun", methods=["POST"])
def api_heun():
    try:
        return _api_edo(heun, _body())
    except Exception as exc:
        return _json_err(exc)


@app.route("/api/edo/rk4", methods=["POST"])
def api_rk4():
    try:
        return _api_edo(runge_kutta_4, _body())
    except Exception as exc:
        return _json_err(exc)


# ---------------------------------------------------------------------------
#  SISTEMAS LINEALES
# ---------------------------------------------------------------------------

@app.route("/api/sistemas/gauss", methods=["POST"])
def api_gauss_sistema():
    try:
        d = _body()
        matriz = [[float(c) for c in fila] for fila in d["matriz"]]
        vector = [float(v) for v in d["vector"]]
        r = eliminacion_gauss(matriz, vector)
        return _json_ok({
            "solucion": r.solucion,
            "residuo": r.residuo,
            "mensaje": r.mensaje,
        })
    except Exception as exc:
        return _json_err(exc)


# ---------------------------------------------------------------------------
#  UTILIDAD – evaluar curva para gráficos frontend
# ---------------------------------------------------------------------------

@app.route("/api/util/evaluar-curva", methods=["POST"])
def api_evaluar_curva():
    """Evalúa f(x) en un rango para dibujar la curva en Plotly.js."""
    try:
        d = _body()
        f = expression_to_callable(d["f_expr"], ("x",))
        a = float(d["a"])
        b = float(d["b"])
        n_puntos = int(d.get("n_puntos", 300))
        xs = [a + (b - a) * i / n_puntos for i in range(n_puntos + 1)]
        ys = []
        for x in xs:
            try:
                ys.append(f(x))
            except Exception:
                ys.append(None)
        return _json_ok({"xs": xs, "ys": ys})
    except Exception as exc:
        return _json_err(exc)


# ---------------------------------------------------------------------------
#  Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, port=5000)
