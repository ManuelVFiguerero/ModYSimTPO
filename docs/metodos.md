# Metodos implementados

## Raices

### Biseccion
- Entradas: `f_expr`, `a`, `b`, `tolerancia`, `max_iter`
- Salidas: `RootResult`
- Incluye: aproximacion final, iteraciones, error absoluto y datos del intervalo

### Punto fijo
- Entradas: `g_expr`, `x0`, `tolerancia`, `max_iter`
- Salidas: `RootResult`

### Newton-Raphson
- Entradas: `f_expr`, `x0`, `df_expr` opcional, `tolerancia`, `max_iter`
- Salidas: `RootResult`
- Si no se provee derivada, se deriva simbolicamente

## Interpolacion

### Lagrange
- Entradas: lista de puntos y `x_eval`
- Salidas: `InterpolationResult`
- Incluye polinomio interpolante como metadato

## Integracion

### Trapecio compuesto
### Simpson 1/3 compuesto
### Simpson 3/8 compuesto
### Rectangulo medio compuesto
### Gauss-Legendre

- Entradas tipicas: `f_expr`, `a`, `b`, `n` u `orden`
- Salidas: `IntegrationResult`
- Incluye muestras, pesos y errores si se provee valor exacto

## Monte Carlo

### Integral Monte Carlo
- Entradas: `f_expr`, `a`, `b`, `n`, `confianza`, `seed`
- Salidas: `MonteCarloResult`

### Estimacion geometrica de pi
- Entradas: `n`, `seed`
- Salidas: `MonteCarloResult`

## EDO

### Euler
### Heun
### RK4

- Entradas: `ode_expr`, `t0`, `y0`, `h`, `pasos`, `solucion_exacta_expr` opcional
- Salidas: `ODEResult`

## Sistemas lineales

### Eliminacion de Gauss
- Entradas: matriz cuadrada `A` y vector `b`
- Salidas: `LinearSystemResult`
