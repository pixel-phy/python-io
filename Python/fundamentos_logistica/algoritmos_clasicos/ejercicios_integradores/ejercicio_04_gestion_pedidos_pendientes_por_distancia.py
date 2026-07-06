"""Ejercicio 04: Gestión de pedidos pendientes por distancia

Un sistema de delivery tiene pedidos con su distancia al destino. Para optimizar rutas,
se ordenan de menor a mayor distancia. Además, se necesita filtrar pedidos urgentes 
(distancia < 5km) y verificar si un pedido específico está pendiente.
    Requisitos:
    1. Ordenar pedidos por distancia usando Ordenamiento por Inserción.
    2. Filtrar pedidos urgentes (<5km) recorriendo la lista original.
    3. Buscar un pedido por ID en la lista original búsqueda lineal.
    4. Mostrar el proceso de inserción paso a paso (al menos 3 pasos). """

def insercion_ordenar_por_distancia(pedidos):
    """
    Ordenamiento por Inserción basado en distancia.
    """
    n = len(pedidos)
    pasos = []
    
    for i in range(1, n):
        actual = pedidos[i]
        j = i - 1
        
        while j >= 0 and pedidos[j][1] > actual[1]:
            pedidos[j + 1] = pedidos[j]
            j -= 1
        
        pedidos[j + 1] = actual
        
        # Guardar estado para mostrar (solo algunos pasos)
        if i <= 3 or i == n - 1:  # Mostrar primeros 3 y último
            pasos.append((i, pedidos))
    
    return pedidos, pasos

def filtrar_urgentes(pedidos, umbral=5.0):
    """Filtra pedidos con distancia menor al umbral."""
    urgentes = []
    for id_pedido, distancia in pedidos:
        if distancia < umbral:
            urgentes.append((id_pedido, distancia))
    return urgentes

def busqueda_lineal_pedido(pedidos, id_buscar):
    """Búsqueda lineal por ID en lista original."""
    for i, (id_pedido, distancia) in enumerate(pedidos):
        if id_pedido == id_buscar:
            return i, id_pedido, distancia
    return None

# DATOS DE EJEMPLO
pedidos = [
    ("ORD-101", 12.5),
    ("ORD-102", 3.2),
    ("ORD-103", 8.7),
    ("ORD-104", 2.1),
    ("ORD-105", 6.4)
]
buscar = "ORD-103"

# 1. Ordenar y mostrar proceso
ordenados, pasos = insercion_ordenar_por_distancia(pedidos)
print("--- Proceso de ordenamiento por inserción ---")
for paso, estado in pasos:
    print(f"Paso {paso}: {estado}")

print("\nLista ordenada por distancia:")
for id_pedido, distancia in ordenados:
    print(f"{id_pedido}: {distancia}km")

# 2. Filtrar urgentes
urgentes = filtrar_urgentes(pedidos)
print("\nPedidos urgentes (<5km):")
if urgentes:
    for id_pedido, distancia in urgentes:
        print(f"{id_pedido}: {distancia}km")
else:
    print("No hay pedidos urgentes")

# 3. Buscar por ID
resultado = busqueda_lineal_pedido(pedidos, buscar)
print(f"\nBuscando {buscar}:")
if resultado:
    idx, id_ped, dist = resultado
    print(f"Encontrado en índice {idx} - Distancia: {dist}km")
else:
    print("No encontrado")

# Caso: sin urgentes
print("\n--- Caso sin urgentes ---")
pedidos_no_urgentes = [("ORD-1", 10), ("ORD-2", 15)]
urgentes_vacio = filtrar_urgentes(pedidos_no_urgentes)
print(f"Urgentes en lista sin urgentes: {urgentes_vacio}")
