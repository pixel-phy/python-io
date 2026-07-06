""" El algoritmo de Verhoeff (Grupo Diedral D5)

    Este algoritmo no utiliza la aritmética común como la que se ha trabajado en los algoritmos anteriores.
    En su lugar, opera dentro del grupo diedral D5, que matemáticamente describe rotaciones y reflexiones
    de un pentágono regular.

    Para programarlo en Python sin tener que calcular álgebra abstracta en tiempo real, el algoritmo se apoya
    en tres matrices (tablas) precalculadas estandarizadas:

    1. Matriz de multiplicación (d): Una tabla de 10 x 10 que define la operación del grupoo D5.
    2. Matriz de Permutación (p): Una tabla de 8 x 10 que altera el valor del dígito basándose en su posición
    (módulo 8) de derecha a izquierda.
    3. Vector de Inversión (inv): Una lista de 10 elementos que halla el elemento inverso dentro del grupo para
    obtener el dígito de control. """

# Ejemplo:
# Matriz de multiplicación basada en el grupo diédrico D_5
MULTIPLICATION_TABLE = [
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

# Matriz de permutación para la posición de los dígitos
PERMUTATION_TABLE = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
    [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
    [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
    [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
    [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
    [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
    [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]
]

# Inversa de la multiplicación para obtener el dígito verificador final
INVERSE_TABLE = [0, 4, 3, 2, 1, 5, 6, 7, 8, 9]


# --- FUNCIONES DEL ALGORITMO ---

def calcular_checksum(numero_str, incluye_digito_verificador):
    """
    Función interna que recorre el número de derecha a izquierda 
    aplicando las operaciones matemáticas de Verhoeff.
    """
    # Convertimos el texto en una lista de números enteros, ignorando espacios o guiones
    digitos = []
    for caracter in numero_str:
        if caracter.isdigit():
            digitos.append(int(caracter))
    
    # Si vamos a generar el dígito (no está incluido aún), 
    # añadimos un 0 temporal al final para la primera operación
    if not incluye_digito_verificador:
        digitos.append(0)
        
    checksum = 0
    
    # Invertimos la lista para recorrerla de derecha a izquierda.
    # Usamos 'enumerate' para saber tanto la posición (i) como el dígito.
    for i, digito in enumerate(reversed(digitos)):
        # 1. Buscamos el valor permutado según la posición del dígito (i % 8)
        fila_permutacion = i % 8
        valor_permutado = PERMUTATION_TABLE[fila_permutacion][digito]
        
        # 2. Mezclamos el checksum acumulado con el valor permutado
        checksum = MULTIPLICATION_TABLE[checksum][valor_permutado]
        
    return checksum


def generar_verhoeff(numero_str):
    """
    Toma un número base y le añade al final su dígito verificador.
    """
    # Calculamos el checksum base
    resultado_checksum = calcular_checksum(numero_str, incluye_digito_verificador=False)
    
    # Buscamos en la tabla inversa qué número neutraliza ese checksum
    digito_verificador = INVERSE_TABLE[resultado_checksum]
    
    # Retornamos el número original con el dígito pegado al final
    return numero_str + str(digito_verificador)


def validar_verhoeff(numero_con_digito):
    """
    Valida si un número entero que ya tiene el dígito de Verhoeff es correcto.
    Devuelve True si es válido, False si no lo es.
    """
    # Al procesar el número completo, si es correcto, el checksum final SIEMPRE debe ser 0
    return calcular_checksum(numero_con_digito, incluye_digito_verificador=True) == 0
