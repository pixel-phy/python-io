"""Ejercicio 08: Auditor de soluciones óptimas para el Solver (Filtro de bloques)

    Un solver de optimización corre en un clúster en la nube y devuelve un archivo de texto gigante con las coordenadas
    de asignación de miles de operarios a tareas: Trabajador:1->Tarea:4|Trabajador:2->Tarea:12... Debido a fallos
    en la memoria del clúster, los resultados pueden alterarse. El clúster genera un Checksum por cada bloque de 50
    asignaciones usando el método de Suma de verificación mediante XOR.

    - Escribe una función de alta velocidad que procese una lista de strings (cada string es una asignación). Debe 
    agruparlos en bloques de 50, calcular el checksum XOR acumulado de los caracteres de ese bloque y verificarlo
    contra una lista de checksums de control provistos por el clúster. Si un bloque falla, debes identificar qué 
    lote de 50 asignaciones debe volver a calcularse en el Solver.

    - Input de prueba conceptual: Simula un mini batch con bloques de tamaño 2.
        - Lista de asignaciones: []Lista de asignaciones: ["T1->M5", "T2->M1", "T3->M2", "T4->M8"]

        -Checksums de control esperados para cada bloque de 2: [115, 43] (Valores hipotéticos). """

def calcular_checksum_xor(bloque):
    """
    Calcula el XOR acumulado de todos los caracteres en un bloque de strings.
    
    Args:
        bloque (list): Lista de strings
    
    Returns:
        int: Checksum XOR de todos los caracteres
    """
    xor_acumulado = 0
    for cadena in bloque:
        for caracter in cadena:
            xor_acumulado ^= ord(caracter)
    return xor_acumulado


def validar_bloques(asignaciones, checksums_control, tamano_bloque=2):
    """
    Valida los bloques de asignaciones contra los checksums de control.
    
    Args:
        asignaciones (list): Lista de strings con asignaciones
        checksums_control (list): Lista de checksums esperados por bloque
        tamano_bloque (int): Tamaño de cada bloque
    
    Returns:
        dict: Resultado de la validación con:
            - 'bloques_fallidos': Lista de índices de bloques que fallaron
            - 'detalles': Lista con info de cada bloque (índice, asignaciones, checksum calculado, esperado, estado)
            - 'todos_validos': Booleano indicando si todos pasaron
    """
    resultados = {
        'bloques_fallidos': [],
        'detalles': [],
        'todos_validos': True
    }
    
    # Calcular cuántos bloques completos hay
    num_bloques = len(asignaciones) // tamano_bloque
    
    for i in range(num_bloques):
        # Extraer el bloque
        inicio = i * tamano_bloque
        fin = inicio + tamano_bloque
        bloque = asignaciones[inicio:fin]
        
        # Calcular checksum del bloque
        checksum_calculado = calcular_checksum_xor(bloque)
        
        # Obtener checksum esperado (si existe en la lista de control)
        checksum_esperado = checksums_control[i] if i < len(checksums_control) else None
        
        # Verificar
        es_valido = (checksum_calculado == checksum_esperado)
        
        # Guardar detalle
        detalle = {
            'indice_bloque': i,
            'bloque': bloque,
            'checksum_calculado': checksum_calculado,
            'checksum_esperado': checksum_esperado,
            'valido': es_valido
        }
        resultados['detalles'].append(detalle)
        
        # Si falla, guardar índice y marcar como no válido
        if not es_valido:
            resultados['bloques_fallidos'].append(i)
            resultados['todos_validos'] = False
    
    return resultados


# Función para validación manual
def calcular_checksum_xor_detallado(bloque):
    """
    Versión con detalles para depuración.
    """
    print(f"\nCalculando XOR para bloque: {bloque}")
    xor = 0
    for cadena in bloque:
        print(f"  Cadena: '{cadena}'")
        for caracter in cadena:
            valor = ord(caracter)
            xor ^= valor
            print(f"    '{caracter}' (ASCII: {valor:3d}) → XOR acumulado: {xor}")
    print(f"  Resultado final: {xor}")
    return xor


# Prueba

asignaciones = ["T1->M5", "T2->M1", "T3->M2", "T4->M8"]
checksums_control = [115, 43]  # Valores hipotéticos dados
tamano_bloque = 2

print(f"Asignaciones: {asignaciones}")
print(f"Checksums de control: {checksums_control}")
print(f"Tamaño de bloque: {tamano_bloque}")
print()

# Validar
resultado = validar_bloques(asignaciones, checksums_control, tamano_bloque)

# Mostrar resultados detallados
for detalle in resultado['detalles']:
    print(f"Bloque {detalle['indice_bloque']}: {detalle['bloque']}")
    print(f"  Checksum calculado: {detalle['checksum_calculado']}")
    print(f"  Checksum esperado:  {detalle['checksum_esperado']}")
    print(f"  ¿Válido? {detalle['valido']} {'Pasa' if detalle['valido'] else 'No pasa'}")
    print()

if resultado['todos_validos']:
    print("Todos los bloques son Válidos")
else:
    print(f" Bloques fallidos: {resultado['bloques_fallidos']}")
    print("  Estos bloques deben re-calcularse en el Solver.")

print("\n")

# Verificación manual
bloque_0 = ["T1->M5", "T2->M1"]
checksum_calculado = calcular_checksum_xor_detallado(bloque_0)

# Comprobamos que da 115 como en el enunciado
print(f"\n¿Coincide con el checksum esperado (115)? {checksum_calculado == 115}")
