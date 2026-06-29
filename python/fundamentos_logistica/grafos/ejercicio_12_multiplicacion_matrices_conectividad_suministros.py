""" Ejercicio 12: Multiplicacioń de Matrices para Conectividad de Suministro

En IO, si elevas una matriz de adyacencia binaria A a la potencia k(A^k), el resultado en la celda [i][j]
te dice cuántos caminos de exactamente k pasos existen entre el nodo i y el nodo j. Implementa una función
    que reciba una matriz de adyacencia binaria que representa vuelos de carga entre hubs logísticos
    y un entero k. Retorna la matriz resultante que muestre cuántas rutas de suministro alternativas existen
    con exactamente k escalas/pasos directos. """

def multiplicar_matrices(A, B):
    """
    Multiplica dos matrices cuadradas A y B.
    
    Args:
        A (list): Matriz N x N
        B (list): Matriz N x N
    
    Returns:
        list: Matriz resultante N x N (A * B)
    
    Raises:
        ValueError: Si las matrices no son cuadradas o no tienen dimensiones compatibles
    """
    n = len(A)
    
    # Validar que sean matrices cuadradas
    if n == 0:
        return []
    
    # Verificar dimensiones
    if len(A[0]) != n or len(B) != n or len(B[0]) != n:
        raise ValueError("Ambas matrices deben ser cuadradas y del mismo tamaño")
    
    # Inicializar matriz resultado con ceros
    C = [[0] * n for _ in range(n)]
    
    # Multiplicación de matrices (algoritmo clásico)
    for i in range(n):
        for k in range(n):
            if A[i][k] != 0:  # Optimización: solo si el elemento es distinto de cero
                for j in range(n):
                    C[i][j] += A[i][k] * B[k][j]
    
    return C


def potencia_matriz(A, k, metodo='exponenciacion'):
    """
    Calcula la potencia k-ésima de una matriz A.
    
    Args:
        A (list): Matriz de adyacencia binaria N x N
        k (int): Potencia a la que se eleva la matriz (k >= 0)
        metodo (str): 'exponenciacion' (default) o 'iterativo'
    
    Returns:
        list: Matriz A^k
    
    Raises:
        ValueError: Si k es negativo o la matriz no es cuadrada
    """
    n = len(A)
    
    if n == 0:
        return []
    
    if k < 0:
        raise ValueError("k debe ser un entero no negativo")
    
    # Validar que sea matriz cuadrada
    for fila in A:
        if len(fila) != n:
            raise ValueError("La matriz debe ser cuadrada")
    
    # Validar que sea binaria (opcional, pero útil)
    for i in range(n):
        for j in range(n):
            if A[i][j] not in [0, 1]:
                print(f"Advertencia: La matriz contiene valores no binarios en ({i},{j}) = {A[i][j]}")
    
    # Caso base: A^0 = Matriz identidad
    if k == 0:
        return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    
    # Caso base: A^1 = A
    if k == 1:
        return [fila[:] for fila in A]  # Copia profunda
    
    # Usar método de exponenciación rápida (recomendado para k grandes)
    if metodo == 'exponenciacion':
        return potencia_matriz_exponenciacion(A, k)
    else:
        # Método iterativo (simple pero menos eficiente)
        return potencia_matriz_iterativa(A, k)


def potencia_matriz_exponenciacion(A, k):
    """
    Calcula A^k usando exponenciación rápida (divide y vencerás).
    Complejidad: O(N^3 * log k)
    
    Args:
        A (list): Matriz N x N
        k (int): Potencia (k >= 1)
    
    Returns:
        list: Matriz A^k
    """
    if k == 0:
        n = len(A)
        return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    
    if k == 1:
        return [fila[:] for fila in A]
    
    # Exponenciación rápida recursiva
    if k % 2 == 0:
        # Si k es par: A^k = (A^(k/2))^2
        mitad = potencia_matriz_exponenciacion(A, k // 2)
        return multiplicar_matrices(mitad, mitad)
    else:
        # Si k es impar: A^k = A * A^(k-1)
        return multiplicar_matrices(A, potencia_matriz_exponenciacion(A, k - 1))


def potencia_matriz_iterativa(A, k):
    """
    Calcula A^k multiplicando iterativamente A * A * ... * A (k veces).
    Complejidad: O(N^3 * k)
    
    Args:
        A (list): Matriz N x N
        k (int): Potencia (k >= 1)
    
    Returns:
        list: Matriz A^k
    """
    n = len(A)
    resultado = [fila[:] for fila in A]  # Copia de A (A^1)
    
    for _ in range(2, k + 1):
        resultado = multiplicar_matrices(resultado, A)
    
    return resultado


def rutas_conectividad(A, k, metodo='exponenciacion'):
    """
    Calcula el número de rutas de exactamente k pasos entre nodos.
    Función principal para el ejercicio.
    
    Args:
        A (list): Matriz de adyacencia binaria N x N
        k (int): Número de pasos/escalas
        metodo (str): 'exponenciacion' o 'iterativo'
    
    Returns:
        dict: Diccionario con la matriz resultado y métricas adicionales
    """
    n = len(A)
    
    # Validaciones
    if n == 0:
        return {'error': 'La matriz está vacía'}
    
    if k < 0:
        return {'error': 'k debe ser un entero no negativo'}
    
    # Calcular la potencia de la matriz
    try:
        matriz_resultado = potencia_matriz(A, k, metodo)
    except Exception as e:
        return {'error': f'Error al calcular la potencia: {str(e)}'}
    
    # Calcular métricas adicionales
    total_caminos = sum(sum(fila) for fila in matriz_resultado)
    
    # Encontrar los caminos más largos
    max_caminos = max(max(fila) for fila in matriz_resultado) if n > 0 else 0
    
    # Encontrar pares con más caminos alternativos
    pares_max = []
    for i in range(n):
        for j in range(n):
            if matriz_resultado[i][j] == max_caminos and max_caminos > 0:
                pares_max.append((i, j))
    
    # Verificar conectividad (si todos los pares tienen al menos un camino)
    todos_conectados = all(matriz_resultado[i][j] > 0 for i in range(n) for j in range(n))
    
    return {
        'matriz': matriz_resultado,
        'k': k,
        'n': n,
        'total_caminos': total_caminos,
        'max_caminos_alternativos': max_caminos,
        'pares_con_mas_caminos': pares_max[:5],  # Top 5 pares
        'todos_conectados': todos_conectados,
        'densidad_caminos': total_caminos / (n * n) if n > 0 else 0
    }


# FUNCIONES DE VISUALIZACIÓN
def imprimir_matriz_conectividad(resultado, nombres_nodos=None, mostrar_ceros=True):
    """
    Imprime la matriz de conectividad de forma legible.
    
    Args:
        resultado (dict): Resultado de la función rutas_conectividad
        nombres_nodos (list, optional): Nombres de los nodos
        mostrar_ceros (bool): Si mostrar los ceros o espacios vacíos
    """
    if 'error' in resultado:
        print(f"ERROR: {resultado['error']}")
        return
    
    matriz = resultado['matriz']
    n = resultado['n']
    k = resultado['k']
    
    if nombres_nodos is None:
        nombres_nodos = [f'N{i}' for i in range(n)]
    elif len(nombres_nodos) != n:
        print(f"El número de nombres ({len(nombres_nodos)}) no coincide con la matriz ({n})")
        nombres_nodos = [f'N{i}' for i in range(n)]
    
    print(f"MATRIZ DE CONECTIVIDAD - RUTAS DE EXACTAMENTE {k} PASOS")
    
    # Encabezado
    print("      " + "  ".join(f"{nombre:>6}" for nombre in nombres_nodos))
    print("   " + "-" * (8 + 8 * n))
    
    for i in range(n):
        fila = matriz[i]
        valores = []
        for j, val in enumerate(fila):
            if val == 0 and not mostrar_ceros:
                valores.append("     ·")
            else:
                # Resaltar caminos que no existen (0)
                if val == 0:
                    valores.append(f"  {val:>3} ")
                else:
                    # Color opcional según cantidad
                    if val <= 1:
                        valores.append(f"  {val:>3} ")
                    elif val <= 3:
                        valores.append(f"  {val:>3}*")
                    elif val <= 6:
                        valores.append(f"  {val:>3}**")
                    else:
                        valores.append(f"  {val:>3}***")
        
        print(f"{nombres_nodos[i]:>3} |" + "  ".join(valores))
    
    print(f"Estadísticas:")
    print(f"  • Total de caminos de {k} pasos: {resultado['total_caminos']}")
    print(f"  • Máximo de caminos alternativos entre un par: {resultado['max_caminos_alternativos']}")
    print(f"  • Densidad de caminos: {resultado['densidad_caminos']*100:.1f}%")
    
    if resultado['todos_conectados']:
        print(" Todos los pares de nodos están conectados con al menos un camino")
    else:
        print(" No todos los pares de nodos están conectados")
    
    if resultado['pares_con_mas_caminos']:
        print(f" Pares con más caminos alternativos (top {len(resultado['pares_con_mas_caminos'])}):")
        for i, j in resultado['pares_con_mas_caminos'][:3]:
            print(f"     • {nombres_nodos[i]} → {nombres_nodos[j]}: {matriz[i][j]} caminos")
    
def imprimir_evolucion_caminos(A, max_k=4):
    """
    Muestra la evolución de la conectividad para diferentes valores de k.
    """
    print("EVOLUCIÓN DE CONECTIVIDAD POR NÚMERO DE PASOS")
    
    for k in range(1, max_k + 1):
        resultado = rutas_conectividad(A, k)
        total = resultado['total_caminos']
        max_caminos = resultado['max_caminos_alternativos']
        print(f"  k = {k}: {total} caminos totales, máximo {max_caminos} caminos entre un par")
        
        # Mostrar evolución con barras
        barra = "█" * min(50, int(total / 10))
        print(f"         [{barra:<50}] {total}")
    
    print("=" * 80)


# Pruebas 
if __name__ == "__main__":
    
    print("Prueba 1: RED LOGÍSTICA BÁSICA (3 hubs)")
    
    # Red logística simple: vuelos entre 3 hubs
    # A[0][1] = 1: Hay vuelo directo del hub 0 al 1
    red_logistica = [
        [0, 1, 0],  # Hub 0 → Hub 1
        [0, 0, 1],  # Hub 1 → Hub 2
        [1, 0, 0]   # Hub 2 → Hub 0 (ciclo)
    ]
    
    nombres_hubs = ['Madrid', 'Barcelona', 'Valencia']
    
    print("Matriz de adyacencia original (vuelos directos):")
    imprimir_matriz_conectividad({
        'matriz': red_logistica,
        'n': 3,
        'k': 1,
        'total_caminos': 3,
        'max_caminos_alternativos': 1,
        'densidad_caminos': 3/9,
        'todos_conectados': False,
        'pares_con_mas_caminos': []
    }, nombres_hubs)
    
    print("\n")
    
    # Calcular A^2, A^3
    for k in [2, 3]:
        print(f"\n--- Rutas con exactamente {k} escalas ---")
        resultado = rutas_conectividad(red_logistica, k)
        imprimir_matriz_conectividad(resultado, nombres_hubs)
        print()
    
    print("\n")
    
    print("Prueba 2: RED COMPLETA CON 4 NODOS")
    
    # Red completamente conectada (todos los vuelos directos posibles)
    red_completa = [
        [0, 1, 1, 1],
        [1, 0, 1, 1],
        [1, 1, 0, 1],
        [1, 1, 1, 0]
    ]
    
    nombres_nodos = ['A', 'B', 'C', 'D']
    
    # Mostrar A^2 (caminos de 2 pasos)
    resultado_k2 = rutas_conectividad(red_completa, 2)
    imprimir_matriz_conectividad(resultado_k2, nombres_nodos)
    
    print("\n")
    
    # Evolución de caminos
    imprimir_evolucion_caminos(red_completa, max_k=4)
    
    print("\n")
    
    print("Prueba 3: RED CON MUCHAS RUTAS ALTERNATIVAS")

    
    # Red donde hay múltiples caminos alternativos
    red_alternativas = [
        [0, 1, 1, 0],
        [1, 0, 1, 1],
        [1, 1, 0, 1],
        [0, 1, 1, 0]
    ]
    
    nombres = ['Centro1', 'Centro2', 'Centro3', 'Centro4']
    
    resultado = rutas_conectividad(red_alternativas, 3)
    imprimir_matriz_conectividad(resultado, nombres)
    
    print("\n")
    
    print("Prueba 4: COMPARACIÓN DE MÉTODOS")
    
    import time
    
    # Matriz más grande para probar rendimiento
    red_mediana = [
        [0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1],
        [1, 0, 0, 1, 0]
    ]
    
    k = 5
    
    # Método exponenciación rápida
    start = time.time()
    result_exp = rutas_conectividad(red_mediana, k, metodo='exponenciacion')
    time_exp = time.time() - start
    
    # Método iterativo
    start = time.time()
    result_iter = rutas_conectividad(red_mediana, k, metodo='iterativo')
    time_iter = time.time() - start
    
    print(f"Comparación de rendimiento para k = {k}:")
    print(f"  Exponenciación rápida: {time_exp*1000:.3f} ms")
    print(f"  Método iterativo: {time_iter*1000:.3f} ms")
    print(f"  Mejora: {(time_iter/time_exp):.2f}x más rápido")
    
    print("\n")
    
    print("Prueba 5: INTERPRETACIÓN LOGÍSTICA")
    
    # Red con centros de distribución reales
    red_real = {
        0: [1, 2],      # Madrid → Barcelona, Valencia
        1: [0, 2, 3],   # Barcelona → Madrid, Valencia, Zaragoza
        2: [0, 1],      # Valencia → Madrid, Barcelona
        3: [1]          # Zaragoza → Barcelona
    }
    
    # Convertir a matriz
    n = 4
    matriz_real = [[0]*n for _ in range(n)]
    for origen, destinos in red_real.items():
        for destino in destinos:
            matriz_real[origen][destino] = 1
    
    ciudades = ['Madrid', 'Barcelona', 'Valencia', 'Zaragoza']
    
    print("Red de hubs logísticos:")
    for ciudad, conexiones in red_real.items():
        print(f"  {ciudades[ciudad]} → {[ciudades[d] for d in conexiones]}")
    
    print("\n--- Rutas de suministro con 2 escalas ---")
    resultado_real = rutas_conectividad(matriz_real, 2)
    imprimir_matriz_conectividad(resultado_real, ciudades)
    
    print("\n--- Interpretación ---")
    for i in range(n):
        for j in range(n):
            caminos = resultado_real['matriz'][i][j]
            if caminos > 0 and i != j:
                print(f"De {ciudades[i]} a {ciudades[j]}: {caminos} rutas alternativas con 2 escalas")
