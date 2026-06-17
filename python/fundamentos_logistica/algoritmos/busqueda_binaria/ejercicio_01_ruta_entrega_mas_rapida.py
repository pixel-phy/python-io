"""Ejercicio 01: Ruta de entrega más rápida
    
    Una empresa de mensajería tiene registrados los tiempos de entrega (en minutos) para diferentes
    rutas, ordenados de menor a mayor. Cada ruta tiene un ID único. El sistema necesita encontrar
    rápidamente si existe una ruta con un tiempo de entrega específico para asignar pedidos urgentes.

    Datos: Lista de tuplas (id_ruta, tiempo_minutos) ordenada por tiempo.
    Entrada: Tiempo objetivo en minutos.
    Salida: ID de la ruta y su tiempo, o mensaje de "no encontrado". """

def buscar_ruta(rutas: list[tuple[str, float]], tiempo_objetivo: float):
    """
        Busca una ruta por tiempo de entrega usando búsqueda binaria iterativa.

        Args:
            rutas: Lista de tuplas (id, tiempo) ordenada por tiempo
            tiempo_objetivo: Tiempo en minutos a buscar

        Returns:
            Tupla (id, tiempo) o None si no se encuentra
    """

    izquierda = 0
    derecha = len(rutas) - 1

    while izquierda <= derecha:
        medio = izquierda + (derecha - izquierda) // 2
        tiempo_actual = rutas[medio][1] # Se extrae el tiempo de la tupla

        if tiempo_actual == tiempo_objetivo:
            return rutas[medio] # Se devuelve la tupla completa
        elif tiempo_actual < tiempo_objetivo:
            izquierda = medio + 1 # Busca en mitad derecha
        else:
            derecha = medio - 1 # Busca en mitad izquierda

    return None

# Pruebas:
rutas = [(101, 15), (102, 23), (103, 31), (104, 42), (105, 58)]

# Caso 1: encontrado
resultado = buscar_ruta(rutas, 42)
if resultado:
    print(f"Ruta {resultado[0]} -> {resultado[1]} minutos")
else:
    print("No existe ruta con ese tiempo")

# Caso 2: No encontrado
resultado = buscar_ruta(rutas, 37)
if resultado:
    print(f"Ruta {resultado[0]} -> {resultado[1]} minutos")
else:
    print("No existe ruta con tiempo 37 minutos")
