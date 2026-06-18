""" Ejercicio 01: Priorización de pedidos por urgencia 

    Un centro de distribución tiene una lista de pedidos pendientes. Cada pedido tiene un código
    y un nivel de urgencia (1 = muy urgente, 5 = poco urgente). Se debe ordenar los pedidos de 
    menor urgente a más urgente para planificar la urta de entrega. """

def ordenar_pedidos_por_urgencia(pedidos: list[tuple[str, int]]):
    """
        Ordena una lista de pedidos por urgencia de menor a mayor usando el algoritmo de selección

        Args:
            Pedidos: Lista de tuplas (código, urgencia)

        Returns:
            Lista ordenada por urgencia ascendente
    """

    n = len(pedidos)

    for i in range(n):
        # Encontrar el índice del elemento con menor urgencia en la parte no ordenada
        indice_min = i
        for j in range(i + 1, n):
            # Comparar por urgencia
            if pedidos[j][1] < pedidos[indice_min][1]:
                indice_min = j

        # Intercambiar el elemento actual con el mínimo encontrado
        if indice_min != i:
            pedidos[i], pedidos[indice_min] = pedidos[indice_min], pedidos[i]

    return pedidos

# Prueba:
pedidos = [
    ("P001", 3),
    ("P002", 1),
    ("P003", 5),
    ("P004", 2),
    ("P005", 4)
]

print("Entrada:", pedidos)
resultado = ordenar_pedidos_por_urgencia(pedidos)
print("Salida:", resultado)

