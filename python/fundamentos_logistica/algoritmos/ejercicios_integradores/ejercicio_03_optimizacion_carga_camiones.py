"""Ejercicio 03: Optimización de Carga de camiones
Un centro de distribución debe cargar camiones con paquetes. Primero se ordenan los paquetes por tamaño
(para aprovechar espacio) y luego se debe verificar si un paquete específico está en la carga original.
    Requisitos:
    1. Ordenar los paquetes por tamaño (ascendente) usando Ordenamiento Burbuja.
    2. Verificar si un paquete existe en la lista Original usando Búsqueda lineal.
    3. Además, encontrar el paquete más pesado de la lista original (recorrido simple).
    4. Mostrar todos los pasos del burbuja (cómo va ordenando)."""

def burbuja_ordenar_por_tamano(carga):
    """Ordenamiento Burbuja basado en tamaño (elemento[1]). """
    n = len(carga)
    pasos = []
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            # Comparar por tamaño (elemento[1])
            if carga[j][1] > carga[j + 1][1]:
                # Intercambiar
                carga[j], carga[j+1] = carga[j + 1], carga[j]
        pasos.append(carga)
    return carga, pasos

def busqueda_lineal_con_peso(carga, codigo_buscar):
    """Búsqueda lineal en lista original por código"""
    for i, (codigo, tamano, peso) in enumerate(carga):
        if codigo == codigo_buscar:
            return i, codigo, tamano, peso
    return None

def encontrar_mas_pesado(carga):
    """Recorrido simple para encontrar el paquete más pesado"""
    if not carga:
        return None

    mas_pesado = carga[0]
    for item in carga[1:]:
        if item[2] > mas_pesado[2]:
            mas_pesado = item
    return mas_pesado

#Prueba:
carga = [
    ("Paq-A", 10, 2.5),
    ("Paq-B", 5, 1.8),
    ("Paq-C", 15, 3.2),
    ("Paq-D", 8, 2.0),
    ("Paq-E", 12, 4.1)
]
buscar = "Paq-D"

print("Carga original:")
for item in carga:
    print(item)

# 1. Ordenar con burbuja y mostrar pasos
ordenados, pasos = burbuja_ordenar_por_tamano(carga)
print("\n--- Proceso de ordenamiento burbuja ---")
for i, paso in enumerate(pasos, 1):
    print(f"Paso {i}: {paso}")

print("\nLista ordenada por tamaño:")
for codigo, tamano, peso in ordenados:
    print(f"{codigo} ({tamano}kg)")

# 2. Buscar lineal
resultado = busqueda_lineal_con_peso(carga, buscar)
print(f"\nBuscando {buscar} (lineal):")
if resultado:
    idx, cod, tam, pes = resultado
    print(f"Encontrado en índice {idx}")
else:
    print("No encontrado")

# 3. Encontrar más pesado
mas_pesado = encontrar_mas_pesado(carga)
if mas_pesado:
    cod, tam, pes = mas_pesado
    print(f"Paquete más pesado: {cod} ({pes}kg)")

# Caso: lista vacía
print("\n--- Caso lista vacía ---")
carga_vacia = []
mas_pesado_vacio = encontrar_mas_pesado(carga_vacia)
print(f"Más pesado en lista vacía: {mas_pesado_vacio}")

