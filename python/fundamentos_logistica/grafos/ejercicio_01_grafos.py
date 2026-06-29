"""Conceptos Básicos de Grafos

En IO, un grafo G = (V,E) es la estructura matemática por excelencia para modelar 
redes de suministro, sistemas de transporte, flujos de procesos o dependencias de tareas.

- Vértices (V / Nodos): Representan los puntos del sistema. Ejemplo: Centros de distribución,
plantas de producción, clientes, o estados de un inventario.

- Aristas (E / Arcos): Representan la relación o conexión entre nodos.Ejemplos: Rutas de transporte,
tuberías, o la transición de una tarea a otra. 

- Grafo No Dirigido: Las conexiones son bidireccionales. Si hay una carretera de doble sentido 
entre el CD A y el CD B, el flujo peude ir en ambos sentidos.

- Grafo DIrigido (Digrafo): Las conexciones tienen un sentido único. Esencial para modelar calles
de un solo sentido, flujos de procesos (la tarea B depende de la A), o redes de sumideros/fuentes.

- Grafo Ponderado: Cada arista tiene un peso (w). En IO, este peso suele ser la función 
objetivo a minimizar o maximizar: costos de transporte, distancias, tiempos de viaje o capacidades
de capacidad máxima.

"""

# Implementación Base en Python

from typing import Dict, List, Tuple, Set

class NetworkNode:
    def __init__(self, name: str, node_type: str):
        self.name = name
        self.node_type = node_type

    def __repr__(self) -> str:
        return f"{self.name} ({self.node_type})"

class SupplyChainNetwork:
    def __init__(self, directed: bool = True):
        self.directed: bool = directed
        # Grafo: Nodo_origen -> Lista de Tuplas (Nodo_Destino, Costo_Transporte)
        self.graph: Dict[str, List[Tuple[str, float]]] = {}
        self.nodes: Dect[str, NetworkNode] = {}

    def add_node(self, name:str, node_type: str) -> None:
        if name not in self.nodes:
            self.nodes[name] = NetworkNode(name, node_type)
            self.graph[name] = []

    def add_route(self, u: str, v: str, cost: float) -> None:
        # Asegurar que los nodos existen
        if u not in self.graph: self.add_node(u, "Generic")
        if v not in self.graph: self.add_node(v, "Generic")

        self.graph[u].append((v, cost))
        if not self.directed:
            self.graph[v].append((u, cost))

    def get_connections(self, u: str) -> List[Tuple[str, float]]:
        return self.graph.get(u, [])
