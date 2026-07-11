"""Ejercicio 11: Verificación de Restricciones en Matriz de Asignación

En un problema de asignación de operarios a máquinas, representamos las conexiones mediante una matriz 
de adyacencia binaria (1 si el operario puede manejar la máquina, 0 si no).
Escribe un algoritmo eficiente que reciba esta matriz y verifique:
    1. Si existen "cuellos de botella" (máquinas que nadie puede operar).
    2. Si existen operarios subutilizados (operarios que no pueden manejar ninguna máquina).
    La función debe retornar los índices de los operarios y máquinas problemáticas en O(V²) o mejor. """

def verificar_asignacion(matriz_binaria, nombres_operarios=None, nombres_maquinas=None):
    """
    Verifica restricciones en una matriz de asignación binaria.
    
    Args:
        matriz_binaria (list): Matriz N x M donde N = operarios, M = máquinas
                               matriz[i][j] = 1 si operario i puede manejar máquina j, 0 si no
        nombres_operarios (list, optional): Nombres de los operarios
        nombres_maquinas (list, optional): Nombres de las máquinas
    
    Returns:
        dict: Diccionario con los resultados del análisis:
            - num_operarios: Número total de operarios (N)
            - num_maquinas: Número total de máquinas (M)
            - operarios_subutilizados: Lista de índices/nombres de operarios sin habilidades
            - maquinas_cuello_botella: Lista de índices/nombres de máquinas sin operarios
            - operarios_con_habilidades: Conteo de operarios con al menos una habilidad
            - maquinas_con_operarios: Conteo de máquinas con al menos un operario
            - densidad_asignacion: Porcentaje de conexiones posibles que existen
            - alertas: Lista de mensajes de advertencia
            - es_asignacion_valida: True si no hay problemas, False si hay cuellos de botella o subutilización
    """
    
    # Validar entrada
    if not matriz_binaria:
        return {
            'error': 'La matriz está vacía',
            'es_asignacion_valida': False,
            'alertas': ['La matriz de asignación está vacía']
        }
    
    N = len(matriz_binaria)  # Número de operarios
    M = len(matriz_binaria[0]) if N > 0 else 0  # Número de máquinas
    
    # Validar que todas las filas tengan la misma longitud
    for i, fila in enumerate(matriz_binaria):
        if len(fila) != M:
            return {
                'error': f'La fila {i} tiene {len(fila)} columnas, pero se esperaban {M}',
                'es_asignacion_valida': False,
                'alertas': ['Dimensiones inconsistentes en la matriz']
            }
    
    # Validar que la matriz sea binaria (0 o 1)
    for i in range(N):
        for j in range(M):
            if matriz_binaria[i][j] not in [0, 1]:
                return {
                    'error': f'Valor no binario en posición ({i}, {j}): {matriz_binaria[i][j]}',
                    'es_asignacion_valida': False,
                    'alertas': ['La matriz contiene valores no binarios']
                }
    
    # Configurar nombres por defecto si no se proporcionan
    if nombres_operarios is None:
        nombres_operarios = [f'Operario_{i}' for i in range(N)]
    elif len(nombres_operarios) != N:
        return {
            'error': f'El número de nombres de operarios ({len(nombres_operarios)}) no coincide con las filas ({N})',
            'es_asignacion_valida': False,
            'alertas': ['Inconsistencia en nombres de operarios']
        }
    
    if nombres_maquinas is None:
        nombres_maquinas = [f'Máquina_{j}' for j in range(M)]
    elif len(nombres_maquinas) != M:
        return {
            'error': f'El número de nombres de máquinas ({len(nombres_maquinas)}) no coincide con las columnas ({M})',
            'es_asignacion_valida': False,
            'alertas': ['Inconsistencia en nombres de máquinas']
        }
    
    # Análisis principal
    operarios_subutilizados = []
    maquinas_cuello_botella = []
    total_conexiones = 0
    
    # 1. Verificar operarios subutilizados (ninguna habilidad)
    for i in range(N):
        if sum(matriz_binaria[i]) == 0:
            operarios_subutilizados.append({
                'indice': i,
                'nombre': nombres_operarios[i]
            })
        else:
            total_conexiones += sum(matriz_binaria[i])
    
    # 2. Verificar máquinas cuello de botella (ningún operario)
    for j in range(M):
        columna = [matriz_binaria[i][j] for i in range(N)]
        if sum(columna) == 0:
            maquinas_cuello_botella.append({
                'indice': j,
                'nombre': nombres_maquinas[j]
            })
    
    # 3. Calcular estadísticas adicionales
    operarios_con_habilidades = N - len(operarios_subutilizados)
    maquinas_con_operarios = M - len(maquinas_cuello_botella)
    densidad = total_conexiones / (N * M) if (N * M) > 0 else 0
    
    # 4. Generar alertas
    alertas = []
    
    if operarios_subutilizados:
        nombres = [op['nombre'] for op in operarios_subutilizados]
        alertas.append(
            f"{len(operarios_subutilizados)} operario(s) subutilizado(s): {', '.join(nombres)}. "
            f"No pueden manejar ninguna máquina."
        )
    
    if maquinas_cuello_botella:
        nombres = [maq['nombre'] for maq in maquinas_cuello_botella]
        alertas.append(
            f"{len(maquinas_cuello_botella)} máquina(s) con cuello de botella: {', '.join(nombres)}. "
            f"Ningún operario puede operarlas."
        )
    
    if densidad < 0.3 and N > 0 and M > 0:
        alertas.append(
            f"La densidad de asignación es baja ({densidad*100:.1f}%). "
            f"Considerar capacitar operarios o redistribuir tareas."
        )
    
    if N < M:
        alertas.append(
            f"Hay menos operarios ({N}) que máquinas ({M}). "
            f"Algunas máquinas quedarán sin operario asignado."
        )
    
    # 5. Determinar si la asignación es válida
    es_valida = (len(operarios_subutilizados) == 0 and len(maquinas_cuello_botella) == 0)
    
    # 6. Construir resultado
    resultado = {
        'num_operarios': N,
        'num_maquinas': M,
        'operarios_subutilizados': operarios_subutilizados,
        'maquinas_cuello_botella': maquinas_cuello_botella,
        'operarios_con_habilidades': operarios_con_habilidades,
        'maquinas_con_operarios': maquinas_con_operarios,
        'total_conexiones': total_conexiones,
        'densidad_asignacion': densidad,
        'alertas': alertas,
        'es_asignacion_valida': es_valida
    }
    
    return resultado


# FUNCIÓN PARA VISUALIZAR LA MATRIZ DE ASIGNACIÓN
def imprimir_matriz_asignacion(matriz_binaria, nombres_operarios=None, nombres_maquinas=None):
    """Imprime la matriz de asignación de forma legible."""
    N = len(matriz_binaria)
    M = len(matriz_binaria[0]) if N > 0 else 0
    
    if nombres_maquinas is None:
        nombres_maquinas = [f'M{j}' for j in range(M)]
    
    # Encabezado
    print("    " + "  ".join(f"{m:>4}" for m in nombres_maquinas))
    print("   " + "-" * (5 + 6 * M))
    
    for i in range(N):
        nombre = nombres_operarios[i] if nombres_operarios else f'O{i}'
        fila = matriz_binaria[i]
        # Mostrar con colores o símbolos
        valores = []
        for val in fila:
            if val == 1:
                valores.append("BIEN")
            else:
                valores.append("MAL")
        print(f"{nombre:>3} |" + "  ".join(valores))


def imprimir_analisis_asignacion(resultado):
    """Imprime el análisis de asignación de forma clara."""
    print("ANÁLISIS DE ASIGNACIÓN OPERARIOS - MÁQUINAS")
    
    if 'error' in resultado:
        print(f"ERROR: {resultado['error']}")
        return
    
    print(f"Estadísticas:")
    print(f"  • Operarios totales: {resultado['num_operarios']}")
    print(f"  • Máquinas totales: {resultado['num_maquinas']}")
    print(f"  • Conexiones posibles: {resultado['num_operarios'] * resultado['num_maquinas']}")
    print(f"  • Conexiones existentes: {resultado['total_conexiones']}")
    print(f"  • Densidad de asignación: {resultado['densidad_asignacion']*100:.1f}%")
    print(f"  • Operarios con habilidades: {resultado['operarios_con_habilidades']}")
    print(f"  • Máquinas con operarios: {resultado['maquinas_con_operarios']}")
    
    print("\n")
    
    if resultado['alertas']:
        print("ALERTAS DETECTADAS:")
        for alerta in resultado['alertas']:
            print(f"  {alerta}")
    else:
        print("No se detectaron problemas en la asignación.")
    
    print("\n")
    
    if resultado['es_asignacion_valida']:
        print("ESTADO: Asignación VÁLIDA - Todos los operarios y máquinas están cubiertos")
    else:
        print("ESTADO: Asignación INVÁLIDA - Se requieren ajustes")
        if resultado['operarios_subutilizados']:
            print("   Operarios subutilizados (no pueden manejar ninguna máquina):")
            for op in resultado['operarios_subutilizados']:
                print(f"      - {op['nombre']} (índice {op['indice']})")
        if resultado['maquinas_cuello_botella']:
            print("   Máquinas cuello de botella (ningún operario puede operarlas):")
            for maq in resultado['maquinas_cuello_botella']:
                print(f"      - {maq['nombre']} (índice {maq['indice']})")

# Prueba
if __name__ == "__main__":
    
    print("Caso 1: ASIGNACIÓN VÁLIDA (completa)")
    
    # Matriz 4x4 con asignación válida (cada operario puede operar al menos una máquina)
    matriz_valida = [
        [1, 1, 0, 0],  # Operario 0: máquinas 0,1
        [0, 1, 1, 0],  # Operario 1: máquinas 1,2
        [1, 0, 0, 1],  # Operario 2: máquinas 0,3
        [0, 1, 1, 1]   # Operario 3: máquinas 1,2,3
    ]
    
    operarios = ['Ana', 'Carlos', 'María', 'Luis']
    maquinas = ['Torno A', 'Fresadora B', 'Cizalla C', 'Soldador D']
    
    print("Matriz de asignación:")
    imprimir_matriz_asignacion(matriz_valida, operarios, maquinas)
    print()
    
    resultado1 = verificar_asignacion(matriz_valida, operarios, maquinas)
    imprimir_analisis_asignacion(resultado1)
    
    print("\n\n")
    
    print("Caso 2: ASIGNACIÓN CON PROBLEMAS")
    
    # Matriz 4x3 con problemas
    matriz_problemas = [
        [1, 0, 0],  # Ana: solo máquina 0
        [0, 0, 0],  # Carlos: ¡subutilizado! (no puede operar ninguna)
        [1, 1, 0],  # María: máquinas 0 y 1
        [0, 1, 0]   # Luis: máquina 1
    ]
    # Máquina 2 es cuello de botella (nadie puede operarla)
    
    operarios2 = ['Ana', 'Carlos', 'María', 'Luis']
    maquinas2 = ['Torno A', 'Fresadora B', 'Impresora 3D']
    
    print("Matriz de asignación:")
    imprimir_matriz_asignacion(matriz_problemas, operarios2, maquinas2)
    print()
    
    resultado2 = verificar_asignacion(matriz_problemas, operarios2, maquinas2)
    imprimir_analisis_asignacion(resultado2)
    
    print("\n\n")
    
    print("Caso 3: MATRIZ DISPERSA (baja densidad)")
    
    import random
    random.seed(42)  # Para reproducibilidad
    
    # Generar matriz 6x6 con ~20% de conexiones
    matriz_dispersa = []
    for i in range(6):
        fila = [1 if random.random() < 0.2 else 0 for _ in range(6)]
        # Asegurar que al menos el operario i pueda operar su máquina correspondiente
        fila[i] = 1
        matriz_dispersa.append(fila)
    
    resultado3 = verificar_asignacion(matriz_dispersa)
    imprimir_analisis_asignacion(resultado3)
    
    print("\n\n")
    
    print("Caso 4: ASIGNACIÓN CON NOMBRES PERSONALIZADOS")
    
    # Escenario con más máquinas que operarios
    matriz_asimetrica = [
        [1, 1, 0, 1, 0],  # Operario 0
        [0, 1, 1, 0, 1],  # Operario 1
        [1, 0, 0, 1, 0],  # Operario 2
    ]
    
    nombres_op = ['Pedro', 'Juan', 'Sofía']
    nombres_maq = ['M1', 'M2', 'M3', 'M4', 'M5']
    
    resultado4 = verificar_asignacion(matriz_asimetrica, nombres_op, nombres_maq)
    imprimir_analisis_asignacion(resultado4)
