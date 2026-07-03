"""Teoría de Grafos: El lenguaje de las Redes en IO

En OR, un grafo G = (V,E) no es solo una estructura de datos: es el modelo de un sistema. 

    - Vértices o Nodos (V): Representan puntos de decisión, orígenes/destinos, centros de distribución (CD), 
    almacenes o estapas en un proyecto.
    
    - Aristas o Arcos (E): Representan conexiones, rutas de transporte, canales de comunicación o dependencias temporales.

    - Grafo no dirigido: Las conexiones son bidireccionales. Si una una carretera de doble sentido entre el Centro A
      y el centro B, el flujo puede ir en ambos sentidos con el mismo costo.

    - Grafo dirigido: Las conexiones tienen un sentido único. Fundamental para modelar calles de un solo sentido, flujos
      de procesos productivos donde no se puede retroceder, o relaciones de precedencia en la gestión de proyectos
      (PERT/CPM).

"""
# Implementación en Python
from typing import Dict, List, Tuple

class NetworkModel:
    """Representa una red de optimización logística mediante un Grafo dirigido."""
    
    def __init__(self):
    # Estructura: {nodo_origen: [(nodo_destino, costo_transporte), ...]}
        self.adjacency_list: Dict[str, List[Tuple[str, float]]] = {}

    def add_node(self, node: str) -> None:
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []

    def add_arc(self, source: str, target: str, cost: float) -> None:
        """Añade un arco dirigido con un costo/peso asociado."""
        self.add_node(source)
        self.add_node(target)
        self.adjacency_list[source].append((target, cost))

    def get_outbound_routes(self, node: str) -> List[tuple[str, float]]:
        """Devuelve las rutas salientes y sus costos para un nodo específico."""
        return self.adjacency_list.get(node, [])

    def __str__(self) -> str:
        return "\n".join([f"{node} -> {edges}" for node, edges in self.adjacency_list.items()])

# Caso de uso:
if __name__ == "__main__":
    supply_chain = NetworkModel()

    # Nodos de la red
    supply_chain.add_arc("Planta_Medellin", "CD_Bogotá", cost=150.0)
    supply_chain.add_arc("Planta_Medellin", "CD_Cali", cost=120.0)
    supply_chain.add_arc("CD_Bogota", "Cliente_Norte", cost=50.0)
    supply_chain.add_arc("CD_Cali", "Cliente_Sur", cost=40.0)

    print("Representación de la Red de Suministro:")
    print(supply_chain)
