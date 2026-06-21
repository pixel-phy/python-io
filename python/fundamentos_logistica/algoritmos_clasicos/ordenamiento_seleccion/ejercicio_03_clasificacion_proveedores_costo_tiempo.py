"""Ejercicio 03: Clasificación de proveedores por costo y tiempo de entrega

    Una empresa evalúa proveedores. Cada proveedor tiene: nombre, costo por unidad (menor es mejor) y 
    tiempo de entrega en día (menor es mejor). Debes ordenar los proveedores de manera descendente
    (mejores primero) según: primero por costo (menor a mayor), y si empatan, por tiempo de entrega. """

def ordenar_proveedores(proveedores: list[tuple[str, int, int]]):
    """
        Ordena proveedores: primero por costo (menor mejor), y si empatan por tiempo_entrega
        (menor mejor). Orden descendente de calidad (mejores primero).

        Args: 
            proveedores: Lista de tuplas(nombre, costo, tiempo_entrega)

        Returns:
            Lista ordenada (mejores primero) """

    n = len(proveedores)
    
    for i in range(n):
        indice_mejor = i

        for j in range(i + 1, n):
            # Comparar por costo primero
            if proveedores[j][1] < proveedores[indice_mejor][1]:
                indice_mejor = j

            # Si igual costo, comparar por tiempo
            elif proveedores[j][1] == proveedores[indice_mejor][1]:
                if proveedores[j][2] < proveedores[indice_mejor][2]:
                    indice_mejor = j

        if indice_mejor != i:
            proveedores[i], proveedores[indice_mejor] = proveedores[indice_mejor], proveedores[i]

    return proveedores

proveedores = [
    ("Proveedor A", 150, 5),
    ("Proveedor B", 120, 3),
    ("Proveedor C", 120, 2),
    ("Proveedor D", 180, 4),
    ("Proveedor E", 130, 3)
]

print("Entrada:")

for p in proveedores:
    print(f"    {p[0]}: ${p[1]} | {p[2]} días")
print("\n")

resultado = ordenar_proveedores(proveedores)

print("Salida:")
for p in resultado:
    print(f"    {p[0]}: ${p[1]} | {p[2]} días")
