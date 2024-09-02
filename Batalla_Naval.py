import os
import random

# Aqui se Crea un tablero de 5x5.
def crear_tablero():
    return [['▩' for _ in range(5)] for _ in range(5)]

# Aqui se Muestra el tablero con estadísticas al lado.
def mostrar_tablero_con_estadisticas(tablero, barcos_hundidos, disparos_realizados, mostrar_barcos=False):
    print("    0   1   2   3   4")
    for i, fila in enumerate(tablero):
        fila_mostrar = []
        for celda in fila:
            if not mostrar_barcos and celda == 'B':
                fila_mostrar.append('▩')
            else:
                fila_mostrar.append(celda)
        print(f"{i}   {'   '.join(fila_mostrar)}")
    
    print("\n                       ➤ ESTADISTICAS:")
    print(f"                        Barcos Hundidos ➣ {barcos_hundidos}")
    print(f"                        Disparos Realizados ➣ {disparos_realizados}")

# Aqui se Coloca el barco en una posición dada.
def colocar_barco(tablero, barco, posicion, direccion):
    x, y = posicion
    if direccion == 'PORTAVIONES':
        if y + barco > 5:
            return False
        for i in range(barco):
            if tablero[x][y + i] != '▩':
                return False
        for i in range(barco):
            tablero[x][y + i] = 'B'
    elif direccion == 'SUBMARINO':
        if x + barco > 5:
            return False
        for i in range(barco):
            if tablero[x + i][y] != '▩':
                return False
        for i in range(barco):
            tablero[x + i][y] = 'B'
    return True

# Aqui es una funciom para Realizar el disparo y actualiza el resultado en el tablero.
def disparar(tablero, posicion):
    x, y = posicion
    if tablero[x][y] == 'B':
        tablero[x][y] = '✷' 
        return "\nEl disparo fue ¡Impacto! 💥"  # Marca el impacto
    elif tablero[x][y] == '▩':
        tablero[x][y] = '🌢'  # Marca el agua
        return "¡El disparo fue Agua! 💧"
    else:
        return " ⚠ ¡Ya disparaste aquí! ⚠."

# Verifica si todos los barcos fueron hundidos.
def verificar_victoria(tablero):
    return not any('B' in fila for fila in tablero)

# Coloca los barcos aleatoriamente en el tablero de la computadora.
def colocar_barcos_aleatorios(tablero):
    barcos = [(3, 'PORTAVIONES'), (2, 'SUBMARINO')]  # Portaaviones y Submarino
    for barco, direccion in barcos:
        colocado = False
        while not colocado:
            x = random.randint(0, 4)
            y = random.randint(0, 4)
            if direccion == 'PORTAVIONES':
                if y + barco <= 5:
                    colocado = colocar_barco(tablero, barco, (x, y), direccion)
            else:  # dirección es 'SUBMARINO'
                if x + barco <= 5:
                    colocado = colocar_barco(tablero, barco, (x, y), direccion)

# Pregunta al usuario si desea volver al menú
def verificar_volver_menu():
    print()
    respuesta = input("¿Quieres volver al menú principal? (s/n): ").strip().lower()
    return respuesta == 's'

# Pregunta al usuario si desea jugar de nuevo
def jugar_de_nuevo():
    print()
    respuesta = input("¿Quieres jugar de nuevo? (s/n): ").strip().lower()
    return respuesta == 's'

# Maneja el turno de un jugador.
def jugar_turno(tablero_oponente, tablero_jugador, barcos_hundidos, disparos_realizados):
    """Maneja el turno de un jugador."""
    mostrar_tablero_con_estadisticas(tablero_oponente, barcos_hundidos, disparos_realizados, mostrar_barcos=False)
    
    while True:
        try:
            print("------------------------------------------------------")
            x = int(input("Ingresa la coordenada x para Atacar (0-4) ➣ "))
            y = int(input("Ingresa la coordenada y para Atacar (0-4) ➣ "))
            print()
            if not (0 <= x < 5 and 0 <= y < 5):
                print("⚠ Coordenadas fuera de rango. ¡Intenta de nuevo! ⚠.")
                continue
        except ValueError:
            print("⚠ Entrada inválida. ¡Intenta de nuevo! ⚠.")
            continue
        
        resultado = disparar(tablero_oponente, (x, y))
        print(resultado)
        disparos_realizados += 1
        if resultado == "¡Impacto!":
            barcos_hundidos += 1
        if verificar_victoria(tablero_oponente):
            return True, barcos_hundidos, disparos_realizados
        return False, barcos_hundidos, disparos_realizados

# Función para jugar contra la máquina.
def jugar_contra_maquina():
    while True:
        os.system("cls")
        print()
        print("**************************************")
        print("¡Bienvenido al juego de Batalla Naval!")
        print("**************************************")
        print("----------jugador vs maquina----------")
        print()
        tablero_jugador = crear_tablero()
        tablero_computadora = crear_tablero()
        
        barcos_jugador_hundidos = 0
        disparos_jugador_realizados = 0
        
        barcos_computadora_hundidos = 0
        disparos_computadora_realizados = 0
        
        print("➤ Coloca tu Flota en el tablero ⚓ ! ")
        barcos = [(3,'PORTAVIONES'), (2,'SUBMARINO')]  # Portaaviones y Submarino
        for barco, direccion in barcos:
            colocado = False
            while not colocado:
                x = int(input(f"➤ Ingresa la coordenada x para el 🚢 de tamaño {barco} ({direccion}) ➣ "))
                y = int(input(f"➤ Ingresa la coordenada y para el 🚢 de tamaño {barco} ({direccion}) ➣ "))
                colocado = colocar_barco(tablero_jugador, barco, (x, y), direccion)
                if not colocado:
                    print("⚠ No se pudo colocar el barco. ¡Inténtalo de nuevo! ⚠.")
        
        colocar_barcos_aleatorios(tablero_computadora)

        while True:
            fin_juego, barcos_jugador_hundidos, disparos_jugador_realizados = jugar_turno(tablero_computadora, tablero_jugador, barcos_jugador_hundidos, disparos_jugador_realizados)
            if fin_juego:
                print("___________________")
                print("🎉 ¡Ganaste! 🎉")
                print("___________________")
                break
            print()
            print("Turno de la computadora...")
            x = random.randint(0, 4)
            y = random.randint(0, 4)
            resultado = disparar(tablero_jugador, (x, y))
            print(f"La Computadora Ataco en ({x}, {y}): {resultado}")
            disparos_computadora_realizados += 1
            mostrar_tablero_con_estadisticas(tablero_jugador, barcos_computadora_hundidos, disparos_computadora_realizados)
            if verificar_victoria(tablero_jugador):
                print("_____________________________")
                print("😡 ¡Perdiste! 😡")
                print("🎉 ¡La computadora ganó! 🎉")
                print("______________________________")
                break

        if not jugar_de_nuevo():
            return

# Función para jugar contra un amigo.
def jugar_contra_amigo():
    while True:
        os.system("cls")
        print()
        print("**************************************")
        print("¡Bienvenido al juego de Batalla Naval!")
        print("**************************************")
        print("----------jugador vs jugador----------")
        print()

        tablero_jugador1 = crear_tablero()
        tablero_jugador2 = crear_tablero()
        
        barcos_jugador1_hundidos = 0
        disparos_jugador1_realizados = 0
        
        barcos_jugador2_hundidos = 0
        disparos_jugador2_realizados = 0
        
        print("- Jugador 1, coloca tu flota en el tablero ⚓")
        barcos = [(3, 'PORTAVIONES'), (2, 'SUBMARINO')]  # Portaaviones y Submarino
        for barco, direccion in barcos:
            colocado = False
            while not colocado:
                x = int(input(f"➤ Ingrese la coordenada x para el barco de tamaño {barco} ({direccion}) ➣ "))
                y = int(input(f"➤ Ingrese la coordenada y para el barco de tamaño {barco} ({direccion}) ➣ "))
                colocado = colocar_barco(tablero_jugador1, barco, (x, y), direccion)
                if not colocado:
                    print("⚠ No se pudo colocar el barco. ¡Inténtalo de nuevo! ⚠.")
        
        os.system("cls")  # Limpia la pantalla para que el Jugador 2 no vea el tablero de Jugador 1
        print("- Jugador 2, coloca tu flota en el tablero ⚓")
        for barco, direccion in barcos:
            colocado = False
            while not colocado:
                x = int(input(f"➤ Ingrese la coordenada x para el barco de tamaño {barco} ({direccion}) ➣ "))
                y = int(input(f"➤ Ingrese la coordenada y para el barco de tamaño {barco} ({direccion}) ➣ "))
                colocado = colocar_barco(tablero_jugador2, barco, (x, y), direccion)
                if not colocado:
                    print("⚠ No se pudo colocar el barco. ¡Inténtalo de nuevo! ⚠.")
        
        turno = 1
        while True:
            if turno == 1:
                print()
                print("Turno del Jugador 1:")
                fin_juego, barcos_jugador2_hundidos, disparos_jugador1_realizados = jugar_turno(tablero_jugador2, tablero_jugador1, barcos_jugador2_hundidos, disparos_jugador1_realizados)
                if fin_juego:
                    print("_____________________________")
                    print("😡 ¡Perdiste! 😡")
                    print("🎉 ¡Jugador 1 ha ganado! 🎉")
                    print("_____________________________")
                    break
                turno = 2
            else:
                print()
                print("Turno del Jugador 2:")
                fin_juego, barcos_jugador1_hundidos, disparos_jugador2_realizados = jugar_turno(tablero_jugador1, tablero_jugador2, barcos_jugador1_hundidos, disparos_jugador2_realizados)
                if fin_juego:
                    print("_____________________________")
                    print("😡 ¡Perdiste! 😡")
                    print("🎉 ¡Jugador 2 ha ganado! 🎉")
                    print("_____________________________")
                    break
                turno = 1

        if not jugar_de_nuevo():
            return
        
# Función para mostrar las instrucciones del juego.
def mostrar_instrucciones():
    os.system("cls")  # Limpia la pantalla para que las instrucciones sean visibles.
    print("\n////////// BATALLA NAVAL //////////")
    print()
    print("---------- INSTRUCCIONES: ---------------------------------------------------------------------")
    print("| 1. El tablero es una cuadrícula de 5x5.                                                      |")
    print("| 2. Cada jugador coloca sus barcos en el tablero.                                             |")
    print("| 3. Cada barco ocupa un número específico de casillas. Portaviones 3 , Submarino 2            |")
    print("| 4. Los barcos pueden ser colocados vertical u horizontalmente.                               |")
    print("| 5. El objetivo es hundir todos los barcos del oponente antes de que ellos hundan los tuyos.  |")
    print("| 6. Los barcos se indican con 'B', los impactos con '✷' y el agua con '🌢'.                    |")
    print("| 7. ¡Buena suerte!                                                                            |")
    print("|______________________________________________________________________________________________|")
    input("¡ Presiona Enter para volver al menú principal !")


# Muestra el menú principal del juego y muestra las opciones de juego.
def menu_principal():
    while True:
        os.system("cls")  # Limpia la pantalla para una mejor experiencia de usuario.
        print("\n|///////// BATALLA NAVAL ////////|")
        print("|1. Jugar contra la máquina      |")
        print("|2. Jugar contra un amigo        |")
        print("|3. Ver instrucciones            |")
        print("|4. Salir                        |")
        print("|--------------------------------|")
        
        opcion = input("|- Selecciona una opción (1-4):  |\n|////////////////////////////////| ➣ ").strip()
        if opcion == '1':
            jugar_contra_maquina()
        elif opcion == '2':
            jugar_contra_amigo()
        elif opcion == '3':
            mostrar_instrucciones()
        elif opcion == '4':
            print("¡Gracias por jugar! ¡Hasta la próxima!")
            break
        else:
            print("⚠ Opción inválida. ¡Intenta de nuevo! ⚠")


# Ejecuta el menú principal.
if __name__ == "__main__":
    menu_principal()
