"""Ejercicio 03: el despachador de Carga Blindado contra Transposiciones

Te entregan un batch masivo de registros de contenedores con el formato "ED_FACTURA,PESO_KG".
    Algunos IDs de factura fueron mal digitados por el personal de rampa. Si metes un peso 
    al ID de factura equivocado, alterarás el modelo de Carga de Aviones/Contenedores.

    - Escribir una función que procese esta lista de strings. Debe filtrar y separar los registros 
en dos listas: una con las cargas cuyos IDs de factura pasen la validación de Verhoeff (listas 
para el Solver) y otra lista con los registros corruptos para auditoría. Además, retrona la cantidad
de peso total atrapado en los bloques corruptos.

Input de entrada: ["1234561,1500", "1235461,2200", "6543210,850"] (Nota: El primer ID 
es el del ejercicio 1 con su verificador; el segundo tiene un error de transposición de los números 3 y 5.) """

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
    c = 0
    for i, car in enumerate(reversed(id_base)):
        val_p = TABLA_P[(i + 1) % 8][int(car)]
        c = TABLA_D[c][val_p]
    return VECTOR_INV[c]

def validar_verhoeff(codigo_completo: str) -> bool:
    """Valida un código completo (incluyendo dígito verificador) usando Verhoeff"""
    c = 0
    for i, car in enumerate(reversed(codigo_completo)):
        val_p = TABLA_P[(i + 1) % 8][int(car)]
        c = TABLA_D[c][val_p]
    return c == 0

def procesar_batch_contenedores(registros: list) -> tuple:
    """
    Procesa un batch de registros de contenedores.
    
    Args:
        registros: Lista de strings con formato "ID_FACTURA,PESO_KG"
    
    Returns:
        tuple: (lista_validos, lista_corruptos, peso_total_corruptos)
    """
    lista_validos = []
    lista_corruptos = []
    peso_total_corruptos = 0
    
    for registro in registros:
        # Separar ID y peso
        partes = registro.split(',')
        if len(partes) != 2:
            # Formato incorrecto, lo tratamos como corrupto
            lista_corruptos.append(registro)
            continue
        
        id_factura = partes[0].strip()
        try:
            peso = float(partes[1].strip())
        except ValueError:
            # Peso no es numérico, lo tratamos como corrupto
            lista_corruptos.append(registro)
            continue
        
        # Validar el ID de factura con Verhoeff
        if validar_verhoeff(id_factura):
            lista_validos.append(registro)
        else:
            lista_corruptos.append(registro)
            peso_total_corruptos += peso
    
    return lista_validos, lista_corruptos, peso_total_corruptos

# Prueba:
registros = ["1234561,1500", "1235461,2200", "6543210,850"]

validos, corruptos, peso_corrupto = procesar_batch_contenedores(registros)

print("\nRegistros válidos:")
for reg in validos:
    print(f"{reg}")

print(f"\nRegistros corruptos:")
for reg in corruptos:
    print(f"{reg}")

print(f"\nPeso total atrapado en los bloques corrruptos: {peso_corrupto:.2f} kg")

# Verificación de los IDs
for registro in registros:
    id_factura = registro.split(',')[0]
    es_valido = validar_verhoeff(id_factura)
    print(f"ID: {id_factura} {'Válido' if es_valido else 'Inválido'}")
