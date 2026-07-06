""" Ejercicio 02: Organización de productos por fecha de vencimiento

    Un supermercado debe ordenar sus produstos perecederos por fecha de vencimiento para aplicar 
    la estrategia FIFO (First In, First Out). Los productos más cercanos a vencer deben ir primero. """

def convertir_fecha(fecha_str):
    """Convierte fecha "DD-MM-AAAA" a tupla (AAAA, MM, DD) para comparar fácilmente"""

    dia, mes, anio = fecha_str.split("-")
    return (int(anio), int(mes), int(dia))

def ordenar_productos_por_vencimiento(productos: list[dict]):
    """ Ordena productos por fecha de vencimiento (más próximo primero)

    Args:
        productos: Lista de diccionarios con 'nombre', 'fecha_vencimiento', 'cantidad'

    Returns:
        Lista ordenada por fecha de vencimiento ascendente 
    """

    n = len(productos)
    
    for i in range(n):
        indice_min = i
        fecha_min = convertir_fecha(productos[i]['fecha_vencimiento'])

        for j in range(i + 1, n):
            fecha_actual = convertir_fecha(productos[j]['fecha_vencimiento'])
            if fecha_actual < fecha_min:
                indice_min = j
                fecha_min = fecha_actual

        if indice_min != i:
            productos[i], productos[indice_min] = productos[indice_min], productos[i]

    return productos

productos = [
    {"nombre": "Leche", "fecha_vencimiento": "15-08-2026", "cantidad": 20},
    {"nombre": "Yogurt", "fecha_vencimiento": "05-08-2026", "cantidad": 15},
    {"nombre": "Queso", "fecha_vencimiento": "20-08-2026", "cantidad": 10},
    {"nombre": "Mantequilla", "fecha_vencimiento": "10-08-2026", "cantidad": 8}
]

print("Entrada:")
for p in productos:
    print(f"    {p}")
print("\n")

resultado = ordenar_productos_por_vencimiento(productos)

print("\Salida:")
for p in productos:
    print(f"    {p}")
print("\n")
