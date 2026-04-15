"""Aplicacion Streamlit del laboratorio numerico."""

from __future__ import annotations

from dataclasses import asdict

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from casos.ejemplos_aplicados import APPLIED_CASES
from casos.ejercicios_tp import INTEGRATION_CASES, INTERPOLATION_CASES, ODE_CASES, ROOT_CASES
from core.metodos_numericos.edo import euler, heun, runge_kutta_4
from core.metodos_numericos.integracion import cuadratura_gauss_legendre, simpson_13_compuesto, simpson_38_compuesto, trapecio_compuesto
from core.metodos_numericos.interpolacion import diferencia_central, interpolacion_lagrange
from core.metodos_numericos.monte_carlo import estimar_pi_geometrico, integracion_montecarlo
from core.metodos_numericos.raices import biseccion, newton_raphson, punto_fijo
from core.metodos_numericos.sistemas_lineales import eliminacion_gauss
from visualizacion.graficos_edo import grafico_trayectoria_edo
from visualizacion.graficos_integracion import grafico_integrando
from visualizacion.graficos_interpolacion import grafico_lagrange
from visualizacion.graficos_montecarlo import histograma_montecarlo
from visualizacion.graficos_raices import grafico_convergencia_raices, grafico_funcion_raiz


def _parsear_puntos(raw: str) -> list[tuple[float, float]]:
    puntos = []
    for bloque in raw.split(";"):
        bloque = bloque.strip()
        if not bloque:
            continue
        x, y = [float(valor.strip()) for valor in bloque.split(",")]
        puntos.append((x, y))
    return puntos


def _mostrar_dataframe(registros: list[dict]) -> None:
    st.dataframe(pd.DataFrame(registros), use_container_width=True)


def _resolver_edo_por_metodo(
    metodo: str,
    ode_expr: str,
    t0: float,
    y0: float,
    h: float,
    pasos: int,
    solucion_exacta: str | None,
):
    if metodo == "Euler":
        return euler(ode_expr, t0, y0, h, pasos, solucion_exacta)
    if metodo == "Heun":
        return heun(ode_expr, t0, y0, h, pasos, solucion_exacta)
    return runge_kutta_4(ode_expr, t0, y0, h, pasos, solucion_exacta)


def _grafico_hornalla(resultado, temperatura_ambiente: float) -> go.Figure:
    tiempos = [paso.t for paso in resultado.pasos]
    temperaturas = [paso.y for paso in resultado.pasos]
    distancia_ambiente = [abs(temp - temperatura_ambiente) for temp in temperaturas]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=tiempos,
            y=temperaturas,
            mode="lines+markers",
            name="Temperatura de la olla",
            line={"color": "#e74c3c", "width": 3},
            marker={"size": 7},
        )
    )
    fig.add_trace(
        go.Scatter(
            x=tiempos,
            y=[temperatura_ambiente for _ in tiempos],
            mode="lines",
            name="Temperatura ambiente",
            line={"color": "#2ecc71", "width": 2, "dash": "dash"},
        )
    )
    fig.add_trace(
        go.Scatter(
            x=tiempos,
            y=distancia_ambiente,
            mode="lines+markers",
            name="Distancia al ambiente",
            line={"color": "#3498db", "width": 2},
            marker={"size": 6},
            yaxis="y2",
        )
    )
    fig.update_layout(
        title="Propagación del calor de la hornalla",
        xaxis_title="Tiempo (minutos)",
        yaxis_title="Temperatura (°C)",
        yaxis2={
            "title": "Distancia al ambiente (°C)",
            "overlaying": "y",
            "side": "right",
            "showgrid": False,
        },
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "x": 0},
        margin={"l": 40, "r": 40, "t": 70, "b": 40},
        template="plotly_white",
    )
    return fig


def _panel_casos() -> None:
    st.subheader("Caso práctico integrado")
    st.write("Simulación de propagación del calor de una hornalla en una olla, explicada de forma simple.")
    st.markdown("**Idea simple:** la temperatura de la olla se va acercando a la del ambiente con el tiempo.")
    st.latex(r"T'(t) = -k\,(T - T_{amb})")

    caso = APPLIED_CASES["ingenieria_enfriamiento"]
    p = caso["parametros"]

    c1, c2 = st.columns(2)
    with c1:
        metodo = st.selectbox("Método numérico", ["Euler", "Heun", "RK4"], index=1)
        temperatura_inicial = st.number_input(
            "Temperatura inicial de la olla (°C)",
            value=float(p["y0"]),
            step=1.0,
        )
        temperatura_ambiente = st.number_input(
            "Temperatura ambiente (°C)",
            value=float(p["temperatura_ambiente"]),
            step=1.0,
        )
    with c2:
        k = st.number_input("Velocidad de intercambio (k)", value=float(p["k"]), min_value=0.01, step=0.05)
        h = st.number_input("Paso de tiempo (min)", value=float(p["h"]), min_value=0.01, step=0.1, format="%.4f")
        pasos = st.number_input("Cantidad de pasos", value=int(p["pasos"]), min_value=1, step=1)

    if st.button("Simular caso de hornalla", use_container_width=True):
        ode_expr = f"-{k}*(y-{temperatura_ambiente})"
        exacta_expr = f"{temperatura_ambiente}+({temperatura_inicial}-{temperatura_ambiente})*exp(-{k}*t)"
        resultado = _resolver_edo_por_metodo(
            metodo,
            ode_expr,
            float(p["t0"]),
            float(temperatura_inicial),
            float(h),
            int(pasos),
            exacta_expr,
        )

        st.success("Simulación completada.")

        inicio = resultado.pasos[0].y
        fin = resultado.pasos[-1].y
        distancia_final = abs(fin - temperatura_ambiente)
        direccion = "se enfrió" if inicio > temperatura_ambiente else "se calentó"

        st.info(
            f"La olla empezó en {inicio:.2f} °C y {direccion} hasta {fin:.2f} °C. "
            f"Al final quedó a {distancia_final:.2f} °C de la temperatura ambiente."
        )

        m1, m2, m3 = st.columns(3)
        m1.metric("Temperatura inicial", f"{inicio:.2f} °C")
        m2.metric("Temperatura final", f"{fin:.2f} °C")
        m3.metric("Distancia al ambiente", f"{distancia_final:.2f} °C")

        st.plotly_chart(_grafico_hornalla(resultado, float(temperatura_ambiente)), use_container_width=True)

        tabla = pd.DataFrame(
            [
                {
                    "Paso": paso.paso,
                    "Tiempo (min)": paso.t,
                    "Temperatura (°C)": paso.y,
                    "Diferencia con ambiente (°C)": abs(paso.y - temperatura_ambiente),
                }
                for paso in resultado.pasos
            ]
        )
        st.dataframe(tabla, use_container_width=True)

    with st.expander("Ver otros casos disponibles"):
        st.json(
            {
                "raices": list(ROOT_CASES.keys()),
                "interpolacion": list(INTERPOLATION_CASES.keys()),
                "integracion": list(INTEGRATION_CASES.keys()),
                "edo": list(ODE_CASES.keys()),
                "aplicados": list(APPLIED_CASES.keys()),
            }
        )


def _panel_raices() -> None:
    metodo = st.selectbox("Metodo de raices", ["Biseccion", "Punto fijo", "Newton-Raphson"])
    if metodo == "Biseccion":
        f_expr = st.text_input("f(x)", value=ROOT_CASES["biseccion_cos"]["parametros"]["f_expr"])
        a = st.number_input("a", value=0.0)
        b = st.number_input("b", value=1.0)
        tol = st.number_input("Tolerancia", value=1e-6, format="%.10f")
        max_iter = st.number_input("Max iteraciones", value=100, min_value=1)
        if st.button("Ejecutar biseccion", use_container_width=True):
            resultado = biseccion(f_expr, a, b, float(tol), int(max_iter))
            st.success(resultado.mensaje)
            _mostrar_dataframe([asdict(paso) for paso in resultado.iteraciones])
            st.plotly_chart(grafico_convergencia_raices(resultado), use_container_width=True)
            st.plotly_chart(grafico_funcion_raiz(f_expr, resultado.aproximacion, a, b), use_container_width=True)
    elif metodo == "Punto fijo":
        g_expr = st.text_input("g(x)", value=ROOT_CASES["punto_fijo_cos"]["parametros"]["g_expr"])
        x0 = st.number_input("x0", value=0.5)
        tol = st.number_input("Tolerancia PF", value=1e-6, format="%.10f")
        max_iter = st.number_input("Max iter PF", value=100, min_value=1)
        if st.button("Ejecutar punto fijo", use_container_width=True):
            resultado = punto_fijo(g_expr, x0, float(tol), int(max_iter))
            st.success(resultado.mensaje)
            _mostrar_dataframe([asdict(paso) for paso in resultado.iteraciones])
            st.plotly_chart(grafico_convergencia_raices(resultado), use_container_width=True)
    else:
        f_expr = st.text_input("f(x)", value=ROOT_CASES["newton_cubica"]["parametros"]["f_expr"])
        df_expr = st.text_input("f'(x) opcional", value=ROOT_CASES["newton_cubica"]["parametros"]["df_expr"])
        x0 = st.number_input("x0", value=1.5)
        tol = st.number_input("Tolerancia Newton", value=1e-6, format="%.10f")
        max_iter = st.number_input("Max iter Newton", value=100, min_value=1)
        if st.button("Ejecutar Newton", use_container_width=True):
            resultado = newton_raphson(f_expr, x0, df_expr or None, float(tol), int(max_iter))
            st.success(resultado.mensaje)
            _mostrar_dataframe([asdict(paso) for paso in resultado.iteraciones])
            st.plotly_chart(grafico_convergencia_raices(resultado), use_container_width=True)


def _panel_interpolacion() -> None:
    raw = st.text_area("Puntos", value="1,1; 2,4; 3,9")
    x_eval = st.number_input("x a evaluar", value=1.5)
    h = st.number_input("h para derivada central", value=0.01, format="%.10f")
    f_expr = st.text_input("f(x) para derivada opcional", value="sin(x)")
    if st.button("Interpolar", use_container_width=True):
        puntos = _parsear_puntos(raw)
        resultado = interpolacion_lagrange(puntos, x_eval)
        st.success(resultado.mensaje)
        st.write(f"Valor interpolado: `{resultado.valor_interpolado:.10f}`")
        st.write(f"Polinomio: `{resultado.metadatos['polinomio']}`")
        st.plotly_chart(grafico_lagrange(puntos, x_eval), use_container_width=True)
    if st.button("Derivar por diferencia central", use_container_width=True):
        derivada = diferencia_central(f_expr, x_eval, float(h))
        st.info(f"f'({x_eval}) ~= {derivada:.10f}")


def _panel_integracion() -> None:
    metodo = st.selectbox("Metodo de integracion", ["Trapecio compuesto", "Simpson 1/3", "Simpson 3/8", "Gauss-Legendre"])
    f_expr = st.text_input("f(x)", value=INTEGRATION_CASES["simpson_sin"]["parametros"]["f_expr"])
    a = st.number_input("a", value=0.0)
    b = st.number_input("b", value=3.141592653589793)
    n = st.number_input("n / orden", value=10, min_value=1)
    exacto = st.text_input("Valor exacto opcional", value="2.0")
    valor_exacto = float(exacto) if exacto.strip() else None
    if st.button("Integrar", use_container_width=True):
        if metodo == "Trapecio compuesto":
            resultado = trapecio_compuesto(f_expr, a, b, int(n), valor_exacto)
        elif metodo == "Simpson 1/3":
            resultado = simpson_13_compuesto(f_expr, a, b, int(n), valor_exacto)
        elif metodo == "Simpson 3/8":
            resultado = simpson_38_compuesto(f_expr, a, b, int(n), valor_exacto)
        else:
            resultado = cuadratura_gauss_legendre(f_expr, a, b, int(n), valor_exacto)
        st.success(resultado.mensaje)
        st.write(f"Integral aproximada: `{resultado.valor_aproximado:.10f}`")
        if resultado.valor_exacto is not None:
            st.write(f"Error absoluto: `{resultado.error_absoluto:.3e}`")
        _mostrar_dataframe([asdict(muestra) for muestra in resultado.muestras])
        st.plotly_chart(grafico_integrando(f_expr, a, b), use_container_width=True)


def _panel_montecarlo() -> None:
    modo = st.radio("Modo Monte Carlo", ["Integral", "Estimacion de pi"], horizontal=True)
    if modo == "Integral":
        f_expr = st.text_input("f(x)", value="exp(-x**2)")
        a = st.number_input("a", value=0.0)
        b = st.number_input("b", value=1.0)
        n = st.number_input("muestras", value=5000, min_value=10)
        if st.button("Ejecutar Monte Carlo", use_container_width=True):
            resultado = integracion_montecarlo(f_expr, a, b, int(n))
            st.success(resultado.mensaje)
            st.write(f"Estimacion: `{resultado.estimacion:.10f}`")
            st.write(f"IC 95%: `[{resultado.ic_bajo:.10f}, {resultado.ic_alto:.10f}]`")
            st.plotly_chart(histograma_montecarlo(resultado), use_container_width=True)
    else:
        n = st.number_input("muestras para pi", value=10000, min_value=10)
        if st.button("Estimar pi", use_container_width=True):
            resultado = estimar_pi_geometrico(int(n))
            st.success(resultado.mensaje)
            st.write(f"Estimacion de pi: `{resultado.estimacion:.10f}`")
            st.plotly_chart(histograma_montecarlo(resultado), use_container_width=True)


def _panel_edo() -> None:
    metodo = st.selectbox("Metodo EDO", ["Euler", "Heun", "RK4"])
    ode_expr = st.text_input("f(t, y)", value="y")
    solucion_exacta = st.text_input("Solucion exacta opcional", value="exp(t)")
    t0 = st.number_input("t0", value=0.0)
    y0 = st.number_input("y0", value=1.0)
    h = st.number_input("h", value=0.1, format="%.10f")
    pasos = st.number_input("pasos", value=10, min_value=1)
    if st.button("Resolver EDO", use_container_width=True):
        resultado = _resolver_edo_por_metodo(metodo, ode_expr, t0, y0, float(h), int(pasos), solucion_exacta or None)
        st.success(resultado.mensaje)
        _mostrar_dataframe([asdict(paso) for paso in resultado.pasos])
        st.plotly_chart(grafico_trayectoria_edo(resultado), use_container_width=True)


def _panel_sistemas() -> None:
    st.write("Ejemplo base: sistema 2x2.")
    a11 = st.number_input("A11", value=2.0)
    a12 = st.number_input("A12", value=1.0)
    a21 = st.number_input("A21", value=1.0)
    a22 = st.number_input("A22", value=3.0)
    b1 = st.number_input("b1", value=1.0)
    b2 = st.number_input("b2", value=2.0)
    if st.button("Resolver sistema", use_container_width=True):
        resultado = eliminacion_gauss([[a11, a12], [a21, a22]], [b1, b2])
        st.success(resultado.mensaje)
        st.write(f"Solucion: `{resultado.solucion}`")
        st.write(f"Residuo: `{resultado.residuo}`")


def main() -> None:
    st.set_page_config(page_title="Laboratorio de Modelado y Simulacion", layout="wide")
    st.title("Laboratorio de Modelado y Simulacion de Metodos Numericos")
    st.caption("Plataforma academica y tecnica para explorar metodos numericos, simulacion y visualizacion.")

    seccion = st.sidebar.selectbox(
        "Seccion",
        ["Casos", "Raices", "Interpolacion", "Integracion", "Monte Carlo", "EDO", "Sistemas lineales"],
    )
    if seccion == "Casos":
        _panel_casos()
    elif seccion == "Raices":
        _panel_raices()
    elif seccion == "Interpolacion":
        _panel_interpolacion()
    elif seccion == "Integracion":
        _panel_integracion()
    elif seccion == "Monte Carlo":
        _panel_montecarlo()
    elif seccion == "EDO":
        _panel_edo()
    else:
        _panel_sistemas()
