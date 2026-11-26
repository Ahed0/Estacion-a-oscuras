# Estación a oscuras

Juego de estrategia por turnos desarrollado en Python. El objetivo es recoger dos fusibles y alcanzar la salida de una estación sin agotar la batería ni ser atrapado por un dron.

## Características

- Tablero de 6 × 6 con diez paredes generadas aleatoriamente.
- Dos fusibles y una salida en posiciones aleatorias.
- Patrulla del dron de entre seis y nueve casillas diferentes.
- Batería inicial de 30 unidades.
- Validación de los mapas mediante búsqueda en anchura (BFS).

## Cómo jugar

El jugador comienza en la casilla (0, 0) y el dron en (5, 5). Cada movimiento válido consume una unidad de batería y hace avanzar al dron. Los movimientos bloqueados o las entradas incorrectas no consumen batería.

La salida permanece bloqueada hasta recoger ambos fusibles. El jugador gana al llegar a ella y pierde si coincide con el dron o agota la batería antes de escapar.

### Controles

| Tecla | Acción |
| --- | --- |
| W | Arriba |
| A | Izquierda |
| S | Abajo |
| D | Derecha |
| Q | Salir de la partida |

### Símbolos

| Símbolo | Significado |
| --- | --- |
| `p` | Jugador |
| `d` | Dron |
| `F` | Fusible |
| `S` | Salida |
| `#` | Pared |
| `.` | Casilla libre |

## Requisitos y ejecución

Se necesita Python 3. El proyecto utiliza únicamente módulos de la biblioteca estándar (`random` y `collections`).

Descarga el archivo `estacion_a_oscuras.py`, abre una terminal en su carpeta y ejecuta el siguiente comando en Windows:

```cmd
py estacion_a_oscuras.py
```

En Linux o macOS:

```bash
python3 estacion_a_oscuras.py
```

## Funcionamiento del programa

El tablero se representa mediante una lista de listas y las posiciones mediante tuplas de coordenadas (fila, columna).

La función `generar_tablero()` coloca las paredes, los fusibles y la salida utilizando `random.sample()`. La función `generar_ruta()` selecciona movimientos válidos del dron mediante `random.choice()` y construye un recorrido de ida y vuelta.

La función `mapa_valido()` utiliza BFS (búsqueda en anchura) para comprobar si existe un camino hasta la salida con los dos fusibles y un máximo de 30 movimientos. La búsqueda utiliza una cola (`deque`), un conjunto de estados visitados y dos variables booleanas para registrar los fusibles recogidos. Durante esta validación se evitan las casillas de la patrulla, lo que garantiza al menos una ruta segura. Si el mapa no es válido, se genera otro.

## Aprendizaje

Proyecto personal desarrollado para ampliar mis conocimientos de Python, practicar la programación modular, el uso de listas, tuplas, conjuntos y colas, la generación aleatoria de escenarios y los algoritmos de búsqueda.
## Autor

Álvaro Ahedo Sevilla
