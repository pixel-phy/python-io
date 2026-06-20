"""Ejercicio 02: Organización de Productos por caducidad

Un supermercado necesita ordenar sus productos perecederos por fecha de caducidad
(formato "DD/MM/AAAA"), de más próximo a caducar a más lejano, para colocarlos al frente de los
estantes. """

def convertir_fecha_a_numero(fecha_str):
    """Convierte fecha DD/MM/AAAA a número para comparar (AAAAMMDD)"""

    dia, mes, anio = fecha_str.split('/')
    return int(anio + mes + dia)

def ordenar_productos_por_caducidad(productos):
    """
        Ordena productos por fecha de caducidad (más próximo primero)
        usando inserción. Los productos son diccionarios.
        """

    lista_ordenada = list(productos)

    print("Lista inicial de productos:")
    for p in lista_ordenada:
        print(f"    {p['nombre']} (Lote: {p['lote']}) - Caduca: {p['fecha_caducidad']}")
    print()

    # Algortimo de inserción
    for i in range(1, len(lista_ordenada)):
        actual = lista_ordenada[i]
        j = i - 1
        fecha_actual = convertir_fecha_a_numero(actual['fecha_caducidad'])

        print(f"Paso {i}: Insertando producto '{actual['nombre']}' (caduca: {actual['fecha_caducidad']})")

        # Comparar fechas (más próximo = menor número)
        while j >= 0 and convertir_fecha_a_numero(lista_ordenada[j]['fecha_caducidad']) > fecha_actual:
            lista_ordenada[j+1] = lista_ordenada[j]
            j -= 1

        lista_ordenada[j+1] = actual

        print(f"    Producto '{actual['nombre']}' insertando en posición {j+1}")

        print(" Estado actual:")
        for idx, p in enumerate(lista_ordenada):
            print(f"    [{idx}] {p['nombre']} - {p['fecha_caducidad']}")

        print()
    return lista_ordenada

# Prueba
productos = [
    {"nombre": "Leche", "lote": "L123", "fecha_caducidad": "15/12/2026"},
    {"nombre": "Yogur", "lote": "Y456", "fecha_caducidad": "20/06/2026"},
    {"nombre": "Queso", "lote": "Q789", "fecha_caducidad": "05/06/2026"},
    {"nombre": "Mantequilla", "lote": "M101", "fecha_caducidad": "10/10/2026"}
]

print("Productos iniciales:")
for p in productos:
    print(f"    {p['nombre']}: caduca {p['fecha_caducidad']}")

print("\n")
resultado = ordenar_productos_por_caducidad(productos)

print("\nResultado final:")
for p in resultado:
    print(f"    {p['nombre']} (lote: {p['lote']}) - Caduca: {p['fecha_caducidad']}")
