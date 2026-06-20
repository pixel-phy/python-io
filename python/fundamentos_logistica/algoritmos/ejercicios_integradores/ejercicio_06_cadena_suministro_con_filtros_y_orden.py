"""Cadena de suministro con múltiples filtros y orden

Una empresa de logística tiene proveedores con nombre, tiempo de entrega (días) y costo de envío. Se necesita:
    • Ordenar proveedores por tiempo de entrega (menor a mayor) usando Burbuja.
    • Ordenar proveedores por costo (menor a mayor) usando Inserción.
    • Buscar un proveedor por nombre en la lista Origianl usando búsqueda lineal.
    • Mostrar el top 3 de proveedores más rápidos y top 3 más baratos.

    Requisitos:
    1. Ordenar por tiempo con burbuja (mostrar pasos).
    2. Ordenar por costo con inserción.
    3. Búsqueda lineal por nombre en original.
    4. Mostrar top 3 de cada lista ordenada. """

def burbuja_ordenar_por_tiempo(proveedores):
    """
    Ordenamiento Burbuja basado en tiempo de entrega (elemento[1]).
    Justificación: Para mostrar el proceso paso a paso y comparar
    con el otro método de ordenamiento (inserción).
    """
    n = len(proveedores)
    pasos = []
    
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if proveedores[j][1] > proveedores[j + 1][1]:
                proveedores[j], proveedores[j + 1] = proveedores[j + 1], proveedores[j]
        
        pasos.append(proveedores)
    
    return proveedores, pasos

def insercion_ordenar_por_costo(proveedores):
    """
    Ordenamiento por Inserción basado en costo (elemento[2]).
    Justificación: Es estable y eficiente para listas pequeñas,
    complementa al burbuja mostrando otra técnica.
    """
    n = len(proveedores)
    
    for i in range(1, n):
        actual = proveedores[i]
        j = i - 1
        
        while j >= 0 and proveedores[j][2] > actual[2]:
            proveedores[j + 1] = proveedores[j]
            j -= 1
        
        proveedores[j + 1] = actual
    
    return proveedores

def busqueda_lineal_proveedor(proveedores, nombre_buscar):
    """Búsqueda lineal por nombre en lista original."""
    for i, (nombre, tiempo, costo) in enumerate(proveedores):
        if nombre == nombre_buscar:
            return i, nombre, tiempo, costo
    return None

def top_n(proveedores, n=3):
    """Devuelve los primeros n elementos de una lista."""
    return proveedores[:n] if len(proveedores) >= n else proveedores

proveedores = [
    ("LogiFast", 3, 150),
    ("CargaPlus", 5, 120),
    ("EnvioRap", 2, 200),
    ("TransExp", 4, 180),
    ("MegaShip", 6, 110)
]
buscar_nombre = "TransExp"

print("Proveedores originales:")
for nombre, tiempo, costo in proveedores:
    print(f"{nombre}: {tiempo} días, ${costo}")

# 1. Ordenar por tiempo (burbuja)
tiempo_ordenados, pasos_burbuja = burbuja_ordenar_por_tiempo(proveedores)
print("\n--- Ordenamiento por tiempo (burbuja) ---")
for i, paso in enumerate(pasos_burbuja, 1):
    print(f"Paso {i}: {paso}")

print("\nTop 3 más rápidos:")
for nombre, tiempo, costo in top_n(tiempo_ordenados, 3):
    print(f"{nombre}: {tiempo} días")

# 2. Ordenar por costo (inserción)
costo_ordenados = insercion_ordenar_por_costo(proveedores)
print("\nTop 3 más baratos:")
for nombre, tiempo, costo in top_n(costo_ordenados, 3):
    print(f"{nombre}: ${costo}")

# 3. Buscar por nombre
resultado = busqueda_lineal_proveedor(proveedores, buscar_nombre)
print(f"\nBuscando '{buscar_nombre}':")
if resultado:
    idx, nom, tiem, cost = resultado
    print(f"Encontrado en índice {idx} - Tiempo: {tiem} días, Costo: ${cost}")
else:
    print("No encontrado")

# 4. Mostrar listas completas ordenadas
print("\nLista completa ordenada por tiempo:")
for nombre, tiempo, costo in tiempo_ordenados:
    print(f"{nombre}: {tiempo} días, ${costo}")

print("\nLista completa ordenada por costo:")
for nombre, tiempo, costo in costo_ordenados:
    print(f"{nombre}: {tiempo} días, ${costo}")

# Caso: búsqueda inexistente
print("\n--- Caso inexistente ---")
resultado_inex = busqueda_lineal_proveedor(proveedores, "NoExiste")
if resultado_inex:
    print(f"Encontrado: {resultado_inex}")
else:
    print("NoExiste no encontrado (correcto)")
