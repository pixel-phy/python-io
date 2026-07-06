""" Ejercicio 35: Matriz de costos de conectividad directa

Los solvers de optimización lineal (como PuLP o Gurobi) a veces requieren matrices densas 
de coeficientes de costos en lugar de listas de adyacencia para formular la función objetivo.

- Escribir un algoritmo que convierta una lista de adyacencia (de un grafo dirigido de IO) en una 
  Matriz de Adyacencia de Costos usando listas anidades o numpy. Si no existe conexión directa entre dos 
  nodos, el costo debe ser infinito ( float('inf') ), y la diagonal principal (un nodo consigo mismo)
  debe ser 0.

"""

import numpy as np

class ConnectivityCostMatrix:
    def __init__(self):
        """
        Inicializa el convertidor de listas de adyacencia a matrices de costos.
        """
        self.adjacency_list = {}
        self.nodes = []
        self.node_index = {}
        self.cost_matrix = None
    
    def load_adjacency_list(self, adjacency_list):
        """
        Carga una lista de adyacencia desde un diccionario.
        
        Args:
            adjacency_list: Dict con formato {origen: {destino: costo}}
        """
        self.adjacency_list = adjacency_list
        self._build_node_mapping()
        self._build_cost_matrix()
    
    def _build_node_mapping(self):
        """
        Construye el mapeo de nodos a índices para la matriz.
        """
        # Recolectar todos los nodos únicos
        all_nodes = set()
        for origin, destinations in self.adjacency_list.items():
            all_nodes.add(origin)
            for destination in destinations.keys():
                all_nodes.add(destination)
        
        # Ordenar nodos para tener un orden consistente
        self.nodes = sorted(list(all_nodes))
        self.node_index = {node: idx for idx, node in enumerate(self.nodes)}
    
    def _build_cost_matrix(self):
        """
        Construye la matriz de costos con infinitos para conexiones inexistentes.
        """
        n = len(self.nodes)
        # Inicializar con infinito
        self.cost_matrix = [[float('inf')] * n for _ in range(n)]
        
        # Diagonal principal = 0
        for i in range(n):
            self.cost_matrix[i][i] = 0
        
        # Llenar con los costos de las conexiones existentes
        for origin, destinations in self.adjacency_list.items():
            if origin in self.node_index:
                i = self.node_index[origin]
                for destination, cost in destinations.items():
                    if destination in self.node_index:
                        j = self.node_index[destination]
                        self.cost_matrix[i][j] = cost
    
    def get_cost_matrix(self):
        """
        Retorna la matriz de costos como lista anidada.
        """
        return self.cost_matrix
    
    def get_cost_matrix_numpy(self):
        """
        Retorna la matriz de costos como array de NumPy.
        """
        return np.array(self.cost_matrix)
    
    def get_node_list(self):
        """
        Retorna la lista ordenada de nodos.
        """
        return self.nodes
    
    def get_node_index_mapping(self):
        """
        Retorna el mapeo de nodos a índices.
        """
        return self.node_index
    
    def display_matrix(self, use_numpy=False):
        """
        Muestra la matriz de costos de forma legible.
        """
        if use_numpy:
            matrix = self.get_cost_matrix_numpy()
        else:
            matrix = self.get_cost_matrix()
        
        n = len(self.nodes)
        
        # Cabecera con nombres de nodos
        print("MATRIZ DE COSTOS DE CONECTIVIDAD DIRECTA")
        print("=" * 70)
        print("      ", end="")
        for node in self.nodes:
            print(f"{node:>8}", end="")
        print()
        print("      " + "-" * (8 * n))
        
        # Filas de la matriz
        for i, node in enumerate(self.nodes):
            print(f"{node:<4} |", end="")
            for j in range(n):
                value = matrix[i][j]
                if value == float('inf'):
                    print(f"{"inf":>8}", end="")
                else:
                    print(f"{value:>8.2f}" if isinstance(value, float) else f"{value:>8}", end="")
            print()
        print("=" * 70)


def adjacency_to_cost_matrix(adjacency_list, return_numpy=False):
    """
    Función independiente para convertir lista de adyacencia a matriz de costos.
    
    Args:
        adjacency_list: Dict con formato {origen: {destino: costo}}
        return_numpy: Si es True, retorna array de NumPy en lugar de lista anidada
    
    Returns:
        tuple: (matriz_costos, lista_nodos, mapeo_nodos)
    """
    # Recolectar todos los nodos únicos
    all_nodes = set()
    for origin, destinations in adjacency_list.items():
        all_nodes.add(origin)
        for destination in destinations.keys():
            all_nodes.add(destination)
    
    # Ordenar nodos
    nodes = sorted(list(all_nodes))
    node_index = {node: idx for idx, node in enumerate(nodes)}
    n = len(nodes)
    
    # Inicializar matriz con infinito
    cost_matrix = [[float('inf')] * n for _ in range(n)]
    
    # Diagonal principal = 0
    for i in range(n):
        cost_matrix[i][i] = 0
    
    # Llenar con costos existentes
    for origin, destinations in adjacency_list.items():
        if origin in node_index:
            i = node_index[origin]
            for destination, cost in destinations.items():
                if destination in node_index:
                    j = node_index[destination]
                    cost_matrix[i][j] = cost
    
    # Convertir a NumPy si se solicita
    if return_numpy:
        cost_matrix = np.array(cost_matrix)
    
    return cost_matrix, nodes, node_index


def adjacency_edges_to_cost_matrix(edges, return_numpy=False):
    """
    Versión alternativa que acepta una lista de aristas (origen, destino, costo).
    
    Args:
        edges: Lista de tuplas (origen, destino, costo)
        return_numpy: Si es True, retorna array de NumPy
    
    Returns:
        tuple: (matriz_costos, lista_nodos, mapeo_nodos)
    """
    # Construir lista de adyacencia desde aristas
    adjacency = {}
    for origin, destination, cost in edges:
        if origin not in adjacency:
            adjacency[origin] = {}
        adjacency[origin][destination] = cost
    
    return adjacency_to_cost_matrix(adjacency, return_numpy)


def format_cost_matrix_for_solver(cost_matrix, node_list=None):
    """
    Formatea la matriz de costos para ser utilizada en solvers de optimización.
    
    Args:
        cost_matrix: Matriz de costos (lista anidada o array de NumPy)
        node_list: Lista de nodos opcional para etiquetar índices
    
    Returns:
        dict: Diccionario con la matriz formateada y metadatos
    """
    if isinstance(cost_matrix, np.ndarray):
        matrix = cost_matrix.tolist()
    else:
        matrix = cost_matrix
    
    n = len(matrix)
    
    # Verificar que la matriz es cuadrada
    for row in matrix:
        if len(row) != n:
            raise ValueError("La matriz debe ser cuadrada")
    
    # Extraer información útil para el solver
    result = {
        "matrix": matrix,
        "dimension": n,
        "has_infinite": any(float('inf') in row for row in matrix),
        "infinite_positions": [],
        "zero_diagonal": all(matrix[i][i] == 0 for i in range(n))
    }
    
    # Registrar posiciones con infinito
    for i in range(n):
        for j in range(n):
            if matrix[i][j] == float('inf'):
                result["infinite_positions"].append((i, j))
    
    if node_list:
        result["nodes"] = node_list
        result["node_mapping"] = {node: idx for idx, node in enumerate(node_list)}
    
    return result


def validate_matrix_symmetry(cost_matrix):
    """
    Valida si una matriz de costos es simétrica (para grafos no dirigidos).
    
    Args:
        cost_matrix: Matriz de costos
    
    Returns:
        bool: True si es simétrica, False en caso contrario
    """
    if isinstance(cost_matrix, np.ndarray):
        matrix = cost_matrix
    else:
        matrix = np.array(cost_matrix)
    
    if matrix.shape[0] != matrix.shape[1]:
        return False
    
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i][j] != matrix[j][i]:
                return False
    
    return True

# Prueba:

#Usando la clase
print("USANDO CLASE")
print("-" * 50)

# Crear lista de adyacencia (grafo dirigido de IO)
adjacency = {
    "EstacionA": {"EstacionB": 10.5, "EstacionC": 7.2},
    "EstacionB": {"EstacionD": 3.8},
    "EstacionC": {"EstacionB": 4.1, "EstacionD": 6.9},
    "EstacionD": {"EstacionE": 12.3},
    "EstacionE": {}
}

# Usar la clase
converter = ConnectivityCostMatrix()
converter.load_adjacency_list(adjacency)

# Obtener la matriz como lista anidada
cost_matrix = converter.get_cost_matrix()
print("Matriz de costos (lista anidada):")
for row in cost_matrix:
    print(row)

# Mostrar la matriz de forma legible
print("\n")
converter.display_matrix()

# Obtener como NumPy
print("\nMatriz como NumPy array:")
numpy_matrix = converter.get_cost_matrix_numpy()
print(numpy_matrix)

print("\nLista de nodos:", converter.get_node_list())
print("Mapeo de nodos:", converter.get_node_index_mapping())

# Ejemplo 2: Usando la función independiente
print("\n" + "=" * 70)
print("FUNCION INDEPENDIENTE")
print("-" * 50)

adjacency = {
    "A": {"B": 15, "C": 20},
    "B": {"D": 25},
    "C": {"B": 10, "D": 30},
    "D": {}
}

cost_matrix, nodes, mapping = adjacency_to_cost_matrix(adjacency)
print("Nodos:", nodes)
print("Mapeo:", mapping)
print("Matriz de costos:")
for row in cost_matrix:
    print(row)

# Ejemplo 3: Usando lista de aristas
print("\n" + "=" * 70)
print("LISTA DE ARISTAS")
print("-" * 50)

edges = [
    ("A", "B", 15),
    ("A", "C", 20),
    ("B", "D", 25),
    ("C", "B", 10),
    ("C", "D", 30)
]

cost_matrix_edges, nodes_edges, mapping_edges = adjacency_edges_to_cost_matrix(edges, return_numpy=True)
print("Nodos:", nodes_edges)
print("Matriz de costos (NumPy):")
print(cost_matrix_edges)

# Ejemplo 4: Formateo para solver
print("\n" + "=" * 70)
print("FORMATO PARA SOLVER")
print("-" * 50)

formatted = format_cost_matrix_for_solver(cost_matrix, nodes)
print("Dimension:", formatted["dimension"])
print("Contiene infinitos:", formatted["has_infinite"])
print("Posiciones con infinito:", formatted["infinite_positions"])
print("Diagonal principal con ceros:", formatted["zero_diagonal"])

# Ejemplo 5: Validación de simetría
print("\n" + "=" * 70)
print("VALIDACION DE SIMETRIA")
print("-" * 50)

# Matriz no dirigida (simétrica)
undirected_edges = [
    ("A", "B", 10),
    ("B", "A", 10),
    ("A", "C", 20),
    ("C", "A", 20)
]
undirected_matrix, _, _ = adjacency_edges_to_cost_matrix(undirected_edges, return_numpy=True)
print("¿La matriz es simétrica?", validate_matrix_symmetry(undirected_matrix))

# Matriz dirigida (no simétrica)
print("¿La matriz original es simétrica?", validate_matrix_symmetry(converter.get_cost_matrix_numpy()))
