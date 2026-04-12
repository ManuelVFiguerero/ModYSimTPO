from core.metodos_numericos.monte_carlo import estimar_pi_geometrico, integracion_montecarlo


def test_integracion_montecarlo_constante():
    resultado = integracion_montecarlo("2", 0.0, 3.0, 2000, seed=42)
    assert abs(resultado.estimacion - 6.0) < 1e-9


def test_estimacion_pi_geometrico():
    resultado = estimar_pi_geometrico(20000, seed=42)
    assert abs(resultado.estimacion - 3.14159) < 0.08
