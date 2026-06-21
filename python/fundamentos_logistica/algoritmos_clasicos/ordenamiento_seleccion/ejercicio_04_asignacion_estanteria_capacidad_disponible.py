"""Ejercicio 04: Asignación de estantería por capacidad disponible

    Un almacén tiene estantería con diferentes capacidades (número de cajas que pueden almacenar). Se deben ordenar 
    las estanterías de mayor a menor capacidad para asignar primero los productos más voluminosos. """

def ordenar_estanterias_por_capacidad(estanterias: list[dict]):
    """
        Ordena estanterías de mayor a menor capacidad usando selección.

        Args:
            estanterias: Lista de diccionarios con 'id_estanteria' y 'capacidad'

    Returns:
            Lista ordenada por capacidad descendente
    """

    n = len(estanterias)

    for i in range(n):
        # Para orden descendente, buscamos el índice del elemento con mayor capacidad
        indice_max = i

        for j in range(i + 1, n):
            if estanterias[j]['capacidad'] > estanterias[indice_max]['capacidad']:
                indice_max = j

        if indice_max != i:
            estanterias[i], estanterias[indice_max] = estanterias[indice_max], estanterias[i]

    return estanterias

estanterias = [
    {"id_estanteria": "E01", "capacidad": 150},
    {"id_estanteria": "E02", "capacidad": 200},
    {"id_estanteria": "E03", "capacidad": 100},
    {"id_estanteria": "E04", "capacidad": 250},
    {"id_estanteria": "E05", "capacidad": 180}
]

print("Entrada:")
for e in estanterias:
    print(f"Estantería {e['id_estanteria']}: {e['capacidad']} cajas")

print("\n")

resultado = ordenar_estanterias_por_capacidad(estanterias)
for e in resultado:
    print(f"estanterias {e['id_estanteria']}: {e['capacidad']} cajas")
