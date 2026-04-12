from core.metodos_numericos.edo import euler, heun, runge_kutta_4


def test_rk4_exp():
    resultado = runge_kutta_4("y", 0.0, 1.0, 0.1, 10, "exp(t)")
    assert abs(resultado.pasos[-1].y - 2.718281828) < 1e-4


def test_euler_and_heun_run():
    resultado_euler = euler("y", 0.0, 1.0, 0.1, 5, "exp(t)")
    resultado_heun = heun("y", 0.0, 1.0, 0.1, 5, "exp(t)")
    assert len(resultado_euler.pasos) == 6
    assert len(resultado_heun.pasos) == 6
