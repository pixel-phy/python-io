"""Camino más corto y Detección de ciclos en IO

En IO, esto no es solo recorrer un grafo: es la base para la optimización de redes de transporte,
la planificación de proyectos (PERT/CPM) y la detección de dependencias circulares destructivas 
en cadenas de suministro.

En el contexto corporativo e industrial, estas dos aplicaciones resulven problemas críticos:
1. Camino más corto (Algoritmo de Dijkstra): Optimiza costos, distancias o tiempos de tránsito en 
redes loísticas.
2. Detección de ciclos (DFS/Tarjan/Algoritmos de ordenamiento topológico): Identifica bucles infinitos en 
asignaciones de tareas o dependencias de inventario, y es fundamental para asegurar que una red de proyectos
(PERT) sea un Grafo Acíclico dirigido (DAG)."""

# Implementación general en Python

import heapq
from typing import Dict, List, Tuple, Optional

class NetworkOptimizer:
    def __init__(self):
        # Lista de adyacencia: {origen: [(destino, costo)]}
        self.graph: Dict[str, List[Tuple[str, float]]] = {}
    
    def add_edge(self, u: str, v: str, weight: float) -> None:
        if u not in self.graph:
            self.graph[u] = []
        self.graph[u].append((v, weight))

    def dijkstra(self, start: str, end: str) -> Tuple[Optional[List[str]], float]:
        """Calcula la ruta de costo mínimo entre dos nodos."""
        queue: List[Tuple[float, str, List[str]]] = [(0.0, start, [start])]
        visited = set()

        while queue:
            (cost, current, path) = heapq.heappop(queue)

            if current in visited:
                continue
            visited.add(current)

            if current == end:
                return path, cost

            for neighbor, weight in self.graph.get(current, []):
                if neighbor not in visited:
                    heapq.heappush(queue, (cost + weight, neighbor, path + [neighbor]))

        return None, float('inf')

    def has_cycle_dfs(self) -> bool:
        """Detecta si existen dependencias circulares (ciclos) en la red."""
        visited = set()
        rec_stack = set() # Pila de recursión para el camino actual

        def dfs(node:str) -> bool:
            visited_add(node)
            rec_stack.add(node)

            for neighbor, _ in self.graph.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(node)
            return False

        for node in self.graph:
            if node not in visited:
                if dfs(node):
                    return True
        return False
