""" Ejercicio 03: Ordenamiento de productos por dos criterios (Precio y nombre)

    Un sistema de inventario debe ordenar productos primero por precio (de menor a mayor)
    y, en caso de empate, alfabéticamente por nombre. Esto ayuda a generar catálogos de productos. 

"""

def ordenar_productos_criterios(productos: list[tuple[str, float]]):
    """
        Ordena tuplas (nombre, precio) por precio ascendete y luego por nombre alfabetico.
    """
    n = len(productos)
    
    for i in range(n - 1):
        intercambio = False

        for j in range(0, n - i - 1):
            producto_actual = productos[j]
            producto_siguiente = productos[j + 1]

            # Extraemos el precio y nombre
            precio1, nombre1 = producto_actual[1], producto_actual[0]
            precio2, nombre2 = producto_siguiente[1], producto_siguiente[0]

            # Criterio 1: comparar por precio
            # Criterio 2: si precios iguales, comprar por nombre (orden alfabético)
            debe_intercambiar = False

            if precio1 > precio2:
                debe_intercambiar = True
            elif precio1 == precio2:
                # Si los precios son iguales, comparamos nombres
                if nombre1 > nombre2:
                    debe_intercambiar = True

            if debe_intercambiar:
                productos[j], productos[j + 1] = productos[j + 1], productos[j]
                intercambiado = True

        if not intercambiado:
            break

    return productos

# Prueba:

productos = [
    ("Laptop", 1200.00),
    ("Mouse", 25.50),
    ("Teclado", 45.00),
    ("Monitor", 300.00),
    ("Mouse", 30.00),    # Mismo nombre, precio diferente
    ("USB", 25.50)       # Mismo precio, nombre diferente
]

print("Productos originales:")
for producto in productos:
          print(f"    {producto[0]} - ${producto[1]:.2f}")
ordenados = ordenar_productos_criterios(productos)
print("\nProductos ordenados:")
for producto in ordenados:
          print(f"    {producto[0]} - ${producto[1]:.2f}")
