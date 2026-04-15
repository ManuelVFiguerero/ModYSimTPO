"""Casos aplicados para mostrar reutilizacion del laboratorio."""

APPLIED_CASES = {
    "ingenieria_enfriamiento": {
        "metodo": "heun",
        "titulo": "Propagacion del calor de una hornalla",
        "descripcion": "Simula como la temperatura de una olla se acerca a la del ambiente.",
        "parametros": {
            "ode_expr": "-0.3*(y-20)",
            "t0": 0.0,
            "y0": 90.0,
            "h": 0.5,
            "pasos": 12,
            "k": 0.3,
            "temperatura_ambiente": 20.0,
        },
    },
    "datos_integral_gaussiana": {
        "metodo": "montecarlo_integral",
        "titulo": "Integral de exp(-x**2) para analisis de datos",
        "descripcion": "Caso estocastico util en probabilidad y ML.",
        "parametros": {"f_expr": "exp(-x**2)", "a": 0.0, "b": 1.0, "n": 5000, "confianza": 0.95, "seed": 42},
    },
}
