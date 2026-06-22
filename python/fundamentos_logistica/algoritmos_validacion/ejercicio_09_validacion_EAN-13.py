"""El Algoritmo de Validación EAN-13:
    A diferencia del SSCC, el EAN-13 tiene exactamente 13 dígitos:
    1. Se toman los primero 12 digitos.
    2. Empezando de izquierda a derecha, los digitos en posiciones impares (1ra, 3ra, 5ta...) se 
    multiplican por 1.
    3. Los digitos en posiciones pares (2da, 4ta, 6ta...) se multiplican por 3.
    4. Se suman todos los resultados.
    5. El dígito de control es el número que se debe sumar a este resultado para alcanzar el 
    siguiente múltiplo de 10. """

def validar_ean13(codigo: str) -> bool:
    if len(codigo) != 13 or not codigo.isdigit():
        return False

    cuerpo = codigo[:-1]
    digito_control = int(codigo[-1])

    # Ponderación EAN-13 estándar de izquierda a derecha
    suma = 0
    for i, char in enumerate(cuerpo):
        digito = int(char)
        if i % 2 == 0: # posición impar en base 1 (índice 0, 2, 4, ...)
            suma += digito * 1
        else:
            suma += digito * 3

    digito_esperado = (10 - (suma % 10)) % 10
    return digito_control == digito_esperado
