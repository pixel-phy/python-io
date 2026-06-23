"""Ejercicio 15: El validador de facturas de Combustible

Los operarios en las estaciones de carga digitan manualmente el número de ticket de combustible antes 
de que el Solver calcule los costos operativos del viaje. Necesitamos validar si el ticket completo
(que ya incluye el dígito verificador al final) es correcto.

    - Escribe una función que valide un código completo usando Verhoeff.
    - Algoritmo de validación: 1. Invierte el string completo (incluyendo el digito verificador).
    2. Inicializa c = 0.
    3. Recorre cada dígito con un índicie i (desde 0 hasta largo - 1).
    4. Busca en la tabla de permutación: val_p = TABLA_P[i % 8][digito].
    5. Actualiza c: c = TABLA_D[c][val_p]
    6. Si el código es totalmente válido, al terminar el bucle, c debe ser exactamente igual a 0.

    Input de prueba: El string resultante que se genera en el ejercicio 1 (ID base + digito). Debería dar True.
    Luego intercambia dos caracteres vecinos a propósito (error de transposición) y demuestra que da False. """

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

def validar_verhoeff(codigo_completo: str) -> bool:
    """Valida un código completo incluyendo el digito verificador"""
    if not codigo_completo or not codigo_completo.isdigit():
        return False

    c = 0
    for i, car in enumerate(reversed(codigo_completo)):
        val_p = TABLA_P[i % 8][int(car)]
        c = TABLA_D[c][val_p]

    return c == 0

# Pruebas
codigo_valido = "1234568"
print(f"Validando '{codigo_valido}': {validar_verhoeff(codigo_valido)}")

errores = [
    "1234569",
    "1234658",
    "1324568",
    "1235468"
]

for codigo_erroneo in errores:
    print(f"Validando '{codigo_erroneo}': {validar_verhoeff(codigo_erroneo)}")
