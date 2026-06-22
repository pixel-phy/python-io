"""Ejercicio 10: El filtro del Sorter Óptico

    Un escáner láser en una cinta transportadora de clasificación de equipaje/mercancía lee 
    códigos EAN-13 a gran velocidad. Debido al movimiento, a veces lee caracteres incompletos
    o cadenas con longitudes erróneas.

    Escribe una función que reciba el string del código de barras, valide que mida exactamente
    13 dígitos y que su dígito verificador sea matemáticamente correcto bajo la norma EAN-13.
    Input de purbea: "7501055311220"."""

def validar_ean13(codigo: str) -> bool:
    """Valida un código EAN-13 completo.

        Args: 
            codigo (str): Código de barras de 13 dígitos

        Returns:
            bool: True si es válido, False en caso contrario
    """
    # 1. Validar que sea string
    if not isinstance(codigo, str):
        return False

    # Validamos cantidad de caracteres
    if len(codigo) != 13:
        return False

    # Validar que todos los caracteres sean digitos
    if not codigo.isdigit():
        return False

    # 4. Calcular el digito verificador
    # Los primeros 12 digitos son los datos, el 13 es el verfiicador
    digitos = [int(c) for c in codigo]
    digito_verificador_recibido = digitos[12]

    # Calcular suma: pares*3 + impares*1
    suma = 0
    for i in range(12):
        if i % 2 == 0:
            suma += digitos[i] * 1
        else:
            suma += digitos[i] * 3

    # Calculamos digito verificador esperado
    digito_verificador_esperado = (10 - (suma % 10)) % 10

    # 5. Comparar
    return digito_verificador_recibido == digito_verificador_esperado

# Prueba
codigo_prueba = "7501055311224"
resultado = validar_ean13(codigo_prueba)
print(f"\nResultado: {resultado}")
