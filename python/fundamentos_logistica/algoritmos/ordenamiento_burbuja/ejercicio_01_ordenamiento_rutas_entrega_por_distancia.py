"""Ejercicio 01: Ordenamiento de Rutas de Entrega por Distacia

    Una empresa de mensajería tiene una lista de rutas de entrega con sus respectivas
    distancias en kilómetros. Necesitan ordenar las rutas de menor a mayor distancia
    para optimizar el consumo de combustible. """

def ordenar_rutas_distancia(rutas: list[tuple[str, float]]):
    """
        Ordena una lista de tuplas (nombre_ruta, distancia) por distancia ascendente
        usando el algoritmo de burbuja """

    n = len(rutas)

    for i in range(n - 1):
        # Bandera de optimización: Si no hay intercambios, la lista ya está ordenada
        intercambiado = False

        for j in range(0, n - i - 1):
            # Comparamos las disntacias
            if rutas[j][1] > rutas[j + 1][1]:
                # Intercambiamos las tuplas completas
                rutas[j], rutas[j + 1] = rutas[j + 1], rutas[j]

                intercambiado = True

        # Si no hubo intercambio
        if not intercambiado:
            break

    return rutas

# Prueba:

rutas = [("Ruta Norte", 45.3), ("Ruta Sur", 32.1), ("Ruta Este", 67.8), ("Ruta Oeste", 23.5), ("Ruta Centro", 54.2)]

rutas_ordenadas = ordenar_rutas_distancia(rutas)
print("\nLista ordenada por distancia: ")
print(rutas_ordenadas)
