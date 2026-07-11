"""Ejercicio 03: Fechas de caducidad en lote
    Un supermercado tiene un lote de productos perecederos con fechas de vencimiento 
    ordenadas (formato día del año, 1-365). Cada fecha tiene asociado el número de productos en ese lote.
    Se necesita encontrar un lote específico para retirarlo.

    Datos: Lista de listas [fecha, cantidad] ordenada por fecha.
    Entrada: Fecha a buscar (número día).
    Salida: Cantidad de productos en esa fecha, o mensaje si no existe. """

def buscar_lote(lotes: list[list], fecha_buscada: int):
    """
        Busca un lote por fecha de vencimiento usando búsqueda binaria.

        Args:
        lotes: Lista de listas [fecha, cantidad] ordenada por fecha
        fehca_buscada: Día del año a buscar (1-365)

    Returns: 
        Cantidad de productos o None si no existe
    """

    izquierda = 0
    derecha = len(lotes) - 1

    while izquierda <= derecha:
        medio = izquierda + (derecha - izquierda) // 2
        fecha_actual = lotes[medio][0] # Primer elemento de la sublista

        if fecha_actual == fecha_buscada:
            return lotes[medio][1] # Se devuelve la cantidad
        elif fecha_actual < fecha_buscada:
            izquierda = medio + 1
        else:
            derecha = medio - 1

    return None

# Prueba del ejercicio
lotes = [[15, 30], [32, 45], [47, 12], [63, 8], [78, 25]]

# Caso 1: Encontrado
cantidad = buscar_lote(lotes, 47)
if cantidad is not None:
    print(f"En fecha 47 hay {cantidad} productos")
else:
    print("No hay lote programado para fecha 47")

# Caso 2: No encontrado
cantidad = buscar_lote(lotes, 55)
if cantidad is not None:
    print(f"En fecha 55 hay {cantidad} productos")
else:
    print("No hay lote programado para fecha 55")

