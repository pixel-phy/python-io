"""Ejercicio 01: Ruta óptima de entrega con reordenamiento

Una empresa de mensajería tiene una lista de pedidos con sus códigos y pesos. Cada día, 
los repartidores deben entregar en orden de prioridad (primero los más livianos para ahorrar
combustible). Además, el sistema debe verificar rápidamente si un pedido específico ya fue 
entregado.

    Requisitos:
    1. Ordenar la lista de pedidos por peso usando Ordenamiento por inserción.
    2. Dado el código de un pedido, buscar si existe en la lista original usando 
    búsqueda lineal.
    3. Mostrar:
        - Lista original con índices.
        - Lista ordenada por peso. 
        - Resultado de búsqueda (existe/no existe y en qué índice original estaba). """

def insercion_ordenada_por_peso(pedidos):
    """
        Ordenamiento por inserción basado en el peso (elemento[1]). """

    n = len(pedidos)

    for i in range(1, n):
        # Guardar elemento actual a insertar
        actual = pedidos[i]
        j = i - 1

        # Mover elementos mayores que 'actual' una posición adelante
        while j >= 0 and pedidos[j][1] > actual[1]:
            pedidos[j+1] = pedidos[j]
            j -= 1

        pedidos[j+1] = actual

    return pedidos

def busqueda_lineal(pedidos, codigo_buscar):
    """
        Busqueda lineal para encontrar un pedido por código. """

    for i, (codigo, peso) in enumerate(pedidos):
        if codigo == codigo_buscar:
            return i, codigo, peso

    return None

#Prueba:
pedidos = [
    ("P001", 5.2),
    ("P001", 3.8),
    ("P003", 7.1),
    ("P004", 2.5), 
    ("P005", 6.0)
]

buscar = "P003"

# 1. Mostrar lista original
print("Lista original:")
for i, (codigo, peso) in enumerate(pedidos):
    print(f"indice {i}: {codigo} - {peso}kg")

# 2. Ordenar por peso
ordenados = insercion_ordenada_por_peso(pedidos)
print("\nLista ordenada por peso (inserción):")
for codigo, peso in ordenados:
    print(f"{codigo} - {peso}kg")

# 3. Buscar pedido
resultado = busqueda_lineal(pedidos, buscar)
print(f"\nBuscando {buscar} (búsqueda lineal):")
if resultado:
    idx, cod, pes = resultado
    print(f"Encontrado en índice original {idx}")
else:
    print("No encontrado")

# Prueba de búsqueda de elemento inexistente
print("\nCaso búsqueda inexistente:")
resultado_inex = busqueda_lineal(pedidos, "P999")
if resultado_inex:
    print(f"Encontrado: {resultado_inex}")
else:
    print("P999 no encontrado")
