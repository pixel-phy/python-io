""" Conservación de Flujo en Nodos (Transbordo)

En los modelos de optimización de redes (Network Flows), la restricción de conservación de flujo dicta 
que para cualquier nodo de transbordo (un centro de distribución intermedio), la cantidad total de 
mercancía que entra debe ser exactamente igual a la cantidad total que sale (no se puede crear ni destruir inventario allí).

    Escribir una función que reciba una lista de entradas de inventario y una lista de salidas para un nodo
específico. Retorna un diccionario indicando si la restricción de conservación de flujo se cumple,
el total de entradas, el total de salidas y la diferencia (residuo).

    Input de prueba: Entradas: [150, 200, 50], Salidas: [180, 220] """

def verificar_conservacion_flujo(entradas: list, salidas: list) -> dict:
    """
        verifica si se cumple la restricción de conservadción de flujo en un nodo.

        Args:
            entradas (list): Lista de cantidades que entran al nodo
            salidas (list): Lista de cantidades que salen del nodo

        Returns:
            dict: Diccionario con los resultados del análisis
    """

    total_entradas = sum(entradas)
    total_salidas = sum(salidas)
    diferencia = total_entradas - total_salidas

    # La conservación de flujo se cumple si la diferencia es 0
    se_cumple = (diferencia == 0)

    return {
        "se_cumple": se_cumple,
        "total_entradas": total_entradas,
        "total_salidas": total_salidas,
        "diferencia": diferencia
    }

# Prueba
entradas = [150, 200, 50]
salidas = [180, 220]

resultado = verificar_conservacion_flujo(entradas, salidas)

print(f"Entradas: {entradas}")
print(f"Salidas: {salidas}")
print(f"\nTotal de entradas: {resultado['total_entradas']}")
print(f"Total de Salidas: {resultado['total_salidas']}")
print(f"Diferencia (Entradas - Salidas): {resultado['diferencia']}")
print(f"\nCumple con la conservación de flujo: {resultado['se_cumple']}")
