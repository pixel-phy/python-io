"""El algoritmo de Damm (Geometría de Cuasigrupos)

El algoritmo de Damm es una alternativa moderna y brillante en Verhoeff. Al igual que Verhoeff, detecta el 100%
    de los errores de transposición, pero tiene una enorme ventaja: no requiere invertir el string ni manejar 
posiciones pares/impares. Se basa enteramente en una matriz de operaciones de cuasigrupo (Una tabla matemática 10 x 10).

    La matriz oficial de Damm es la siguiente:

    MATRIZ_DAMM = [
    [0, 3, 1, 7, 5, 9, 8, 6, 4, 2],
    [7, 0, 9, 2, 1, 5, 4, 8, 6, 3],
    [4, 2, 0, 6, 8, 7, 1, 3, 5, 9],
    [1, 7, 5, 0, 9, 8, 3, 4, 2, 6],
    [6, 1, 2, 3, 0, 4, 5, 9, 7, 8],
    [3, 6, 7, 4, 2, 0, 9, 5, 8, 1],
    [5, 8, 6, 9, 7, 2, 0, 1, 3, 4],
    [8, 9, 4, 5, 3, 6, 2, 0, 1, 7],
    [9, 4, 3, 8, 6, 1, 7, 2, 0, 5],
    [2, 5, 8, 1, 4, 3, 6, 7, 9, 0]
]

- Algoritmo de Validación: 
    1. Inicializa una variable interseccion = 0.
    2. Recorre el string de izquierda a derecha (orden natural).
    3. En cada paso, actualiza: interseccion = MATRIZ_DAMM[interseccion][int(caracter)]
    4. Si el código completo (incluyendo su dígito verificador) es correcto, al final de la cadena
    interseccion debe valer exactamente 0.
    
    Escribe la función validar_damm(codigo: str) -> bool. Pruébala con el código "5724". Luego, simula
    un error de transposición cambiando el input a "5274" y demuestra que el código captura el error 
    devolviendo False. """

MATRIZ_DAMM = [
    [0, 3, 1, 7, 5, 9, 8, 6, 4, 2],
    [7, 0, 9, 2, 1, 5, 4, 8, 6, 3],
    [4, 2, 0, 6, 8, 7, 1, 3, 5, 9],
    [1, 7, 5, 0, 9, 8, 3, 4, 2, 6],
    [6, 1, 2, 3, 0, 4, 5, 9, 7, 8],
    [3, 6, 7, 4, 2, 0, 9, 5, 8, 1],
    [5, 8, 6, 9, 7, 2, 0, 1, 3, 4],
    [8, 9, 4, 5, 3, 6, 2, 0, 1, 7],
    [9, 4, 3, 8, 6, 1, 7, 2, 0, 5],
    [2, 5, 8, 1, 4, 3, 6, 7, 9, 0]
]

def validar_damm(codigo: str) -> bool:
    """
        valida un código usando el algoritmo de Damm.

        Args:
            codigo: String con los digitos a validar (incluyendo digito verificador)

        Returns:
            True si el código es válido, False en caso contrario
    """

    interseccion = 0

    for caracter in codigo:
        # Se convierte el caracter a entero
        digito = int(caracter)
        # Actualizamos la interseccion usando la matriz
        interseccion = MATRIZ_DAMM[interseccion][digito]

    # El código es válido si al final intersección es 0
    return interseccion == 0

# Prueba
print(f"Código '5724' es válido: {validar_damm('5724')}")

# Prueba 2
print(f"Código '5274' es válido: {validar_damm('5274')}")
