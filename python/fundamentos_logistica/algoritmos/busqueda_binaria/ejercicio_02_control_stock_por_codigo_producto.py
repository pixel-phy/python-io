""" Ejercicio 02: Control de Stock con código de producto

    Un almacén tiene productos organizados por código SKU (ordenado numéricamente). Cada producto tiene
    asociado su cantidad en stock. El sistema debe verificar si un código SKU existe y mostrar su disponibilidad.

    Datos: Diccionario con SKU como clave y sctok como valor (ordenado por clave).
    Entrada: Código SKU a buscar.
    Salida: Stock disponible o mensaje de "producto no encontrado". """

def buscar_stock(inventario: dict, sku_buscado: int):
    """
        Busca un SKU en el inventario usando búsqueda binaria.
        Como los diccionarios no tienen un índice numérico, convertimos a listas ordenadas.

        Args:
            Inventario: Diccionario {sku: stock} ordenado por sku
            sku_buscado: Código SKU a buscar

        Returns: 
            Stock del producto o None si no existe.
    """

# Convertimos las claves del diccionario a una lista ordenada
    skus = sorted(inventario.keys()) # Con esto garantizamos orden

    izquierda = 0
    derecha = len(skus) - 1

    while izquierda <= derecha:
        medio = izquierda + (derecha - izquierda) // 2
        sku_actual = skus[medio]

        if sku_actual == sku_buscado:
            return inventario[sku_actual] # Devolvemos el stock
        elif sku_actual < sku_buscado:
            izquierda = medio + 1 
        else:
            derecha = medio - 1
    return None # SKU no encontrado

# Prueba: 

inventario = {1001: 45, 1003: 12, 1007: 89, 1010: 34, 1015: 67}

# Caso 1: encontrado
stock = buscar_stock(inventario, 1007)
if stock is not None:
    print(f"Producto 1007 tiene {stock} unidades")
else:
    print("Producto 1007 no encontrado en inventario")

# Caso 2: No encontrado
stock = buscar_stock(inventario, 1005)
if stock is not None:
    print(f"Producto 1005 tiene {stock} unidades")
else:
    print("Producto 1005 no encontrado en inventario")
