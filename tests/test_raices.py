from core.metodos_numericos.raices import biseccion, newton_raphson, punto_fijo


def test_biseccion_cos_x():
    resultado = biseccion("cos(x) - x", 0.0, 1.0, 1e-8, 200)
    assert resultado.convergio is True
    assert abs(resultado.aproximacion - 0.7390851332) < 1e-6


def test_newton_derivada_automatica():
    resultado = newton_raphson("x**2 - 2", 1.0, None, 1e-10, 50)
    assert resultado.convergio is True
    assert abs(resultado.aproximacion - 2 ** 0.5) < 1e-8


def test_punto_fijo_cos():
    resultado = punto_fijo("cos(x)", 0.5, 1e-8, 200)
    assert abs(resultado.aproximacion - 0.7390851332) < 1e-6
