"""Ejercicio 02: Priorización de pedidos por fecha de vencimiento

    En un almacén de productos perecederos, los pedidos deben procesarse según su fecha
    de vencimiento (lo más cercanos a vencer primero). Las fechas están en formato "DD-MM-YYYY". """

def ordenar_pedidos_vencimiento(pedidos: list[dict]):
    """ Ordena una lista de diccionarios por fecha de vencimiento (formato DD-MM-YYYY)
        usando burbuja. Convierte fechas a tuplas para comparar. 
    """

    def convertir_fecha_tupla(fecha_str):
        """Convierte 'DD-MM-YYYY' a (YYYY, MM, DD) para comparación correcta"""

        dia, mes, anio = fecha_str.split('-')
        return (int(anio), int(mes), int(dia))

    n = len(pedidos)

    for i in range(n - 1):
        intercambiado = False

        for j in range(0, n - i - 1):
            # Extraemos las fechas y las convertimos para comparar
            fecha1 = pedidos[j]["vencimiento"]
            fecha2 = pedidos[j + 1]["vencimiento"]

            # Convertimos a tuplas para comparar cronologicamente
            tupla1 = convertir_fecha_tupla(fecha1)
            tupla2 = convertir_fecha_tupla(fecha2)

            # Comparamos fechas: si fecha1 es mayor que fecha2 (más lejana)
            if tupla1 > tupla2:
                pedidos[j], pedidos[j + 1] = pedidos[j + 1], pedidos[j]
                intercambiado = True

        if not intercambiado:
            break

    return pedidos

# Prueba: 

pedidos = [
    {"id": "P001", "producto": "Leche", "vencimiento": "15-08-2026"},
    {"id": "P002", "producto": "Pan", "vencimiento": "20-06-2026"},
    {"id": "P003", "producto": "Huevos", "vencimiento": "10-07-2026"},
    {"id": "P004", "producto": "Carne", "vencimiento": "05-06-2026"},
    {"id": "P005", "producto": "Fruta", "vencimiento": "25-08-2026"}
]

print("Pedidos originales: ")
for pedido in pedidos:
    print(f"    {pedido['id']} - {pedido['producto']} - {pedido['vencimiento']}")

print("\nProceso de ordenamiento:")
ordenados = ordenar_pedidos_vencimiento(pedidos)
print("\nPedidos ordenados por vencimiento: ")
for pedido in ordenados:
    print(f"    {pedido['id']} - {pedido['producto']} - {pedido['vencimiento']}")
