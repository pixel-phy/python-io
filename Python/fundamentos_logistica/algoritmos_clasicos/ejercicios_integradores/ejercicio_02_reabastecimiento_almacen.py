"""Ejercicio 02: Reabastecimiento de almacén

Un almacén tiene productos con su stock actual. Para planificar Reabastecimiento, se necesita:
    - Ordenar los productos por nombre para búsquedas rápidas.
    - Dado un nombre de producto, verificar si existe y consultar su stock.
    - Identificar productos con stock bajo (< 10 unidades) para generar alertas.

    Requisitos:
    1. Ordenar la lista de productos por nombre alfabéticamente usando ordenamiento por selección.
    2. Buscar un producto por nombre en la lista ordenada usando búsqueda binaria.
    3. Recorrer la lista original (No ordenada) para generar lista de productos con stock bajo.
    4. Mostrar resultados intermedios. """

def seleccion_ordenar_por_nombre(inventario):
    """
        Ordenamiento por selección basado en nombre (elemento[0]). """

    n = len(inventario)

    for i in range(n):
        # Encontrar el índice del menor elemento en la parte no ordenada
        min_idx = i
        for j in range(i + 1, n):
            # Comparar nombres alfabéticamente
            if inventario[j][0] < inventario[min_idx][0]:
                min_idx = j

        # Intercambiamos el elementos actual con el menor encontrado
        inventario[i], inventario[min_idx] = inventario[min_idx], inventario[i]

    return inventario

def busqueda_binaria(inventario_ordenado, nombre_buscar):
    """
        Búsqueda binaria para encontrar un producto por nombre"""

    izquierda = 0
    derecha = len(inventario_ordenado) - 1

    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        nombre_medio = inventario_ordenado[medio][0]

        if nombre_medio == nombre_buscar:
            return medio, inventario_ordenado[medio]
        elif nombre_buscar < nombre_medio:
            derecha = medio - 1
        else:
            izquierda = medio + 1

    return None

def stock_bajo(inventario, umbral=10):
    """Recorre la lista original y devuelve productos con stock bajo."""
    bajos = []
    for producto, stock in inventario:
        if stock < umbral:
            bajos.append((producto, stock))
    return bajos

# Prueba
inventario = [
    ("Manzanas", 15),
    ("Peras", 8),
    ("Naranjas", 23),
    ("Platanos", 5),
    ("Uvas", 12),
    ("Fresas", 3)
]
buscar = "Peras"

# 1. Productos con stock bajo (en original)
bajos = stock_bajo(inventario)
print("Stock bajo (<10) en original:")
for prod, stock in bajos:
    print(f"{prod}: {stock}")

# 2. Ordenar por nombre
ordenados = seleccion_ordenar_por_nombre(inventario)
print("\nLista ordenada por nombre (selección):")
for prod, stock in ordenados:
    print(f"{prod}: {stock}")

# 3. Buscar con binaria
resultado = busqueda_binaria(ordenados, buscar)
print(f"\nBuscando: '{buscar}' (binaria):")
if resultado:
    idx, (nombre, stock) = resultado
    print(f"Encontrado en indice {idx} - stock: {stock}")
else:
    print("No encontrado")

# Caso busqueda inexistente
print("\nCaso inexistente:")
resultado_inex = busqueda_binaria(ordenados, "kiwi")
if resultado_inex:
    print(f"Encontrado: {resultado_inex}")
else:
    print("Kiwi no encontrado.")
