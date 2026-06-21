"""Ejercicio 05: Optimización de carga de camiones
    Un centro de distribución tiene registrados los pesos de carga (kg) de los camiones, ordenados 
    de menor a mayor. Cada camión tiene un número de flota. El sistema debe encontrar un camión con
    peso exacto para balancear la flota.

    Datos: Lista de tuplas (nro_flota, peso_carga) ordenada por peso.
    Entrada: Peso objetivo.
    Salida: Número de float y peso, o mensaje de "no encontrado". """

def buscar_camion(camiones: list[tuple[str, int]], peso_objetivo: int):
    """
        Busca un camión por peso de carga usando búsqueda binaria.

        Args:
            Camiones: Lista de tuplas (nro_flota, peso) ordenada por peso
            peso_objetivo: Peso en kg a buscar

        Returns: 
            Tupla (nro_flota, peso) o None si no existe
    """

    izquierda = 0
    derecha = len(camiones) - 1

    while izquierda <= derecha:
        medio = izquierda + (derecha - izquierda) // 2
        peso_actual = camiones[medio][1] # Segundo elemento de la tupla

        if peso_actual == peso_objetivo:
            return camiones[medio]
        elif peso_actual < peso_objetivo:
            izquierda = medio + 1
        else:
            derecha = medio - 1

    return None

# Prueba
camiones = [("F101", 1200), ("F203", 1450), ("F312", 1800), ("F425", 2100), ("F538", 2500)]

# Caso 1: encontrado
resultado = buscar_camion(camiones, 1800)
if resultado:
    print(f"Camión {resultado[0]} con {resultado[1]} kg")
else:
    print("No hay camión con peso 1800 kg")

# Caso 2: No encontrado
resultado = buscar_camion(camiones, 1950)
if resultado:
    print(f"Camión {resultado[0]} con {resultado[1]} kg")
else:
    print("No hay camión con peso 1950 kg")
