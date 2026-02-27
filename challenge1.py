# JUEGO: GATO vs RATÓN con MINIMAX 
# FUNCIÓN PARA MOSTRAR EL TABLERO

def mostrar(tablero):
    for fila in tablero:                # Recorre cada fila del tablero
        print("".join(fila))            # Imprime la fila como texto continuo

# MOVIMIENTOS POSIBLES (arriba/abajo/izq/der)
def movimientos(x, y, dimension):
    movs = []                           # Lista donde guardamos movimientos válidos
    direcciones = [(-1,0),(1,0),(0,-1),(0,1)]  # Movimientos: arriba, abajo, izq, der

    for dx, dy in direcciones:          # Recorre las 4 direcciones
        nx = x + dx                     # comprueba nueva fila
        ny = y + dy                     # comprueba nueva columna

        if 0 <= nx < dimension and 0 <= ny < dimension: 
            # el 0 es el limite minimio del tablero
            # # Verifica que NO salga del tablero
            movs.append((nx, ny))       # Agrega el movimiento válido

    return movs                         # Devuelve lista de movimientos permitidos

# DISTANCIA MANHATTAN
def dist(a, b):                         # a y b son posiciones del tablero expresadas como tuplas (fila, columna)
# abs(a[0] - b[0]) = distancia vertical entre las posiciones
# abs(a[1] - b[1]) = distancia horizontal entre las posiciones
# cualcula la distancia entre dos posiciones del tablero
    return abs(a[0] - b[0]) + abs(a[1] - b[1])   # Suma de diferencias absolutas
# el 0 es x y el 1 es y 

# ESTADOS FINALES (GANAR / PERDER)
def terminal(g, r, salida):
    if g == r:                          # Si el gato está en la misma casilla que el ratón
        return True, -1000              # Ratón pierde
    if r == salida:                     # Si el ratón llegó a la salida
        return True, 1000               # Ratón gana
    return False, 0                     # Si nada de eso pasó, el juego sigue


# HEURÍSTICA (para profundidad 0)
# la heurística es una fórmula que estima qué tan bueno es un estado cuando ya no seguimos recursións
def evaluar(g, r, salida):
    return 2 * dist(g, r) - 3 * dist(r, salida)
    # 2 * distancia entre gato y ratón → queremos que sea GRANDE (gato lejos)
    # 3 * distancia ratón-salida → queremos que sea PEQUEÑA (ratón cerca)


# MINIMAX
# recursividad = es el minimax 
#recursidad: es cuando una función se llama a sí misma para resolver un problema..
def minimax(g, r, salida, depth, es_turno_raton, dim):
    """
    Esta función simula jugadas del futuro.

    - Si es turno del ratón (MAX) → busca beneficios para él.
    - Si es turno del gato  (MIN) → busca perjudicar al ratón.
    depth = profundidad de busqueda
    depth = significa cuántos pasos hacia adelante piensa
    """

    fin, valor = terminal(g, r, salida)     # 1) Ver si el juego terminó
    if fin:
        return valor, None                  # Si termina, no hay movimiento

    if depth == 0:                          # 2) Si profundidad llegó a 0
        return evaluar(g, r, salida), None  #   devolvemos la heurística


    # TURNO DEL RATÓN (MAX) 
    if es_turno_raton:
        mejor_val = float("-inf")           # Queremos el MAYOR valor posible.. el gato esta lejos 
        mejor_mov = None                    
        
        for nx, ny in movimientos(r[0], r[1], dim):  # Simula movimientos del ratón
            val, _ = minimax(g, (nx, ny), salida, depth-1, False, dim) # depth-1 se usa para que cada vez baje un nivel
            # es recursividad 
            if val > mejor_val:             # Si la jugada mejora el estado
                mejor_val = val             # Guardamos mejor valor
                mejor_mov = (nx, ny)        # Guardamos mejor movimiento

        return mejor_val, mejor_mov         # Devuelve mejor mov. del ratón SIMULADO


    # TURNO DEL GATO (MIN) 
    else:
        peor_val = float("inf")             # El raton esta lejos de la salida.
        mejor_mov = None

        for nx, ny in movimientos(g[0], g[1], dim):  # Simula movimientos del gato
            val, _ = minimax((nx, ny), r, salida, depth-1, True, dim)

            if val < peor_val:              # Si el valor es peor para el ratón
                peor_val = val              # El gato lo prefiere
                mejor_mov = (nx, ny)        # Guarda el movimiento elegido

        return peor_val, mejor_mov          # Devuelve el movimiento real del gato


# CONTROL REAL DEL RATÓN (el jugador)
def mover_raton(r, dim):
    teclas = {"w": (-1,0), "s": (1,0), "a": (0,-1), "d": (0,1)}  # Mapa de movimientos
    while True:
        tecla = input("Mover ratón (W/A/S/D): ").lower()         # Espera entrada del jugador

        if tecla not in teclas:                                  # Entrada inválida
            print("Tecla inválida.")
            continue
        # asigno nueva posicion de mi raton
        dx, dc = teclas[tecla]                                   # Obtiene desplazamiento
        nr = r[0] + dx                                           # Nueva fila
        nc = r[1] + dc                                            # Nueva columna

        if 0 <= nr < dim and 0 <= nc < dim:                      # Verifica que no salga
            return (nr, nc)                                      # Devuelve nueva posición

        print("No puedes salir del tablero.")                    # Error si intenta salir

# BUCLE PRINCIPAL DEL JUEGO
def main():
    dim = 8                                                      # Tamaño del tablero
    # lista de listas = matriz
    tablero = [["🔲" for _ in range(dim)] for _ in range(dim)]   # Tablero vacío
    #El primer for _ in range(dim) → crea una fila de dim elementos "🔲"
    #El segundo for _ in range(dim) → repite eso dim veces para crear todas las filas
    gato = (0, 0)                                                # Posición inicial del gato
    raton = (7, 7)                                               # Posición inicial del ratón
    salida = (0, 7)                                              # Posición de la salida

    tablero[gato[0]][gato[1]] = "🐱"                             # Coloca gato
    tablero[raton[0]][raton[1]] = "🐭"                           # Coloca ratón
    tablero[salida[0]][salida[1]] = "🚪"                         # Coloca salida

    print("\n RATÓN vs GATO con MINIMAX \n")

    while True:                                                  # Bucle del juego
        mostrar(tablero)                                         # Muestra tablero
        print()

        # COMPRUEBA SI EL JUEGO TERMINÓ
        if raton == salida:
            print("¡El ratón llegó a la salida! 🚪🐭")
            break

        if gato == raton:
            print("¡El gato atrapó al ratón! 🐱💀")
            break

        
        # TURNO REAL DEL RATÓN (jugador)
        tablero[raton[0]][raton[1]] = "🔲"                       # Limpia casilla anterior
        raton = mover_raton(raton, dim)                          # Usuario mueve
        tablero[raton[0]][raton[1]] = "🐭"                       # Pone ratón en nuevo lugar

        if raton == salida:
            mostrar(tablero)
            print("¡Victoria del ratón!")
            break

        # TURNO DEL GATO (IA MINIMAX)
        tablero[gato[0]][gato[1]] = "🔲"                         # Limpia posición anterior
        # la raiz 
        _, mov = minimax(gato, raton, salida, 3, False, dim)
        # _ para ignorar
        if mov:                                                  # Si MINIMAX devolvió movimiento
            gato = mov                                           # Se mueve el gato

        tablero[gato[0]][gato[1]] = "🐱"                         # Coloca gato en nuevo lugar

        if gato == raton:
            mostrar(tablero)
            print("¡El gato te atrapó!")
            break

# para que se ejecute mi archivo main directamente 
# Porque Python necesita una forma de decidir si un archivo se debe ejecutar directamente o no.
if __name__ == "__main__":
    main()
