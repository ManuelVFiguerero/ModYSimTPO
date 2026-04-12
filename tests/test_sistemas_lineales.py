from core.metodos_numericos.sistemas_lineales import eliminacion_gauss


def test_eliminacion_gauss():
    resultado = eliminacion_gauss([[2.0, 1.0], [1.0, 3.0]], [1.0, 2.0])
    x1, x2 = resultado.solucion
    assert abs(x1 - 0.2) < 1e-10
    assert abs(x2 - 0.6) < 1e-10
