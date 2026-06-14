"""Ejercicio 2:
    Tienes una ruta con paradas fijas y una lista de órdenes de entrega. """

# Coordenadas de 3 almacenes (cada una es una tuple con lat, lon)
almacenes = [
    (40.7128, -74.0060),  # NY
    (34.0522, -118.2437), # LA
    (41.8781, -87.6298)   # CHI
]

# Órdenes del día (lista mutable)
ordenes = ["ORD-101", "ORD-102", "ORD-103"]

"""Agregar una nueva orden "ORD-104" a la lista ordenes y luego imprime la primera tuple de almacenes. """

ordenes.append("ORD-104")
x, *rest = almacenes
print(f"La coordenada del primer almacen es: {x}.")
print(ordenes)
