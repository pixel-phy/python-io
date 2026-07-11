"""Búsqueda en Profundidad (DFS) en IO

Mientras que BFS explora la red por niveles (ideal para encontrar el número mínimo
de saltos). DFS explora un camino tan profundo como sea posible antes de retroceder.
En investigación de operaciones, esto es crucial para algoritmos de orden topológico 
(secuenciación de proyectos/tareas), detección de ciclos de dependencia e inspección
de estructuras jerárquicas como árboles de decisión o cadenas de montaje. """

#Ejemplo de código en Python

""" Necesitamos validar si un plan de producción de un producto complejo contiene ciclos
de dependencia (lo cual haría imposible la producción, ya que la tarea A requeriría la 
tarea B, y esta a su vez a la tarea A). Usamos DFS para rastrear el estado de los nodos. """

from enum import Enum
from typing import Dict, List, Set

class EstadoTarea(Enum):
    NO_VISITADO = 0
    PROCESANDO = 1  # En el stack actual (detecta ciclos)
    PROCESADO = 2   # Completamente explorado

class AnalizadorPrecedencias:
    """Analiza la viabilidad de un plan de producción industrial usando DFS."""
    
    def __init__(self):
        self.grafo: Dict[str, List[str]] = {}

    def agregar_precedencia(self, tarea_origen: str, tarea_destino: str) -> None:
        """Establece que 'tarea_origen' debe ejecutarse antes que 'tarea_destino'."""
        if tarea_origen not in self.grafo:
            self.grafo[tarea_origen] = []
        if tarea_destino not in self.grafo:
            self.grafo[tarea_destino] = []
        self.grafo[tarea_origen].append(tarea_destino)

    def tiene_ciclo_inviable(self) -> bool:
        """Detecta si hay dependencias circulares mediante DFS iterativo (Simulando recursión)."""
        estados = {nodo: EstadoTarea.NO_VISITADO for nodo in self.grafo}
        
        for nodo_raiz in self.grafo:
            if estados[nodo_raiz] == EstadoTarea.NO_VISITADO:
                # El stack guarda tuplas: (nodo, iterador_de_vecinos)
                # Esto imita exactamente el comportamiento del call stack de la recursión
                stack = [(nodo_raiz, iter(self.grafo[nodo_raiz]))]
                estados[nodo_raiz] = EstadoTarea.PROCESANDO
                
                while stack:
                    nodo_actual, vecinos_iter = stack[-1]
                    
                    try:
                        # Intentamos obtener el siguiente vecino sin procesar
                        vecino = next(vecinos_iter)
                        
                        if estados[vecino] == EstadoTarea.PROCESANDO:
                            return True  # ¡Ciclo detectado! Dependencia inviable.
                        
                        if estados[vecino] == EstadoTarea.NO_VISITADO:
                            estados[vecino] = EstadoTarea.PROCESANDO
                            stack.append((vecino, iter(self.grafo[vecino])))
                            
                    except StopIteration:
                        # Si ya no quedan vecinos por explorar, sacamos el nodo del stack
                        stack.pop()
                        estados[nodo_actual] = EstadoTarea.PROCESADO
                        
        return False

# Ejemplo rápido de uso en IO
analizador = AnalizadorPrecedencias()
analizador.agregar_precedencia("Inyección de Plástico", "Ensamblaje Base")
analizador.agregar_precedencia("Ensamblaje Base", "Control de Calidad")
analizador.agregar_precedencia("Control de Calidad", "Inyección de Plástico") # Ciclo malicioso

print(f"¿El plan de producción es inviable por ciclos?: {analizador.tiene_ciclo_inviable()}")
