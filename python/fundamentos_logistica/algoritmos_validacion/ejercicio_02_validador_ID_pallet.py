"""Ejercicio 02: Validador de ID de Pallet (SSCC)

En un centro de distribución automatizado, los pallets de inventario se identifican con un código que incluye
un dígito de control de Luhn.
    - Escribir una función que reciba una cadena de texto con el ID del pallet y devuelva un booleano 
    indicando si es válido.
    - Probar "73500000000000017". """

def validar_pallet(id_pallet: str) -> bool:
    """
        Validar un ID de pallet (SSCC-18/GS1) optimizado para alta eficiencia.

        Evita la creación de listas intermedias en memoria mediante iteración inversa.

    """
    # 1. Limpieza rápida y validación de tipo
    id_limpio = id_pallet.replace(" ", "").replace("-", "")
    if not id_limpio or not id_limpio.isdigit():
        return False

    digito_control = int(id_limpio[-1])

    cupero_codigo = id_limpio[:-1]

    suma = 0
    # Iterar de derecha a izquierda sin duplicar el string en memoria
    # i = 0 es el dígito de control (último carácter)
    multiplicar_por_tres = True

    for char in reversed(cupero_codigo):
        digito = int(char)
        if multiplicar_por_tres:
            suma += digito * 3
        else:
            suma += digito
        multiplicar_por_tres = not multiplicar_por_tres

    digito_esperado = (10 - (suma % 10)) % 10

    return digito_control == digito_esperado

#Prueba
id_pallet = "373500000000000017"
print(f"ID del pallet: {id_pallet}")
print(f"¿Es válido según estándar logístico SSCC?: {validar_pallet(id_pallet)}")
