"""Ejercicio 33: Cálculo de Grados de Entrada/Salida para Cuellos de Botella

En un sistema de manufactura flexible, los nodos son estaciones de trabajo. Un nodo con alto grado de entrada
(In-degree) puede ser un cuello de botella de inventario en proceso (WIP). Un nodo con alto grado de salida 
(Out-degree) es un gran distribuidor de flujo.

- Diseñar una función que reciba un grafo dirigido (red de procesos) y devuelva un reporte (dict) con el In-degree
  y Out-degree de cada estación. Identifica automáticamente cuál es la estación con mayor riesgo de cuello de botella
  (mayor In-degree).

"""

def calculate_degrees_and_bottleneck(directed_graph):
    """
    Calcula los grados de entrada y salida para cada nodo en un grafo dirigido
    e identifica la estación con mayor riesgo de cuello de botella.
    
    Args:
        directed_graph: Diccionario que representa el grafo dirigido.
                        Formato: {nodo: [lista_de_vecinos_salida]}
    
    Returns:
        dict: Reporte con in-degree, out-degree y el nodo con mayor in-degree
    """
    if not directed_graph:
        return {
            "report": {},
            "bottleneck_risk": None,
            "max_in_degree": 0
        }
    
    # Inicializar diccionarios para grados
    in_degree = {node: 0 for node in directed_graph}
    out_degree = {node: 0 for node in directed_graph}
    
    # Calcular out-degree para cada nodo
    for node, neighbors in directed_graph.items():
        out_degree[node] = len(neighbors)
        
        # Calcular in-degree: contar cuántas veces aparece cada nodo como vecino
        for neighbor in neighbors:
            if neighbor in in_degree:
                in_degree[neighbor] += 1
            else:
                # Si el vecino no está en el grafo como clave, lo añadimos
                in_degree[neighbor] = 1
                out_degree[neighbor] = out_degree.get(neighbor, 0)
    
    # Asegurar que todos los nodos tengan entrada en out_degree
    for node in in_degree:
        if node not in out_degree:
            out_degree[node] = 0
    
    # Construir reporte
    report = {}
    for node in sorted(set(list(in_degree.keys()) + list(out_degree.keys()))):
        report[node] = {
            "in_degree": in_degree.get(node, 0),
            "out_degree": out_degree.get(node, 0)
        }
    
    # Identificar cuello de botella (nodo con mayor in-degree)
    max_in_degree = -1
    bottleneck_node = None
    
    for node, degrees in report.items():
        if degrees["in_degree"] > max_in_degree:
            max_in_degree = degrees["in_degree"]
            bottleneck_node = node
    
    return {
        "report": report,
        "bottleneck_risk": bottleneck_node,
        "max_in_degree": max_in_degree
    }


def calculate_degrees_alternative(graph_edges):
    """
    Versión alternativa que recibe una lista de aristas (origen, destino).
    
    Args:
        graph_edges: Lista de tuplas (origen, destino)
    
    Returns:
        dict: Mismo formato que la función principal
    """
    if not graph_edges:
        return {
            "report": {},
            "bottleneck_risk": None,
            "max_in_degree": 0
        }
    
    in_degree = {}
    out_degree = {}
    
    for origin, destination in graph_edges:
        # Out-degree para el origen
        out_degree[origin] = out_degree.get(origin, 0) + 1
        if destination not in out_degree:
            out_degree[destination] = out_degree.get(destination, 0)
        
        # In-degree para el destino
        in_degree[destination] = in_degree.get(destination, 0) + 1
        if origin not in in_degree:
            in_degree[origin] = in_degree.get(origin, 0)
    
    # Construir reporte
    all_nodes = set(list(in_degree.keys()) + list(out_degree.keys()))
    report = {}
    
    for node in sorted(all_nodes):
        report[node] = {
            "in_degree": in_degree.get(node, 0),
            "out_degree": out_degree.get(node, 0)
        }
    
    # Identificar cuello de botella
    max_in_degree = -1
    bottleneck_node = None
    
    for node, degrees in report.items():
        if degrees["in_degree"] > max_in_degree:
            max_in_degree = degrees["in_degree"]
            bottleneck_node = node
    
    return {
        "report": report,
        "bottleneck_risk": bottleneck_node,
        "max_in_degree": max_in_degree
    }


def print_bottleneck_report(result):
    """
    Función auxiliar para imprimir el reporte de forma legible.
    """
    print("REPORTE DE GRADOS DE ENTRADA Y SALIDA")
    print("=" * 50)
    
    report = result["report"]
    for node in sorted(report.keys()):
        degrees = report[node]
        print(f"Estación {node}:")
        print(f"  In-degree (entradas): {degrees['in_degree']}")
        print(f"  Out-degree (salidas): {degrees['out_degree']}")
        print()
    
    bottleneck = result["bottleneck_risk"]
    max_degree = result["max_in_degree"]
    
    if bottleneck is not None:
        print("=" * 50)
        print(f"ESTACIÓN CON MAYOR RIESGO DE CUELLO DE BOTELLA:")
        print(f"  Estación: {bottleneck}")
        print(f"  In-degree: {max_degree}")
        print(f"  Recomendación: Revisar capacidad de procesamiento y flujo de entrada")
    else:
        print("No hay nodos en el grafo.")

# Prueba:

# Grafo representado como diccionario de adyacencia
manufacturing_graph = {
    "EstacionA": ["EstacionB", "EstacionC"],
    "EstacionB": ["EstacionD"],
    "EstacionC": ["EstacionB", "EstacionD"],
    "EstacionD": ["EstacionE"],
    "EstacionE": []
}

result = calculate_degrees_and_bottleneck(manufacturing_graph)
print_bottleneck_report(result)

# Grafo representado como lista de aristas
edges = [
    ("EstacionA", "EstacionB"),
    ("EstacionA", "EstacionC"),
    ("EstacionB", "EstacionD"),
    ("EstacionC", "EstacionB"),
    ("EstacionC", "EstacionD"),
    ("EstacionD", "EstacionE")
]

result_edges = calculate_degrees_alternative(edges)
print_bottleneck_report(result_edges)

# Acceso directo a los datos
result = calculate_degrees_and_bottleneck(manufacturing_graph)
print("Reporte detallado:", result["report"])
print("Cuello de botella:", result["bottleneck_risk"])
print("Grado de entrada máximo:", result["max_in_degree"])
