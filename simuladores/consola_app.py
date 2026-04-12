"""Aplicacion de consola del laboratorio numerico."""

from __future__ import annotations

from core.metodos_numericos.edo import euler, heun, runge_kutta_4
from core.metodos_numericos.integracion import simpson_13_compuesto, trapecio_compuesto
from core.metodos_numericos.interpolacion import interpolacion_lagrange
from core.metodos_numericos.monte_carlo import estimar_pi_geometrico, integracion_montecarlo
from core.metodos_numericos.raices import biseccion, newton_raphson, punto_fijo
from core.metodos_numericos.sistemas_lineales import eliminacion_gauss


def _leer_float(mensaje: str) -> float:
    while True:
        try:
            return float(input(mensaje).strip())
        except ValueError:
            print("Entrada invalida. Escribi un numero real.")


def _leer_int(mensaje: str, minimo: int = 1) -> int:
    while True:
        try:
            valor = int(input(mensaje).strip())
            if valor < minimo:
                print(f"El valor debe ser mayor o igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("Entrada invalida. Escribi un entero.")


def _leer_expr(mensaje: str) -> str:
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("La expresion no puede estar vacia.")


def _mostrar_iteraciones_raices(resultado) -> None:
    print(f"\nMetodo: {resultado.metodo}")
    print(f"Estado: {resultado.mensaje}")
    for paso in resultado.iteraciones:
        print(f"it={paso.iteracion:>2}  x={paso.aproximacion:.10f}  e_abs={paso.error_absoluto:.3e}")
    print(f"Resultado final: {resultado.aproximacion:.10f}")


def _resolver_raices() -> None:
    print("\n1) Biseccion\n2) Punto fijo\n3) Newton-Raphson")
    opcion = input("Elegi metodo: ").strip()
    if opcion == "1":
        resultado = biseccion(
            _leer_expr("f(x): "),
            _leer_float("a: "),
            _leer_float("b: "),
            _leer_float("Tolerancia: "),
            _leer_int("Max iteraciones: "),
        )
        _mostrar_iteraciones_raices(resultado)
    elif opcion == "2":
        resultado = punto_fijo(
            _leer_expr("g(x): "),
            _leer_float("x0: "),
            _leer_float("Tolerancia: "),
            _leer_int("Max iteraciones: "),
        )
        _mostrar_iteraciones_raices(resultado)
    elif opcion == "3":
        resultado = newton_raphson(
            _leer_expr("f(x): "),
            _leer_float("x0: "),
            _leer_expr("f'(x) [Enter no soportado en consola breve]: "),
            _leer_float("Tolerancia: "),
            _leer_int("Max iteraciones: "),
        )
        _mostrar_iteraciones_raices(resultado)
    else:
        print("Opcion invalida.")


def _resolver_integracion() -> None:
    print("\n1) Trapecio compuesto\n2) Simpson 1/3\n3) Monte Carlo\n4) Monte Carlo geometrico para pi")
    opcion = input("Elegi metodo: ").strip()
    if opcion == "1":
        resultado = trapecio_compuesto(_leer_expr("f(x): "), _leer_float("a: "), _leer_float("b: "), _leer_int("n: "))
        print(f"Integral aproximada: {resultado.valor_aproximado:.10f}")
    elif opcion == "2":
        resultado = simpson_13_compuesto(_leer_expr("f(x): "), _leer_float("a: "), _leer_float("b: "), _leer_int("n par: ", 2))
        print(f"Integral aproximada: {resultado.valor_aproximado:.10f}")
    elif opcion == "3":
        resultado = integracion_montecarlo(_leer_expr("f(x): "), _leer_float("a: "), _leer_float("b: "), _leer_int("muestras: ", 2))
        print(f"Estimacion: {resultado.estimacion:.10f}")
        print(f"IC 95%: [{resultado.ic_bajo:.10f}, {resultado.ic_alto:.10f}]")
    elif opcion == "4":
        resultado = estimar_pi_geometrico(_leer_int("muestras: ", 10))
        print(f"Estimacion de pi: {resultado.estimacion:.10f}")
    else:
        print("Opcion invalida.")


def _resolver_interpolacion() -> None:
    puntos = []
    cantidad = _leer_int("Cantidad de puntos: ", 2)
    for i in range(cantidad):
        puntos.append((_leer_float(f"x{i + 1}: "), _leer_float(f"y{i + 1}: ")))
    resultado = interpolacion_lagrange(puntos, _leer_float("x a evaluar: "))
    print(f"Valor interpolado: {resultado.valor_interpolado:.10f}")
    print(f"Polinomio: {resultado.metadatos['polinomio']}")


def _resolver_edo() -> None:
    print("\n1) Euler\n2) Heun\n3) RK4")
    opcion = input("Elegi metodo: ").strip()
    expr = _leer_expr("f(t, y): ")
    t0 = _leer_float("t0: ")
    y0 = _leer_float("y0: ")
    h = _leer_float("h: ")
    pasos = _leer_int("Cantidad de pasos: ")
    if opcion == "1":
        resultado = euler(expr, t0, y0, h, pasos)
    elif opcion == "2":
        resultado = heun(expr, t0, y0, h, pasos)
    elif opcion == "3":
        resultado = runge_kutta_4(expr, t0, y0, h, pasos)
    else:
        print("Opcion invalida.")
        return
    for paso in resultado.pasos:
        print(f"paso={paso.paso:>2}  t={paso.t:.4f}  y={paso.y:.10f}")


def _resolver_sistema_lineal() -> None:
    n = _leer_int("Dimension del sistema: ", 1)
    matriz = []
    vector = []
    print("Ingresa los coeficientes fila por fila.")
    for i in range(n):
        fila = []
        for j in range(n):
            fila.append(_leer_float(f"A[{i + 1},{j + 1}]: "))
        matriz.append(fila)
        vector.append(_leer_float(f"b[{i + 1}]: "))
    resultado = eliminacion_gauss(matriz, vector)
    print("Solucion:", resultado.solucion)
    print("Residuo:", resultado.residuo)


def main() -> None:
    while True:
        print("\n==============================")
        print("Laboratorio de Modelado y Simulacion")
        print("==============================")
        print("1) Busqueda de raices")
        print("2) Integracion numerica")
        print("3) Interpolacion")
        print("4) EDO")
        print("5) Sistemas lineales")
        print("0) Salir")
        opcion = input("Selecciona una opcion: ").strip()
        try:
            if opcion == "1":
                _resolver_raices()
            elif opcion == "2":
                _resolver_integracion()
            elif opcion == "3":
                _resolver_interpolacion()
            elif opcion == "4":
                _resolver_edo()
            elif opcion == "5":
                _resolver_sistema_lineal()
            elif opcion == "0":
                break
            else:
                print("Opcion invalida.")
        except Exception as exc:  # noqa: BLE001
            print(f"Error: {exc}")
