"""Ejercicio 34: Filtro de Arcos por capacidad crítica

Te dan una red de tuberías de petróleo (digrafo) donde cada arco tiene un peso que
representa la capacidad máxima de barriles por hora.

- Implementa un método que reciba un umbral mínimo de capacidad Q. El método debe retornar
  un nuevo grafo que contenga úncamente los "Arcos críticos" cuya capacidad sea estrictamente
  menor o igual a Q (rutas que restringen el flujo del sistema). 

"""

class PipelineNetwork:
    def __init__(self):
        """
        Inicializa la red de tuberías como un grafo dirigido.
        Estructura: {nodo_origen: {nodo_destino: capacidad, ...}, ...}
        """
        self.graph = {}
    
    def add_edge(self, origin, destination, capacity):
        """
        Añade un arco dirigido con capacidad específica.
        
        Args:
            origin: Nodo origen
            destination: Nodo destino
            capacity: Capacidad en barriles por hora (debe ser positiva)
        """
        if capacity <= 0:
            raise ValueError("La capacidad debe ser un valor positivo")
        
        if origin == destination:
            raise ValueError("No se permiten bucles en la red")
        
        if origin not in self.graph:
            self.graph[origin] = {}
        
        self.graph[origin][destination] = capacity
        
        # Asegurar que el destino existe como nodo aunque no tenga salidas
        if destination not in self.graph:
            self.graph[destination] = {}
    
    def filter_critical_edges(self, Q):
        """
        Filtra los arcos críticos cuya capacidad es estrictamente menor o igual a Q.
        
        Args:
            Q: Umbral mínimo de capacidad (barriles por hora)
        
        Returns:
            PipelineNetwork: Nuevo grafo con solo los arcos críticos
        """
        if Q < 0:
            raise ValueError("El umbral Q debe ser un valor no negativo")
        
        critical_network = PipelineNetwork()
        
        # Recorrer todos los nodos y sus arcos
        for origin, destinations in self.graph.items():
            for destination, capacity in destinations.items():
                # Verificar si la capacidad es crítica (menor o igual a Q)
                if capacity <= Q:
                    # Añadir el arco crítico al nuevo grafo
                    critical_network.add_edge(origin, destination, capacity)
        
        return critical_network
    
    def filter_critical_edges_alternative(self, Q):
        """
        Versión alternativa que devuelve un diccionario en lugar de un objeto.
        
        Args:
            Q: Umbral mínimo de capacidad
        
        Returns:
            dict: Grafo filtrado en formato {origen: {destino: capacidad}}
        """
        if Q < 0:
            raise ValueError("El umbral Q debe ser un valor no negativo")
        
        filtered_graph = {}
        
        for origin, destinations in self.graph.items():
            for destination, capacity in destinations.items():
                if capacity <= Q:
                    if origin not in filtered_graph:
                        filtered_graph[origin] = {}
                    filtered_graph[origin][destination] = capacity
                    
                    # Asegurar que el destino esté en el diccionario
                    if destination not in filtered_graph:
                        filtered_graph[destination] = {}
        
        return filtered_graph
    
    def get_critical_edges_report(self, Q):
        """
        Genera un reporte detallado de los arcos críticos.
        
        Args:
            Q: Umbral mínimo de capacidad
        
        Returns:
            dict: Reporte con estadísticas de arcos críticos
        """
        critical_edges = []
        total_edges = 0
        
        for origin, destinations in self.graph.items():
            for destination, capacity in destinations.items():
                total_edges += 1
                if capacity <= Q:
                    critical_edges.append({
                        "origin": origin,
                        "destination": destination,
                        "capacity": capacity
                    })
        
        return {
            "Q_threshold": Q,
            "total_edges": total_edges,
            "critical_edges_count": len(critical_edges),
            "critical_edges": critical_edges,
            "critical_percentage": (len(critical_edges) / total_edges * 100) if total_edges > 0 else 0
        }
    
    def display_network(self):
        """
        Muestra la red de forma legible.
        """
        if not self.graph:
            print("Red vacía")
            return
        
        print("RED DE TUBERÍAS")
        print("=" * 50)
        for origin in sorted(self.graph.keys()):
            destinations = self.graph[origin]
            if destinations:
                for destination, capacity in sorted(destinations.items()):
                    print(f"{origin} -> {destination} : {capacity} barriles/hora")
            else:
                print(f"{origin} (sin salidas)")
        print("=" * 50)


def filter_edges_by_capacity(graph, Q):
    """
    Función independiente que filtra arcos por capacidad crítica.
    Acepta un diccionario de adyacencia como entrada.
    
    Args:
        graph: Dict con formato {origen: {destino: capacidad}}
        Q: Umbral mínimo de capacidad
    
    Returns:
        dict: Grafo filtrado con arcos donde capacidad <= Q
    """
    if Q < 0:
        raise ValueError("El umbral Q debe ser un valor no negativo")
    
    filtered = {}
    
    for origin, destinations in graph.items():
        for destination, capacity in destinations.items():
            if capacity <= Q:
                if origin not in filtered:
                    filtered[origin] = {}
                filtered[origin][destination] = capacity
                
                if destination not in filtered:
                    filtered[destination] = {}
    
    return filtered


def compare_networks(original, filtered, Q):
    """
    Compara la red original con la red filtrada.
    
    Args:
        original: PipelineNetwork o dict
        filtered: PipelineNetwork o dict
        Q: Umbral utilizado
    """
    def count_edges(network):
        if isinstance(network, PipelineNetwork):
            return sum(len(dest) for dest in network.graph.values())
        else:
            return sum(len(dest) for dest in network.values())
    
    original_edges = count_edges(original)
    filtered_edges = count_edges(filtered)
    
    print("ANALISIS DE ARCOS CRITICOS")
    print("=" * 50)
    print(f"Umbral Q: {Q} barriles/hora")
    print(f"Arcos totales en red original: {original_edges}")
    print(f"Arcos críticos (capacidad <= Q): {filtered_edges}")
    print(f"Porcentaje de arcos críticos: {(filtered_edges/original_edges*100):.1f}%" if original_edges > 0 else "0%")
    print("=" * 50)

# Prueba:

# Crear la red de tuberías
pipeline = PipelineNetwork()

# Añadir arcos con diferentes capacidades
pipeline.add_edge("A", "B", 100)
pipeline.add_edge("A", "C", 50)
pipeline.add_edge("B", "C", 75)
pipeline.add_edge("B", "D", 30)
pipeline.add_edge("C", "D", 120)
pipeline.add_edge("D", "E", 25)
pipeline.add_edge("E", "A", 60)

# Mostrar red original
print("RED ORIGINAL")
pipeline.display_network()

# Filtrar arcos críticos con umbral Q = 50
Q = 50
critical_pipeline = pipeline.filter_critical_edges(Q)

print("\nRED CON ARCOS CRITICOS (capacidad <= 50)")
critical_pipeline.display_network()

# Obtener reporte detallado
report = pipeline.get_critical_edges_report(Q)
print("\nREPORTE DE ARCOS CRITICOS")
for edge in report["critical_edges"]:
    print(f"  {edge['origin']} -> {edge['destination']}: {edge['capacity']} barriles/hora")

# Usar la función independiente con un diccionario
graph_dict = {
    "A": {"B": 100, "C": 50},
    "B": {"C": 75, "D": 30},
    "C": {"D": 120},
    "D": {"E": 25},
    "E": {"A": 60}
}

filtered_dict = filter_edges_by_capacity(graph_dict, 50)
print("\nFILTRADO CON FUNCION INDEPENDIENTE")
for origin, dests in filtered_dict.items():
    for dest, cap in dests.items():
        print(f"  {origin} -> {dest}: {cap}")

# Comparar redes
compare_networks(pipeline, critical_pipeline, Q)
