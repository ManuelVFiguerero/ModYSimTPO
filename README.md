# Laboratorio de Modelado y Simulacion de Metodos Numericos

Repositorio Python orientado a metodos numericos, modelado y simulacion con un enfoque doble:

- academico: estudiar, comparar y visualizar metodos numericos
- tecnico: reutilizar el motor para problemas aplicados de ciencia, ingenieria y ciencia de datos

El proyecto evoluciono desde una base monolitica hacia una estructura modular con separacion entre:

- `core/`: motor numerico y utilidades compartidas
- `simuladores/`: interfaces de consola, Streamlit y helpers para notebooks
- `visualizacion/`: graficos reutilizables
- `casos/`: ejercicios de TP y ejemplos aplicados
- `docs/`: arquitectura, metodos y guias de uso
- `tests/`: pruebas basicas con `pytest`

## Metodos implementados

### Busqueda de raices
- Biseccion
- Punto fijo
- Newton-Raphson
- Aceleracion de Aitken

### Interpolacion y derivacion
- Interpolacion de Lagrange
- Diferencia central

### Integracion numerica
- Trapecio compuesto
- Simpson 1/3 compuesto
- Simpson 3/8 compuesto
- Rectangulo medio compuesto
- Cuadratura de Gauss-Legendre

### Simulacion estocastica
- Monte Carlo para integrales
- Monte Carlo geometrico para estimacion de pi

### EDO
- Euler
- Heun
- Runge-Kutta de orden 4

### Sistemas lineales
- Eliminacion de Gauss con pivoteo parcial

## Instalacion

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Ejecucion

### Consola

```bash
python app.py
```

### Streamlit

```bash
streamlit run web_app.py
```

## Estructura del proyecto

```text
core/
  metodos_numericos/
  utils/
simuladores/
visualizacion/
casos/
docs/
tests/
app.py
web_app.py
modelos.py
```

## Compatibilidad

`modelos.py` se conserva como fachada de compatibilidad para no romper el uso anterior del repositorio. La implementacion real vive ahora en `core/`.

## Stack tecnologico

- Python 3.10+
- Streamlit
- Plotly
- Pandas
- SymPy
- Pytest

## Documentacion adicional

- [Arquitectura](docs/arquitectura.md)
- [Metodos](docs/metodos.md)
- [Uso](docs/uso.md)
