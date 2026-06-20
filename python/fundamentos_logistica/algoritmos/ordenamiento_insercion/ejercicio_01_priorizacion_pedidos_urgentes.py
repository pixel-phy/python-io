"""Ejercicio 01: Priorización de pedidos urgentes

Un centro de distribución recibe pedidos con diferentes niveles de urgencia (1 = más urgente, 5 = menos urgente).
    Debes ordenar los pedidos de menor a mayor número de urgencia para que los más urgentes se procesen primero. """

def ordenar_pedidos_por_urgencia(pedidos: list[tuple[str, int, str]]):
    """
        Ordena una lista de pedidos por nivel de urgencia usando inserción.
        Los pedidos son tuplas (id, urgencia, ciudad).
        """
    # Convertimos la lista original a una lista mutable
    lista_ordenada = list(pedidos)

    print(f"Lista inicial: {lista_ordenada}\n")

    # ALgoritmo de inserción: recorremos desde el segundo elemento
    for i in range(1, len(lista_ordenada)):
        # Elemento actual a insertar
        elemento_actual = lista_ordenada[i]
        # Indice del elemento anterior
        j = i - 1

        print(f"Paso {i}: Insertando pedido {elemento_actual[0]} (urgencia: {elemento_actual[1]})")

        # Mover elementos mayores (menos urgentes = número mayor) a la derecha
        while j >= 0 and lista_ordenada[j][1] > elemento_actual[1]:
            lista_ordenada[j + 1] = lista_ordenada[j]
            j -= 1

        #Insertar el elemento en su posición correcta
        lista_ordenada[j + 1] = elemento_actual

        # Mostrar el estado actual
        print(f" Lista después de insertar: {lista_ordenada}")
        print(f" El pedido {elemento_actual[0]} se colocó en la posición {j+1}\n")
    return lista_ordenada

# Prueba:
pedidos = [
    ("P003", 3, "Madrid"),
    ("P001", 1, "Barcelona"),
    ("P005", 5, "Valencia"),
    ("P002", 2, "Sevilla"),
    ("P004", 4, "Bilbao")
]

print("Lista de pedidos inicial:")
for p in pedidos:
    print(f"    {p[0]}: urgencia {p[1]}, Destino {p[2]}")

print("\n")

resultado = ordenar_pedidos_por_urgencia(pedidos)

print("Pedidos ordenados por urgencia (ascendente):")
for p in resultado:
    print(f"    {p[0]}: Urgencia {p[1]}, Destino {p[2]}")
