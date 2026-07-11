"""Búsqueda en Anchura (BFS)
En IO, entender cómo fluye la información o los recursos paso a paso es una de las habilidades más críticas.

El recorrido BFS no es solo un algoritmo para "visitar" nodos; es la base fundamental de la optimización
en redes no ponderadas (donde todas las conexiones tiene el mismo costo o importancia).

    - Minimización de Escalas Logísticas: BFS expande el mapa por niveles. Significa que la primera vez que 
      BFS encuentra un nodo, garantiza que ha llegado a él utilizando el menor número de arcos posibles. En
      transporte, esto equivale a encontrar la ruta con menos transbordos o escalas de camión/avión.

    - Análisis de Capacidad y Alcance: Si una planta manufacturera se contamina o un lote de materia prima sale
      defectuoso, un BFS te permite mapear en "Ola 1", "Ola 2" y "Ola3" qué otras plantas o almacenes se verán
      afectados por el efecto de manera cronlógica.

    - Estructura clave: Depende críticamente de una Cola (Queue) con política FIFO. El primero en ser descubierto
      es el primero en ser explorado.
"""

# Implementación en Python
from collections import deque
from typing import Dict, List, Set, Any

def bfs_logistico_base(lista_adyacencia: Dict[Any, list[Any]], nodo_inicio: Any) -> List[Any]:
    """
        Estrucutra estándar de un BFS optimizado para IO. 
        Complejidad temporal: O(V + E)
        Complejidad Espacial: O(V)
    """
    # Cola FIFO para nodos por explorar
    cola = deque([nodo_inicio])
    # Set hash O(1) para evitar bucles infinitos en redes con ciclos
    visitados: Set[Any] = {nodo_inicio}
    # Registro del orden de exploración
    orden_exploracion = []

    while cola:
        nodo_actual = cola.popleft() # Extraer el más antiguo (O(1))
        orden_exploracion.append(nodo_actual)

        # Expandir hacia los vecinos inmediatos
        for vecino in lista_adyacencia.get(nodo_actual, []):
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append(vecino)

    return orden_exploracion


