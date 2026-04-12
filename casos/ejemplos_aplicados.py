"""Casos aplicados para mostrar reutilizacion del laboratorio."""

APPLIED_CASES = {
    "ingenieria_enfriamiento": {
        "metodo": "heun",
        "titulo": "Modelo simple de enfriamiento",
        "descripcion": "Aproxima una ley de enfriamiento linealizada.",
        "parametros": {"ode_expr": "-0.3*(y-20)", "t0": 0.0, "y0": 90.0, "h": 0.5, "pasos": 12},
    },
    "datos_integral_gaussiana": {
        "metodo": "montecarlo_integral",
        "titulo": "Integral de exp(-x**2) para analisis de datos",
        "descripcion": "Caso estocastico util en probabilidad y ML.",
        "parametros": {"f_expr": "exp(-x**2)", "a": 0.0, "b": 1.0, "n": 5000, "confianza": 0.95, "seed": 42},
    },
}
