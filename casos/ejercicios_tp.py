"""Casos base alineados con ejercicios de trabajos practicos."""

ROOT_CASES = {
    "biseccion_cos": {
        "metodo": "biseccion",
        "titulo": "Raiz de sqrt(x) - cos(x)",
        "parametros": {"f_expr": "sqrt(x) - cos(x)", "a": 0.0, "b": 1.0, "tolerancia": 1e-6, "max_iter": 100},
    },
    "punto_fijo_cos": {
        "metodo": "punto_fijo",
        "titulo": "Punto fijo para cos(x) = x",
        "parametros": {"g_expr": "cos(x)", "x0": 0.5, "tolerancia": 1e-6, "max_iter": 100},
    },
    "newton_cubica": {
        "metodo": "newton_raphson",
        "titulo": "Newton para x^3 - 2x - 5",
        "parametros": {"f_expr": "x**3 - 2*x - 5", "df_expr": "3*x**2 - 2", "x0": 1.5, "tolerancia": 1e-6, "max_iter": 50},
    },
}

INTERPOLATION_CASES = {
    "lagrange_cuadratica": {
        "metodo": "lagrange",
        "titulo": "Interpolacion de nodos cuadraticos",
        "parametros": {"puntos": [(1.0, 1.0), (2.0, 4.0), (3.0, 9.0)], "x_eval": 1.5},
    }
}

INTEGRATION_CASES = {
    "simpson_sin": {
        "metodo": "simpson_13",
        "titulo": "Integral de sin(x) en [0, pi]",
        "parametros": {"f_expr": "sin(x)", "a": 0.0, "b": 3.141592653589793, "n": 10, "valor_exacto": 2.0},
    }
}

ODE_CASES = {
    "rk4_lineal": {
        "metodo": "rk4",
        "titulo": "PVI y' = y, y(0)=1",
        "parametros": {"ode_expr": "y", "t0": 0.0, "y0": 1.0, "h": 0.1, "pasos": 10, "solucion_exacta_expr": "exp(t)"},
    }
}
