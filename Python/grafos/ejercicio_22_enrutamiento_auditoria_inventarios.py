"""Ejercicio 22: Enrutamiento de Auditoría de Inventarios (Caminos Únicos)

Un auditor logístico debe salir de la Sede Central (A) y llegar al Centro de Distribución Principal
(B). Quiere conocer todos los caminos posibles en la red de transporte que no repitan ninguna ciudad
intermedia, para evaluar alternativas de costos fijos. Utiliza DFS con backtracking para listar 
todos los caminos simples entre un origen y un destino. """

from typing import List, Dict, Set, Optional

class EnrutadorAuditoria:
    """Encuentra todos los caminos simples entre dos nodos en una red de transporte."""
    
    def __init__(self):
        self.grafo: Dict[str, List[str]] = {}
        self.caminos: List[List[str]] = []
        self.mejor_camino: Optional[List[str]] = None
        self.mejor_costo: Optional[float] = None

    def agregar_conexion(self, ciudad_origen: str, ciudad_destino: str, costo: float = 1.0) -> None:
        """
        Agrega una conexión bidireccional entre dos ciudades.
        
        Args:
            ciudad_origen: Ciudad de origen
            ciudad_destino: Ciudad de destino
            costo: Costo fijo de transporte (por defecto 1.0)
        """
        # Grafo no dirigido (conexiones bidireccionales)
        if ciudad_origen not in self.grafo:
            self.grafo[ciudad_origen] = []
        if ciudad_destino not in self.grafo:
            self.grafo[ciudad_destino] = []
        
        self.grafo[ciudad_origen].append(ciudad_destino)
        self.grafo[ciudad_destino].append(ciudad_origen)

    def encontrar_caminos(self, origen: str, destino: str) -> List[List[str]]:
        """
        Encuentra todos los caminos simples entre origen y destino usando DFS con backtracking.
        
        Args:
            origen: Nodo de inicio
            destino: Nodo de destino
            
        Returns:
            List[List[str]]: Lista de todos los caminos simples encontrados
        """
        if origen not in self.grafo or destino not in self.grafo:
            return []
        
        self.caminos = []
        camino_actual = [origen]
        visitados = {origen}
        
        self._dfs_backtracking(origen, destino, camino_actual, visitados)
        return self.caminos

    def _dfs_backtracking(self, actual: str, destino: str, camino: List[str], visitados: Set[str]) -> None:
        """
        DFS recursivo con backtracking para encontrar todos los caminos simples.
        """
        if actual == destino:
            # Encontramos un camino completo
            self.caminos.append(camino.copy())
            return
        
        for vecino in self.grafo[actual]:
            if vecino not in visitados:
                # Marcar como visitado
                visitados.add(vecino)
                camino.append(vecino)
                
                # Explorar
                self._dfs_backtracking(vecino, destino, camino, visitados)
                
                # Backtracking: desmarcar
                camino.pop()
                visitados.remove(vecino)

    def encontrar_mejor_camino(self, origen: str, destino: str, costos: Dict[str, Dict[str, float]]) -> Optional[List[str]]:
        """
        Encuentra el camino con menor costo total entre origen y destino.
        
        Args:
            origen: Nodo de inicio
            destino: Nodo de destino
            costos: Diccionario de costos entre nodos (bidireccionales)
            
        Returns:
            Optional[List[str]]: El camino con menor costo o None si no hay caminos
        """
        caminos = self.encontrar_caminos(origen, destino)
        
        if not caminos:
            return None
        
        self.mejor_camino = None
        self.mejor_costo = float('inf')
        
        for camino in caminos:
            costo_total = 0.0
            for i in range(len(camino) - 1):
                origen_nodo = camino[i]
                destino_nodo = camino[i + 1]
                # El costo es bidireccional
                if origen_nodo in costos and destino_nodo in costos[origen_nodo]:
                    costo_total += costos[origen_nodo][destino_nodo]
                else:
                    # Si no hay costo definido, usamos 1.0 por defecto
                    costo_total += 1.0
            
            if costo_total < self.mejor_costo:
                self.mejor_costo = costo_total
                self.mejor_camino = camino
        
        return self.mejor_camino

    def mostrar_caminos(self, origen: str, destino: str) -> None:
        """Muestra todos los caminos encontrados de forma clara."""
        caminos = self.encontrar_caminos(origen, destino)
        
        if not caminos:
            print(f"No se encontraron caminos desde {origen} hasta {destino}")
            return
        
        print(f"CAMINOS POSIBLES DESDE {origen} HASTA {destino}")
        print("=" * 60)
        
        for i, camino in enumerate(caminos, 1):
            print(f"Camino {i:2}: {' -> '.join(camino)}")
        
        print("=" * 60)
        print(f"Total de caminos encontrados: {len(caminos)}")

    def mostrar_caminos_con_costos(self, origen: str, destino: str, costos: Dict[str, Dict[str, float]]) -> None:
        """Muestra todos los caminos con sus costos totales."""
        caminos = self.encontrar_caminos(origen, destino)
        
        if not caminos:
            print(f"No se encontraron caminos desde {origen} hasta {destino}")
            return
        
        print(f"CAMINOS Y COSTOS DESDE {origen} HASTA {destino}")
        print("=" * 70)
        
        for i, camino in enumerate(caminos, 1):
            costo_total = 0.0
            detalles = []
            
            for j in range(len(camino) - 1):
                origen_nodo = camino[j]
                destino_nodo = camino[j + 1]
                
                # Obtener costo
                if origen_nodo in costos and destino_nodo in costos[origen_nodo]:
                    costo = costos[origen_nodo][destino_nodo]
                else:
                    costo = 1.0
                
                costo_total += costo
                detalles.append(f"{origen_nodo}->{destino_nodo}:{costo}")
            
            print(f"Camino {i:2}: {' -> '.join(camino)}")
            print(f"       Costo total: {costo_total:.2f}  |  Detalles: {' | '.join(detalles)}")
            print()
        
        print("=" * 70)
        
        # Encontrar el mejor camino
        mejor = self.encontrar_mejor_camino(origen, destino, costos)
        if mejor:
            costo_mejor = self.mejor_costo
            print(f"MEJOR CAMINO (menor costo): {' -> '.join(mejor)}")
            print(f"Costo total optimizado: {costo_mejor:.2f}")


# ===== EJEMPLO DE USO =====
# Red de transporte para auditoría logística
enrutador = EnrutadorAuditoria()

# Agregar conexiones de la red (grafo no dirigido)
enrutador.agregar_conexion("A", "B", 5.0)  # Sede Central -> Centro Distribución
enrutador.agregar_conexion("A", "C", 3.0)
enrutador.agregar_conexion("A", "D", 4.0)
enrutador.agregar_conexion("B", "E", 6.0)
enrutador.agregar_conexion("C", "E", 2.0)
enrutador.agregar_conexion("C", "F", 7.0)
enrutador.agregar_conexion("D", "F", 3.0)
enrutador.agregar_conexion("E", "G", 4.0)
enrutador.agregar_conexion("F", "G", 5.0)
enrutador.agregar_conexion("G", "B", 2.0)  # Conexión final a destino

# Definir costos específicos (sobrescribe los costos por defecto)
costos = {
    "A": {"B": 5.0, "C": 3.0, "D": 4.0},
    "B": {"A": 5.0, "E": 6.0, "G": 2.0},
    "C": {"A": 3.0, "E": 2.0, "F": 7.0},
    "D": {"A": 4.0, "F": 3.0},
    "E": {"B": 6.0, "C": 2.0, "G": 4.0},
    "F": {"C": 7.0, "D": 3.0, "G": 5.0},
    "G": {"E": 4.0, "F": 5.0, "B": 2.0}
}

# Mostrar todos los caminos
enrutador.mostrar_caminos("A", "B")

print("\n" + "=" * 70)
print()

# Mostrar caminos con costos
enrutador.mostrar_caminos_con_costos("A", "B", costos)
