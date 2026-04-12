"""Excepciones de dominio para el laboratorio numerico."""


class LaboratorioError(Exception):
    """Excepcion base del laboratorio."""


class ValidationError(LaboratorioError):
    """Error de validacion de parametros de entrada."""


class ExpressionParseError(LaboratorioError):
    """Error de parseo o evaluacion de expresiones matematicas."""


class ConvergenceError(LaboratorioError):
    """Error asociado a falta de convergencia o configuracion invalida."""
