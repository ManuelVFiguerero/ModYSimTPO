# Arquitectura del laboratorio

## Capas principales

### 1. Motor numerico
Ubicado en `core/metodos_numericos/`.

Responsabilidades:

- implementar algoritmos numericos
- validar entradas
- devolver resultados estructurados
- evitar dependencias de UI

### 2. Utilidades compartidas
Ubicadas en `core/utils/`.

Incluyen:

- parser seguro de funciones con SymPy
- validaciones
- metricas de error
- modelos de resultados
- errores de dominio

### 3. Simuladores
Ubicados en `simuladores/`.

Incluyen:

- `consola_app.py`: interfaz por terminal
- `streamlit_app.py`: interfaz interactiva web
- `notebook_helpers.py`: acceso directo para notebooks

### 4. Visualizacion
Ubicada en `visualizacion/`.

Responsabilidades:

- graficos de convergencia
- trayectorias de EDO
- integrandos
- histogramas Monte Carlo

### 5. Casos de estudio
Ubicados en `casos/`.

Responsabilidades:

- centralizar presets de TP
- ofrecer ejemplos aplicados
- facilitar reutilizacion desde la app

## Flujo general

1. El usuario ingresa parametros desde consola, Streamlit o notebook.
2. La interfaz invoca funciones del `core`.
3. El parser transforma expresiones textuales en funciones evaluables.
4. El metodo numerico ejecuta validaciones y devuelve un resultado estructurado.
5. La capa de visualizacion representa tablas y graficos a partir de ese resultado.

## Compatibilidad heredada

`modelos.py` se mantiene como adaptador para el codigo existente. Esto permite migracion progresiva sin romper la experiencia previa del repositorio.
