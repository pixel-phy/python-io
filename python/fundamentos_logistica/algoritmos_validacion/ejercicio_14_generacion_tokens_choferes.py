"""Ejercicio 14: El generador de Tokens para Choferes

Cada chofer de la flota tiene un ID base numérico de 6 digitos. Para que puedan loguearse en la app de ruteo
sin errores, el sistema debe añadir un sétimo digito calculado con el algoritmo de Verhoeff.

    - Escribir una función que reciba el ID base de 6 dígitos y calcule su digito verificador de Verhoeff. 
    - Algoritmo de generación: 1. Invierte el ID base.
    2. Inicializa c = 0.
    3. Recorre con un índice i desde 0 hasta 5. Busca el dígito en la tabla de permutación.
    4. Actualiza c usando la tabla de multiplicación.
    5. El digito verificador final será el inverso de c.

    Input de prueba: "123456". """

# Tablas del algoritmo de Verhoeff
TABLA_D = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
    [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
    [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
    [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
    [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
    [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
    [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
    [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
]

TABLA_P = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
    [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
    [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
    [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
    [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
    [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
    [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]
]

VECTOR_INV = [0, 4, 3, 2, 1, 5, 6, 7, 8, 9]

def validacion_verhoeff(id_base: str) -> int:
    """Calcula el dígito verificador de Verhoeff para un ID base"""
    # Invertir el ID base
    c = 0
    for i, car in enumerate(reversed(id_base)):
        val_p = TABLA_P[(i+1) % 8][int(car)]
        c = TABLA_D[c][val_p]

    return VECTOR_INV[c]

# Prueba
id_base = "123456"
digito_verificador = validacion_verhoeff(id_base)
print(f"ID base: {id_base}")
print(f"Digito verificador: {digito_verificador}")
print(f"ID completo: {id_base}{digito_verificador}")

