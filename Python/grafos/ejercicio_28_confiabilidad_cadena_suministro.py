"""Ejercicio 28: El Camino "Más seguro" (Confiabilidad de Cadena de Suministro)

En logística marítima, cada tramo entre puertos tiene una "Probabilidad de éxito/llegada a tiempo" 
(un valor entre 0 y 1). La confiabilidad total de una ruta es la multiplicación de las probabilidades
de sus tramos. Queremos garantizar la confiabilidad.
    - Diseña un algoritmo basado en Dijkstra para encontrar la ruta con la máxima confiabilidad de 
    origen a destino. """

import heapq
import math

def encontrar_ruta_mas_confiable(grafo, origen, destino):
    """
    Encuentra la ruta con máxima confiabilidad usando logaritmos.
    
    Args:
        grafo: Diccionario {nodo: [(vecino, probabilidad)]}
        origen: Nodo de inicio
        destino: Nodo final
    
    Returns:
        Tupla (confiabilidad_total, [ruta])
    """
    # Transformar probabilidades a costos logarítmicos
    # costo = -log(probabilidad)
    # Minimizar costo = Maximizar probabilidad
    
    # Inicializar Dijkstra
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[origen] = 0  # -log(1) = 0
    padres = {origen: None}
    cola_prioridad = [(0, origen)]
    visitados = set()
    
    while cola_prioridad:
        costo_actual, nodo_actual = heapq.heappop(cola_prioridad)
        
        if nodo_actual in visitados:
            continue
        
        visitados.add(nodo_actual)
        
        # Si llegamos al destino, podemos parar
        if nodo_actual == destino:
            break
        
        # Explorar vecinos
        for vecino, probabilidad in grafo.get(nodo_actual, []):
            if vecino in visitados:
                continue
            
            # Calcular nuevo costo logarítmico
            nuevo_costo = costo_actual - math.log(probabilidad)
            
            if nuevo_costo < distancias[vecino]:
                distancias[vecino] = nuevo_costo
                padres[vecino] = nodo_actual
                heapq.heappush(cola_prioridad, (nuevo_costo, vecino))
    
    # Verificar si hay ruta
    if distancias[destino] == float('inf'):
        return 0.0, []
    
    # Reconstruir ruta
    ruta = []
    nodo = destino
    while nodo is not None:
        ruta.append(nodo)
        nodo = padres.get(nodo)
    ruta.reverse()
    
    # Calcular confiabilidad real (multiplicación de probabilidades)
    confiabilidad = math.exp(-distancias[destino])
    
    return confiabilidad, ruta

def mostrar_ruta_confiable(ruta, confiabilidad, grafo):
    """Muestra la ruta con detalles de confiabilidad."""
    if not ruta:
        print("No se encontró ruta")
        return
    
    print(f"\nRuta más confiable encontrada")
    print(f"   Confiabilidad total: {confiabilidad:.4f} ({confiabilidad*100:.2f}%)")
    print(f"   Ruta: {' → '.join(ruta)}")
    print("\n   Detalle de tramos:")
    
    for i in range(len(ruta) - 1):
        origen = ruta[i]
        destino = ruta[i+1]
        # Buscar la probabilidad en el grafo original
        for vecino, prob in grafo.get(origen, []):
            if vecino == destino:
                conf_tramo = prob
                contribucion_log = -math.log(prob)
                print(f"   • {origen} → {destino}: {conf_tramo:.3f} "
                      f"(contribución log: {contribucion_log:.3f})")

# ===== EJEMPLO DE USO =====

# Red de puertos con probabilidades de éxito
# Formato: nodo: [(vecino, probabilidad_llegada)]
red_maritima = {
    'Puerto_A': [('Puerto_B', 0.95), ('Puerto_C', 0.85), ('Puerto_D', 0.70)],
    'Puerto_B': [('Puerto_A', 0.95), ('Puerto_E', 0.90), ('Puerto_F', 0.80)],
    'Puerto_C': [('Puerto_A', 0.85), ('Puerto_F', 0.88), ('Puerto_G', 0.75)],
    'Puerto_D': [('Puerto_A', 0.70), ('Puerto_G', 0.92), ('Puerto_H', 0.65)],
    'Puerto_E': [('Puerto_B', 0.90), ('Puerto_F', 0.85), ('Puerto_I', 0.95)],
    'Puerto_F': [('Puerto_B', 0.80), ('Puerto_C', 0.88), ('Puerto_E', 0.85), 
                 ('Puerto_H', 0.90), ('Puerto_I', 0.82)],
    'Puerto_G': [('Puerto_C', 0.75), ('Puerto_D', 0.92), ('Puerto_I', 0.78)],
    'Puerto_H': [('Puerto_D', 0.65), ('Puerto_F', 0.90), ('Puerto_I', 0.88)],
    'Puerto_I': [('Puerto_E', 0.95), ('Puerto_F', 0.82), ('Puerto_G', 0.78), 
                 ('Puerto_H', 0.88)]
}

print("=" * 80)
print("CAMINO MÁS SEGURO - MAXIMIZACIÓN DE CONFIABILIDAD")
print("=" * 80)

# Caso 1: Ruta directa vs ruta más confiable
print("\nCASO 1: De Puerto_A a Puerto_I")
print("-" * 50)
confiabilidad, ruta = encontrar_ruta_mas_confiable(red_maritima, 'Puerto_A', 'Puerto_I')
mostrar_ruta_confiable(ruta, confiabilidad, red_maritima)

# Comparación con ruta directa
print("\n   Comparación de rutas alternativas:")
rutas_alternativas = [
    (['Puerto_A', 'Puerto_B', 'Puerto_E', 'Puerto_I'], "A→B→E→I"),
    (['Puerto_A', 'Puerto_C', 'Puerto_F', 'Puerto_I'], "A→C→F→I"),
    (['Puerto_A', 'Puerto_D', 'Puerto_G', 'Puerto_I'], "A→D→G→I"),
]

for ruta_alt, nombre in rutas_alternativas:
    conf = 1.0
    for i in range(len(ruta_alt)-1):
        for vecino, prob in red_maritima.get(ruta_alt[i], []):
            if vecino == ruta_alt[i+1]:
                conf *= prob
                break
    print(f"   {nombre}: {conf:.4f} ({conf*100:.2f}%)")

# Caso 2: Ruta con diferentes niveles de confiabilidad
print("\nCASO 2: De Puerto_B a Puerto_H")
print("-" * 50)
confiabilidad, ruta = encontrar_ruta_mas_confiable(red_maritima, 'Puerto_B', 'Puerto_H')
mostrar_ruta_confiable(ruta, confiabilidad, red_maritima)

# Caso 3: Demostración de la transformación logarítmica
print("\nCASO 3: Demostración de transformación matemática")
print("-" * 50)
print("   Ruta: Puerto_A → Puerto_B → Puerto_E → Puerto_I")
print("   Probabilidades: 0.95 × 0.90 × 0.95 = 0.81225")
print("   Transformación log: -log(0.95) - log(0.90) - log(0.95)")
print(f"   = {(-math.log(0.95)):.3f} + {(-math.log(0.90)):.3f} + {(-math.log(0.95)):.3f}")
print(f"   = {(-math.log(0.95) - math.log(0.90) - math.log(0.95)):.3f}")
print(f"   Confiabilidad recuperada: e^(-0.2079) = {math.exp(-0.2079):.4f}")
