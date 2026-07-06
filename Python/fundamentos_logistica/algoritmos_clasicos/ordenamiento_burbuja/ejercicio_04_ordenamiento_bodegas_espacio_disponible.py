"""Ejercicio 04: Ordenamiento de Bodegas por Espacio Disponible y Código

    Una cadena de supermercados tiene múltiples bodegas. Necesitan ordenarlas por 
    espacio disponible (de menor a mayor) para saber cuáles necesitan reabastecimiento
    urgente. En caso de empate, por código de bodega. """

def ordenar_bodegas(bodegas: list[dict]):
    """
        Ordena diccionarios de bodegas por espacio_libre, y en caso de empate, 
        por código alfabéticamente """

    n =len(bodegas)

    for i in range(n - 1):
        intercambiado = False

        for j in range(0, n - i - 1):
            bodega_actual = bodegas[j]
            bodega_siguiente = bodegas[j + 1]

            espacio1 = bodega_actual["espacio_libre"]
            espacio2 = bodega_siguiente["espacio_libre"]
            codigo1 = bodega_actual["codigo"]
            codigo2 = bodega_siguiente["codigo"]

            # Criterio 1: espacio libre
            # Criterio 2: si igual, código alfabéticamente
            
            debe_intercambiar = False

            if espacio1 > espacio2:
                debe_intercambiar = True
            elif espacio1 == espacio2:
                if codigo1 > codigo2:
                    debe_intercambiar = True

            if debe_intercambiar:
                bodegas[j], bodegas[j+ 1] = bodegas[j + 1], bodegas[j]

                intercambiado = True

        if not intercambiado:
            break

    return bodegas

# Prueba:

bodegas = [
    {"codigo": "B03", "nombre": "Bodega Norte", "espacio_libre": 1500},
    {"codigo": "B01", "nombre": "Bodega Central", "espacio_libre": 800},
    {"codigo": "B05", "nombre": "Bodega Sur", "espacio_libre": 1200},
    {"codigo": "B02", "nombre": "Bodega Este", "espacio_libre": 800},   # Mismo espacio
    {"codigo": "B04", "nombre": "Bodega Oeste", "espacio_libre": 2000}
]

print("Bodegas originales:")
for bodega in bodegas:
    print(f"    {bodega['codigo']} - {bodega['nombre']} - {bodega['espacio_libre']} m²")

ordenadas = ordenar_bodegas(bodegas)

print("\nBodegas ordenadas:")
for bodega in bodegas:
    print(f"    {bodega['codigo']} - {bodega['nombre']} - {bodega['espacio_libre']} m²")
