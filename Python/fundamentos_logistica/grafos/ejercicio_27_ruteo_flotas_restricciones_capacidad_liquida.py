"""Ejercicio 27: Ruteo de Flotas con Restricción de Capacidad Líquida

Una empresa de transporte de químicos tiene una red de distribución. Cada arista tiene una 
distancia y un límite de peso máximo permitido para camiones cisterna debido a puentes antiguos.

    Implementar un algoritmo que encuentre el camino más corto entre un centro de producción A 
    y un cliente B, pero que filtre y descarte automáticamente cualquier arista (tramo vial) 
    cuyo límite de capacidad de peso sea inferior al peso del camión actual (W). """

import heapq
from collections import defaultdict

def encontrar_ruta_segura(grafo, origen, destino, peso_camion):
    """
    Encuentra el camino más corto entre origen y destino considerando 
    solo aristas que soporten el peso del camión.
    
    Args:
        grafo: Diccionario {nodo: [(vecino, distancia, capacidad)]}
        origen: Nodo de inicio
        destino: Nodo final
        peso_camion: Peso del camión cisterna (W)
    
    Returns:
        Tupla (distancia_total, [ruta]) o (None, []) si no hay ruta
    """
    # Filtrar aristas que no soportan el peso
    grafo_filtrado = filtrar_aristas_por_peso(grafo, peso_camion)
    
    # Verificar si destino es alcanzable
    if destino not in grafo_filtrado and destino != origen:
        print(f"El destino {destino} no es accesible con peso {peso_camion}")
        return None, []
    
    # Dijkstra para encontrar el camino más corto
    distancias = {nodo: float('inf') for nodo in grafo_filtrado}
    distancias[origen] = 0
    padres = {origen: None}
    cola_prioridad = [(0, origen)]
    visitados = set()
    
    while cola_prioridad:
        dist_actual, nodo_actual = heapq.heappop(cola_prioridad)
        
        if nodo_actual in visitados:
            continue
        
        visitados.add(nodo_actual)
        
        # Si llegamos al destino, podemos parar (Dijkstra garantiza óptimo)
        if nodo_actual == destino:
            break
        
        # Explorar vecinos filtrados
        for vecino, distancia, capacidad in grafo_filtrado.get(nodo_actual, []):
            if vecino in visitados:
                continue
            
            nueva_dist = dist_actual + distancia
            if nueva_dist < distancias[vecino]:
                distancias[vecino] = nueva_dist
                padres[vecino] = nodo_actual
                heapq.heappush(cola_prioridad, (nueva_dist, vecino))
    
    # Reconstruir ruta
    if distancias[destino] == float('inf'):
        print(f"No existe ruta válida desde {origen} hasta {destino}")
        return None, []
    
    ruta = []
    nodo = destino
    while nodo is not None:
        ruta.append(nodo)
        nodo = padres.get(nodo)
    ruta.reverse()
    
    return distancias[destino], ruta

def filtrar_aristas_por_peso(grafo, peso_camion):
    """
    Filtra el grafo manteniendo solo aristas con capacidad >= peso_camion.
    
    Args:
        grafo: Grafo original
        peso_camion: Peso mínimo requerido
    
    Returns:
        Grafo filtrado
    """
    grafo_filtrado = defaultdict(list)
    
    for nodo, aristas in grafo.items():
        for vecino, distancia, capacidad in aristas:
            if capacidad >= peso_camion:
                grafo_filtrado[nodo].append((vecino, distancia, capacidad))
            else:
                print(f"Arista descartada: {nodo} → {vecino} "
                      f"(capacidad: {capacidad} < {peso_camion})")
    
    return dict(grafo_filtrado)

def mostrar_ruta(ruta, distancia, grafo):
    """Muestra la ruta con detalles de cada tramo."""
    if not ruta:
        print("No se encontró ruta")
        return
    
    print(f"\nRuta encontrada (distancia total: {distancia} km)")
    print(f"   {' → '.join(ruta)}")
    print("\n   Detalle de tramos:")
    
    for i in range(len(ruta) - 1):
        origen = ruta[i]
        destino = ruta[i+1]
        # Buscar la arista en el grafo original para mostrar capacidad
        for vecino, dist, cap in grafo.get(origen, []):
            if vecino == destino:
                print(f"   • {origen} → {destino}: {dist} km, capacidad: {cap} toneladas")
                break

# ===== EJEMPLO DE USO =====

# Crear red de distribución
# Formato: nodo: [(vecino, distancia_km, capacidad_toneladas)]
red_distribucion = {
    'A': [('B', 10, 15), ('C', 5, 8)],
    'B': [('A', 10, 15), ('D', 7, 12), ('E', 15, 6)],
    'C': [('A', 5, 8), ('D', 8, 5), ('F', 12, 10)],
    'D': [('B', 7, 12), ('C', 8, 5), ('E', 6, 9), ('G', 20, 7)],
    'E': [('B', 15, 6), ('D', 6, 9), ('H', 4, 11)],
    'F': [('C', 12, 10), ('G', 9, 4), ('H', 10, 8)],
    'G': [('D', 20, 7), ('F', 9, 4), ('H', 15, 6)],
    'H': [('E', 4, 11), ('F', 10, 8), ('G', 15, 6)]
}

print("=" * 70)
print("RUTEO DE FLOTAS CON RESTRICCIÓN DE CAPACIDAD")
print("=" * 70)

# Caso 1: Camión liviano (peso 5 toneladas)
print("\nCASO 1: Camión de 5 toneladas")
print("-" * 50)
distancia, ruta = encontrar_ruta_segura(red_distribucion, 'A', 'H', 5)
mostrar_ruta(ruta, distancia, red_distribucion)

# Caso 2: Camión mediano (peso 9 toneladas)
print("\nCASO 2: Camión de 9 toneladas")
print("-" * 50)
distancia, ruta = encontrar_ruta_segura(red_distribucion, 'A', 'H', 9)
mostrar_ruta(ruta, distancia, red_distribucion)

# Caso 3: Camión pesado (peso 13 toneladas)
print("\nCASO 3: Camión de 13 toneladas")
print("-" * 50)
distancia, ruta = encontrar_ruta_segura(red_distribucion, 'A', 'H', 13)
mostrar_ruta(ruta, distancia, red_distribucion)

# Caso 4: Sin ruta disponible
print("\nCASO 4: Camión muy pesado (20 toneladas)")
print("-" * 50)
distancia, ruta = encontrar_ruta_segura(red_distribucion, 'A', 'H', 20)
mostrar_ruta(ruta, distancia, red_distribucion)
