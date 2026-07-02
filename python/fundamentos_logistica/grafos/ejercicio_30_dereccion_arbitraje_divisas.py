"""Ejercicio 30: Detección de Arbitraje de divisas (Ciclos negativos)

En la mesa de dinero de una empresa multinacional de commodities, se evalúan tasas de cambio entre monedas.
Un 'ciclo de arbitraje' ocurre cuando puedes cambiar Moneda A -> Moneda B -> Moneda C -> Moneda A y terminar 
con más dinero del que empezaste. Esto es equivalente a un ciclo de costo negativo en un grafo.

    Implementa el algoritmo de Bellman - Ford para detectar si existe una oportunidad de arbitraje en una
    matriz de tasas de cambio dada. El programa debe retornar el ciclo exacto de monedas para ejecutar 
    la operación financiera. """

import math

def detectar_arbitraje(matriz_tasas, monedas):
    """
    Detecta oportunidades de arbitraje usando Bellman-Ford.
    
    Args:
        matriz_tasas: Matriz n x n con tasas de cambio
        monedas: Lista de nombres de monedas
    
    Returns:
        Tupla (ciclo, ganancia) donde ciclo es lista de monedas y ganancia es el factor
    """
    n = len(monedas)
    
    # Convertir tasas a pesos logarítmicos
    # peso = -log(tasa)
    # Un ciclo negativo en pesos = oportunidad de arbitraje
    pesos = [[0.0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            if i == j:
                pesos[i][j] = 0.0
            elif matriz_tasas[i][j] > 0:
                pesos[i][j] = -math.log(matriz_tasas[i][j])
            else:
                pesos[i][j] = float('inf')
    
    # Inicializar distancias y padres
    dist = [float('inf')] * n
    padre = [-1] * n
    
    # Elegir un nodo fuente (podemos usar cualquier nodo)
    # Para detectar ciclos negativos en cualquier parte del grafo,
    # inicializamos todas las distancias a 0
    dist = [0.0] * n
    
    # Ejecutar Bellman-Ford por n-1 iteraciones
    for _ in range(n - 1):
        for i in range(n):
            for j in range(n):
                if pesos[i][j] != float('inf') and dist[i] + pesos[i][j] < dist[j]:
                    dist[j] = dist[i] + pesos[i][j]
                    padre[j] = i
    
    # Verificar si existe ciclo negativo en la n-ésima iteración
    ciclo_encontrado = False
    nodo_inicio = -1
    
    for i in range(n):
        for j in range(n):
            if pesos[i][j] != float('inf') and dist[i] + pesos[i][j] < dist[j]:
                ciclo_encontrado = True
                nodo_inicio = j
                break
        if ciclo_encontrado:
            break
    
    if not ciclo_encontrado:
        return None, 1.0
    
    # Extraer el ciclo
    # Primero, asegurarnos de que nodo_inicio esté en el ciclo
    # Hacer n iteraciones para asegurar que estamos en el ciclo
    for _ in range(n):
        nodo_inicio = padre[nodo_inicio]
    
    # Reconstruir ciclo
    ciclo_nodos = []
    nodo_actual = nodo_inicio
    
    while True:
        ciclo_nodos.append(nodo_actual)
        nodo_actual = padre[nodo_actual]
        if nodo_actual == nodo_inicio:
            break
    
    # Invertir para tener orden correcto
    ciclo_nodos.reverse()
    ciclo_nodos.append(ciclo_nodos[0])  # Cerrar el ciclo
    
    # Calcular la ganancia real del arbitraje
    ganancia = 1.0
    for i in range(len(ciclo_nodos) - 1):
        origen = ciclo_nodos[i]
        destino = ciclo_nodos[i + 1]
        ganancia *= matriz_tasas[origen][destino]
    
    # Convertir índices a nombres de monedas
    ciclo_monedas = [monedas[idx] for idx in ciclo_nodos]
    
    return ciclo_monedas, ganancia

def mostrar_arbitraje(ciclo, ganancia):
    """Muestra la oportunidad de arbitraje de forma clara."""
    if ciclo is None:
        print("No se detectaron oportunidades de arbitraje")
        return
    
    print("\nOPORTUNIDAD DE ARBITRAJE DETECTADA")
    print("-" * 50)
    print(f"Ciclo: {' -> '.join(ciclo)}")
    print(f"Ganancia potencial: {ganancia:.6f} ({(ganancia-1)*100:.2f}% de beneficio)")
    
    print("\nDesglose de la operacion:")
    for i in range(len(ciclo) - 1):
        origen = ciclo[i]
        destino = ciclo[i + 1]
        # Encontrar la tasa en la matriz original (necesitamos reconstruirla)
        # Para este ejemplo, asumimos que tenemos acceso a la matriz original
        # Mostramos el detalle conceptual

def generar_matriz_tasas_ejemplo():
    """Genera una matriz de tasas de cambio de ejemplo."""
    # Monedas: USD, EUR, GBP, JPY, CHF
    # Tasa[i][j] = cantidad de moneda j por 1 unidad de moneda i
    return [
        [1.0, 0.85, 0.75, 110.0, 0.92],   # USD
        [1.18, 1.0, 0.88, 130.0, 1.08],   # EUR
        [1.33, 1.14, 1.0, 147.0, 1.22],   # GBP
        [0.0091, 0.0077, 0.0068, 1.0, 0.0084],  # JPY
        [1.09, 0.93, 0.82, 119.0, 1.0]    # CHF
    ]

# ===== CASOS DE PRUEBA =====

print("=" * 80)
print("DETECCION DE ARBITRAJE DE DIVISAS (BELLMAN-FORD)")
print("=" * 80)

# Caso 1: Matriz con oportunidad de arbitraje
print("\nCaso 1: Mercado con oportunidad de arbitraje")
print("-" * 50)

monedas = ['USD', 'EUR', 'GBP', 'JPY', 'CHF']

# Matriz con una oportunidad de arbitraje artificial
# Crearemos un ciclo USD -> EUR -> GBP -> USD con ganancia
matriz_arbitraje = [
    [1.0, 0.85, 0.75, 110.0, 0.92],   # USD
    [1.18, 1.0, 0.90, 130.0, 1.08],   # EUR (tasa EUR->GBP aumentada de 0.88 a 0.90)
    [1.35, 1.14, 1.0, 147.0, 1.22],   # GBP (tasa GBP->USD aumentada de 1.33 a 1.35)
    [0.0091, 0.0077, 0.0068, 1.0, 0.0084],  # JPY
    [1.09, 0.93, 0.82, 119.0, 1.0]    # CHF
]

ciclo, ganancia = detectar_arbitraje(matriz_arbitraje, monedas)
mostrar_arbitraje(ciclo, ganancia)

if ciclo:
    print("\nVerificacion del arbitraje:")
    print("Inicio con 1 USD")
    for i in range(len(ciclo) - 1):
        origen = ciclo[i]
        destino = ciclo[i + 1]
        idx_origen = monedas.index(origen)
        idx_destino = monedas.index(destino)
        tasa = matriz_arbitraje[idx_origen][idx_destino]
        print(f"  {origen} -> {destino}: 1 {origen} * {tasa:.4f} = {tasa:.4f} {destino}")

# Caso 2: Mercado sin arbitraje
print("\nCaso 2: Mercado sin oportunidad de arbitraje")
print("-" * 50)

# Matriz sin arbitraje (tasas consistentes)
matriz_sin_arbitraje = [
    [1.0, 0.85, 0.75, 110.0, 0.92],
    [1.1765, 1.0, 0.88, 129.4, 1.0824],
    [1.3333, 1.1364, 1.0, 146.7, 1.2273],
    [0.0091, 0.0077, 0.0068, 1.0, 0.0084],
    [1.0870, 0.9239, 0.8148, 119.0, 1.0]
]

ciclo, ganancia = detectar_arbitraje(matriz_sin_arbitraje, monedas)
mostrar_arbitraje(ciclo, ganancia)

# Caso 3: Arbitraje triangular clásico (USD -> EUR -> GBP -> USD)
print("\nCaso 3: Arbitraje triangular clasico")
print("-" * 50)

matriz_triangular = [
    [1.0, 0.85, 0.75, 110.0, 0.92],
    [1.18, 1.0, 0.88, 130.0, 1.08],
    [1.34, 1.14, 1.0, 147.0, 1.22],   # GBP->USD = 1.34 (ligeramente superior)
    [0.0091, 0.0077, 0.0068, 1.0, 0.0084],
    [1.09, 0.93, 0.82, 119.0, 1.0]
]

ciclo, ganancia = detectar_arbitraje(matriz_triangular, monedas)
mostrar_arbitraje(ciclo, ganancia)

if ciclo:
    print("\nEstrategia de arbitraje:")
    print("1. Cambiar USD a EUR: 1.0 * 0.85 = 0.85 EUR")
    print("2. Cambiar EUR a GBP: 0.85 * 0.88 = 0.748 GBP")
    print("3. Cambiar GBP a USD: 0.748 * 1.34 = 1.00232 USD")
    print(f"   Beneficio: {(1.00232 - 1.0) * 100:.2f}%")

# Caso 4: Arbitraje con 4 monedas
print("\nCaso 4: Arbitraje de 4 monedas (USD -> EUR -> GBP -> JPY -> USD)")
print("-" * 50)

matriz_4_monedas = [
    [1.0, 0.85, 0.75, 110.0, 0.92],
    [1.18, 1.0, 0.88, 132.0, 1.08],   # EUR->JPY = 132 (oportunidad)
    [1.33, 1.14, 1.0, 148.0, 1.22],   # GBP->JPY = 148
    [0.0093, 0.0079, 0.0070, 1.0, 0.0086], # JPY->USD = 0.0093
    [1.09, 0.93, 0.82, 119.0, 1.0]
]

ciclo, ganancia = detectar_arbitraje(matriz_4_monedas, monedas)
mostrar_arbitraje(ciclo, ganancia)

# Caso 5: Ejemplo con criptomonedas
print("\nCaso 5: Arbitraje en criptomonedas")
print("-" * 50)

criptos = ['BTC', 'ETH', 'USDT', 'XRP']
matriz_cripto = [
    [1.0, 16.5, 28000, 45000],    # BTC
    [0.0606, 1.0, 1700, 2700],    # ETH
    [0.0000357, 0.000588, 1.0, 1.6],  # USDT
    [0.0000222, 0.000370, 0.625, 1.0]  # XRP
]

ciclo, ganancia = detectar_arbitraje(matriz_cripto, criptos)
mostrar_arbitraje(ciclo, ganancia)

if ciclo:
    print("\nOportunidad detectada en criptomonedas:")
    for i in range(len(ciclo) - 1):
        print(f"  {ciclo[i]} -> {ciclo[i+1]}", end="")
        if i < len(ciclo) - 2:
            print(" -> ", end="")
    print(f"\nGanancia teorica: {ganancia:.6f}x")

# Caso 6: Análisis de sensibilidad
print("\nCaso 6: Analisis de sensibilidad del arbitraje")
print("-" * 50)

# Mostrar cómo pequeñas variaciones afectan el arbitraje
tasa_base = 1.33  # GBP->USD base
print(f"Tasa GBP->USD base: {tasa_base}")

for delta in [0.001, 0.002, 0.005, 0.01]:
    tasa_modificada = tasa_base + delta
    matriz_sensibilidad = [
        [1.0, 0.85, 0.75, 110.0, 0.92],
        [1.18, 1.0, 0.88, 130.0, 1.08],
        [tasa_modificada, 1.14, 1.0, 147.0, 1.22],
        [0.0091, 0.0077, 0.0068, 1.0, 0.0084],
        [1.09, 0.93, 0.82, 119.0, 1.0]
    ]
    
    ciclo, ganancia = detectar_arbitraje(matriz_sensibilidad, monedas)
    if ciclo:
        print(f"  Tasa {tasa_modificada:.3f}: Arbitraje detectable con ganancia {ganancia:.6f}")
    else:
        print(f"  Tasa {tasa_modificada:.3f}: Sin arbitraje")
