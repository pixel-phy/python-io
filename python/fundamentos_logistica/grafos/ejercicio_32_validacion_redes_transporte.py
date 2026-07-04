"""Ejercicio 32: Validación de Redes de Transporte

En una red de transporte de doble sentido (No dirigida), es vital asegurar que si existe una ruta 
de A a B con un costo X, exista la contraparte de B a A con el mismo costo.

- Crea una clase UndirectedSupplyNetwork. Implementa un método add_edge(node1, node2, distance)
  que garantice la simetría en la estructura interna de datos. Si se añade una ruta, debe reflejarse
  en ambos sentidos automáticamente.

"""

class UndirectedSupplyNetwork:
    def __init__(self):
        """
        Inicializa la red de transporte no dirigida.
        Usamos un diccionario de diccionarios para almacenar las conexiones.
        La estructura será: {node1: {node2: distance, node3: distance, ...}, ...}
        """
        self.graph = {}
    
    def add_edge(self, node1, node2, distance):
        """
        Añade una ruta bidireccional entre node1 y node2 con la distancia dada.
        Garantiza simetría: si existe ruta de A a B, existe de B a A con mismo costo.
        
        Args:
            node1: Primer nodo
            node2: Segundo nodo
            distance: Costo/distancia de la ruta (debe ser positivo)
        """
        # Validación básica
        if distance < 0:
            raise ValueError("La distancia no puede ser negativa")
        
        if node1 == node2:
            raise ValueError("No se permiten bucles (node1 == node2)")
        
        # Asegurar que node1 existe en el grafo
        if node1 not in self.graph:
            self.graph[node1] = {}
        
        # Asegurar que node2 existe en el grafo
        if node2 not in self.graph:
            self.graph[node2] = {}
        
        # Añadir la ruta en ambos sentidos con la misma distancia
        self.graph[node1][node2] = distance
        self.graph[node2][node1] = distance
    
    def get_neighbors(self, node):
        """
        Devuelve los vecinos de un nodo con sus distancias.
        """
        return self.graph.get(node, {})
    
    def get_distance(self, node1, node2):
        """
        Devuelve la distancia entre dos nodos si existe la ruta.
        Retorna None si no existe conexión directa.
        """
        if node1 in self.graph and node2 in self.graph[node1]:
            return self.graph[node1][node2]
        return None
    
    def __str__(self):
        """
        Representación legible de la red.
        """
        result = []
        for node, neighbors in sorted(self.graph.items()):
            neighbors_str = ', '.join(f"{neighbor}: {dist}" for neighbor, dist in sorted(neighbors.items()))
            result.append(f"{node} -> {{{neighbors_str}}}")
        return "\n".join(result)
    
    def remove_edge(self, node1, node2):
        """
        Elimina una ruta en ambos sentidos.
        """
        if node1 in self.graph and node2 in self.graph[node1]:
            del self.graph[node1][node2]
            del self.graph[node2][node1]
            
            # Limpiar nodos que quedan sin conexiones
            if not self.graph[node1]:
                del self.graph[node1]
            if not self.graph[node2]:
                del self.graph[node2]
            return True
        return False

# Prueba:

# Crear la red
network = UndirectedSupplyNetwork()

# Añadir rutas
network.add_edge("A", "B", 10)
network.add_edge("B", "C", 20)
network.add_edge("A", "C", 15)

# Verificar simetría
print("Distancia A->B:", network.get_distance("A", "B"))  # 10
print("Distancia B->A:", network.get_distance("B", "A"))  # 10 (simétrica)

# Ver todos los vecinos
print("Vecinos de B:", network.get_neighbors("B"))  # {'A': 10, 'C': 20}

# Mostrar red completa
print("\nRed completa:")
print(network)

# Eliminar una ruta
network.remove_edge("A", "B")
print("\nDespués de eliminar A-B:")
print(network)
