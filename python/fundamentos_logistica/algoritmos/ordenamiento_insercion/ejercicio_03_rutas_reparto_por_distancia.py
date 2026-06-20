"""Ejercicio 03: Rutas de Reparto por distancia

Una empresa de mensajería tiene una lista de envío pendientes con su distancia en kilómetros desde el almacén.
    Deben ordenar las rutas de menor a mayor distancia para optimizar el combustible. También necesitan poder 
    ordenar de mayor a menor (descendente) para casos especiales. """

def ordenar_envio_por_distancia(envios: list[tuple[str, float, str]], descendente: bool=False):
    """
        Ordena envíos por distancia usando inserción.
        Descendente= True para ordenar de mayor a menor.
        """

    lista_ordenada = list(envios)

    orden = "descendente" if descendente else "ascendente"
    print(f"Ordenamiento {orden.upper()}")
    print(f"Lista inicial: {lista_ordenada}\n")

    for i in range(1, len(lista_ordenada)):
        actual = lista_ordenada[i]
        j = i - 1

        print(f"Paso {i}: Insertando envío {actual[0]} (distancia: {actual[1]} km)")

        # Si descendente, usamos < en lugar de >
        if descendente:
            while j >= 0 and lista_ordenada[j][1] < actual[1]:
                lista_ordenada[j + 1] = lista_ordenada[j]
                j -= 1

        else:
            while j >= 0 and lista_ordenada[j][1] > actual[1]:
                lista_ordenada[j+1] = lista_ordenada[j]
                j -= 1

        lista_ordenada[j+1] = actual

        print(f"    Envío {actual[0]} colocado en posición {j+1}")
        print(f"    Estado: {lista_ordenada}\n")

    return lista_ordenada

# Prueba
envios = [
    ("E005", 12.5, "Zona Norte"),
    ("E001", 3.2, "Centro"),
    ("E003", 8.7, "Zona Este"),
    ("E002", 15.0, "Zona Oeste"),
    ("E004", 5.3, "Zona Sur")
]

print("Envíos iniciales:")
for e in envios:
    print(f"    {e[0]}: {e[1]} km -> {e[2]}")

# Orden ascendente
resultado_asc = ordenar_envio_por_distancia(envios, descendente=False)
print("\nResultado ascendente (menor a mayor distancia)")
for e in resultado_asc:
    print(f"    {e[0]}: {e[1]} km {e[2]}")

# Orden descendente
resultado_desc = ordenar_envio_por_distancia(envios, descendente=True)
print("\nResultado descendente (mayor a menor distacia)")
for e in resultado_desc:
    print(f"    {e[0]}: {e[1]} km -> {e[2]}")
