"""Ejercicio 2: Primera ubicación de un lote vencido

En un almacén de alimentos perecederos, cada lote tiene una fecha de vencimiento (número de días desde hoy). 
Se debe encontrar el primer lote (dias < 0) en la lista para priorizar su descarte. La lista está ordenada por
pasillo, no por fecha. Usa búsqueda lineal para encontrar el primer elemento con vencimiento negativo. """

def encontrar_primer_vencido(lotes: list):
    # Recorremos la lista secuencialmente
    for lote in lotes:
        # Verificamos si el vencimiento es negativo
        if lote["vencimiento"] < 0:
            return lote # Se retorna lote vencido encontrado
    return None # Si no hay lotes vencidos

# Prueba
lotes = [
    {"codigo": "L001", "vencimiento": 5},
    {"codigo": "L002", "vencimiento": -2},
    {"codigo": "L003", "vencimiento": 10},
    {"codigo": "L004", "vencimiento": -1}
]

print(encontrar_primer_vencido(lotes))
