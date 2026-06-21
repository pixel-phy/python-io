""" Ejercicio 05: Inventario con reorden y búsqueda múltiple

Un supermercado tiene productos con código, nombre y precio. Se necesita:
    - Ordenar por precio para ofertas ( de menor a mayor) usando Ordenamiento por Selección.
    - Buscar un producto por código (no por nombre) usando Búsqueda Binaria en la lista ordenada
    por precio (pero la búsqueda es por código, así que primero extraemos solo códigos).
    - Calcular precio promedio y encontrar producto más caro y más barato de la lista original. 

    Requisitos:
    1. Ordenar por precio usando Selección.
    2. Extraer lista de códigos de la lista ordenada.
    3. Buscar un código en esa lista de códigos usando Búsqueda Binaria.
    4. Mostrar el índice en la lista ordenada. """


def seleccion_ordenar_por_precio(productos):
    """
    Ordenamiento por Selección basado en precio (elemento[2]).
    """
    n = len(productos)
    
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if productos[j][2] < productos[min_idx][2]:
                min_idx = j
        
        productos[i], productos[min_idx] = productos[min_idx], productos[i]
    
    return productos

def extraer_codigos(lista_productos):
    """Extrae solo los códigos de una lista de productos."""
    return [producto[0] for producto in lista_productos]

def busqueda_binaria_codigos(lista_codigos, codigo_buscar):
    """
    Búsqueda Binaria en una lista de códigos (strings).

    """
    izquierda = 0
    derecha = len(lista_codigos) - 1
    
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        codigo_medio = lista_codigos[medio]
        
        if codigo_medio == codigo_buscar:
            return medio
        elif codigo_buscar < codigo_medio:
            derecha = medio - 1
        else:
            izquierda = medio + 1
    
    return None

def estadisticas_precios(productos):
    """Calcula precio promedio, más caro y más barato de lista original."""
    if not productos:
        return None, None, None
    
    total = 0
    mas_caro = productos[0]
    mas_barato = productos[0]
    
    for codigo, nombre, precio in productos:
        total += precio
        if precio > mas_caro[2]:
            mas_caro = (codigo, nombre, precio)
        if precio < mas_barato[2]:
            mas_barato = (codigo, nombre, precio)
    
    promedio = total / len(productos)
    return promedio, mas_caro, mas_barato

productos = [
    ("A100", "Leche", 1.20),
    ("B200", "Pan", 0.80),
    ("C300", "Huevos", 2.50),
    ("D400", "Queso", 4.30),
    ("E500", "Manzanas", 1.50)
]
buscar_codigo = "C300"

# 1. Estadísticas de precios
promedio, mas_caro, mas_barato = estadisticas_precios(productos)
print("Estadísticas de precios (original):")
print(f"Precio promedio: ${promedio:.2f}")
print(f"Más caro: {mas_caro[0]} - {mas_caro[1]} - ${mas_caro[2]:.2f}")
print(f"Más barato: {mas_barato[0]} - {mas_barato[1]} - ${mas_barato[2]:.2f}")

# 2. Ordenar por precio
ordenados = seleccion_ordenar_por_precio(productos)
print("\nLista ordenada por precio (selección):")
for codigo, nombre, precio in ordenados:
    print(f"{codigo}: {nombre} - ${precio:.2f}")

# 3. Extraer códigos y buscar
codigos = extraer_codigos(ordenados)
print(f"\nCódigos extraídos (en orden de precio): {codigos}")

indice = busqueda_binaria_codigos(codigos, buscar_codigo)
print(f"\nBuscando código {buscar_codigo}:")
if indice is not None:
    codigo, nombre, precio = ordenados[indice]
    print(f"Encontrado en índice {indice} - {nombre} - ${precio:.2f}")
else:
    print("No encontrado")

# Caso: código inexistente
print("\n--- Caso inexistente ---")
indice_inex = busqueda_binaria_codigos(codigos, "Z999")
print(f"Código Z999: {'No encontrado' if indice_inex is None else 'Encontrado'}")
