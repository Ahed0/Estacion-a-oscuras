import random
from collections import deque

BATERIA_INICIAL = 30


def main():
    tablero, ruta_dron, salida = generar_tablero()
    p_coordenada = (0, 0)
    d_coordenada = (5, 5)
    indice_dron = 0
    fusible_recogidos = 0
    bat = BATERIA_INICIAL

    while True:
        mostrar_tab(tablero, p_coordenada, d_coordenada)
        print(f"Batería: {bat} | Fusibles: {fusible_recogidos}/2")
        tecla = input("W, A, S, D para moverte. Q para salir: ").strip().upper()

        if tecla == "Q":
            break

        destino = calc_destino(p_coordenada, tecla)

        if destino == salida and fusible_recogidos < 2:
            print("Obtén los dos fusibles. Salida bloqueada.")
            continue

        if destino != p_coordenada and casilla_libre(tablero, destino):
            p_coordenada = destino
            bat = bateria(bat)

            if perder(p_coordenada, d_coordenada):
                print("¡El dron te ha atrapado!")
                break

            if recoger_fusible(tablero, p_coordenada):
                fusible_recogidos += 1
                print(f"Fusibles recogidos: {fusible_recogidos}/2")

            d_coordenada, indice_dron = mover_dron(ruta_dron, indice_dron)

            if perder(p_coordenada, d_coordenada):
                print("¡El dron te ha atrapado!")
                break

            if ganar(tablero, p_coordenada, fusible_recogidos):
                print("¡GANASTE!")
                break

            if bat == 0:
                print("¡Te quedaste sin batería!")
                break


def generar_tablero():
    inicio = (0, 0)
    inicio_dron = (5, 5)

    while True:
        tablero = []
        posiciones = []

        # Crear el tablero y reunir las posiciones donde podemos colocar paredes.
        for fila in range(6):
            nueva_fila = []
            for col in range(6):
                nueva_fila.append(".")
                coordenada = (fila, col)
                if coordenada != inicio and coordenada != inicio_dron:
                    posiciones.append(coordenada)
            tablero.append(nueva_fila)

        for fila, col in random.sample(posiciones, 10):
            tablero[fila][col] = "#"

        ruta_dron = generar_ruta(tablero, inicio_dron)

        if len(set(ruta_dron)) < 6:
            continue

        disponibles = []
        for posicion in posiciones:
            if casilla_libre(tablero, posicion) and posicion not in ruta_dron:
                disponibles.append(posicion)

        fusible1, fusible2, salida = random.sample(disponibles, 3)

        for fila, col in (fusible1, fusible2):
            tablero[fila][col] = "F"

        fila, col = salida
        tablero[fila][col] = "S"

        if mapa_valido(tablero, inicio, salida, ruta_dron, fusible1, fusible2):
            return tablero, ruta_dron, salida


def generar_ruta(tablero, inicio):
    ruta = [inicio]
    numero_pasos = random.randint(5, 8)
    posicion_actual = inicio

    for paso in range(numero_pasos):
        disponibles = []
        for tecla in "WASD":
            destino = calc_destino(posicion_actual, tecla)
            if destino != (0, 0) and destino not in ruta and casilla_libre(tablero, destino):
                disponibles.append(destino)

        if not disponibles:
            break

        posicion_actual = random.choice(disponibles)
        ruta.append(posicion_actual)

    # Añadir el recorrido de vuelta sin repetir los extremos.
    for indice in range(len(ruta) - 2, 0, -1):
        ruta.append(ruta[indice])

    return ruta


def mapa_valido(tablero, inicio, salida, ruta_dron, fusible1, fusible2):
    pendientes = deque()
    pendientes.append((inicio, False, False, 0))

    visitados = set()
    visitados.add((inicio, False, False))

    while pendientes:
        posicion, tiene_fusible1, tiene_fusible2, pasos = pendientes.popleft()

        if posicion == salida and tiene_fusible1 and tiene_fusible2:
            return True

        if pasos == BATERIA_INICIAL:
            continue

        for tecla in "WASD":
            destino = calc_destino(posicion, tecla)

            if not casilla_libre(tablero, destino) or destino in ruta_dron:
                continue

            if destino == salida and not (tiene_fusible1 and tiene_fusible2):
                continue

            nuevo_fusible1 = tiene_fusible1
            nuevo_fusible2 = tiene_fusible2

            if destino == fusible1:
                nuevo_fusible1 = True
            if destino == fusible2:
                nuevo_fusible2 = True

            estado = (destino, nuevo_fusible1, nuevo_fusible2)
            if estado not in visitados:
                visitados.add(estado)
                pendientes.append((destino, nuevo_fusible1, nuevo_fusible2, pasos + 1))

    return False


def recoger_fusible(tablero, p_coordenada):
    fila, col = p_coordenada
    if tablero[fila][col] == "F":
        tablero[fila][col] = "."
        return True
    return False


def mover_dron(ruta_dron, indice_dron):
    indice_dron = (indice_dron + 1) % len(ruta_dron)
    return ruta_dron[indice_dron], indice_dron


def mostrar_tab(tablero, p_coordenada, d_coordenada):
    for fila in range(len(tablero)):
        for col in range(len(tablero[fila])):
            if (fila, col) == p_coordenada:
                print("p", end="")
            elif (fila, col) == d_coordenada:
                print("d", end="")
            else:
                print(tablero[fila][col], end="")
        print()


def calc_destino(p_coordenada, tecla):
    fila, col = p_coordenada
    destino = p_coordenada

    if tecla == "W":
        destino = (fila - 1, col)
    elif tecla == "S":
        destino = (fila + 1, col)
    elif tecla == "A":
        destino = (fila, col - 1)
    elif tecla == "D":
        destino = (fila, col + 1)

    return destino


def bateria(bat):
    bat -= 1
    print(f"Batería restante: {bat}.")
    return bat


def muro(tablero, destino):
    fila, col = destino
    return tablero[fila][col] == "#"


def en_tablero(coordenada):
    fila, col = coordenada
    return 0 <= fila < 6 and 0 <= col < 6


def ganar(tablero, p_coordenada, fusible_recogidos):
    fila, col = p_coordenada
    return tablero[fila][col] == "S" and fusible_recogidos == 2


def perder(p_coordenada, d_coordenada):
    return p_coordenada == d_coordenada


def casilla_libre(tablero, destino):
    return en_tablero(destino) and not muro(tablero, destino)


if __name__ == "__main__":
    main()
