"""Ejercicio 21: Secuenciación de Proyectos (Algoritmo CPM / PERT preliminar)

Dada una red de actividades de un proyecto de infraestructura civis sin cilos (DAG), necesitas generar el Orden
Topológico de las tareas utilizando DFS. Este orden es el que le dice al gerente de operaciones en qué secuencia
exacta debe ejecutar las actividades para que ninguna violes sus restricciones de precedencia. """

from enum import Enum
from typing import Dict, List, Set, Optional

class EstadoTarea(Enum):
    NO_VISITADO = 0
    PROCESANDO = 1  # En el stack actual (detecta ciclos)
    PROCESADO = 2   # Completamente explorado

class SecuenciadorProyectos:
    """Genera el orden topológico de tareas en un proyecto usando DFS."""
    
    def __init__(self):
        self.grafo: Dict[str, List[str]] = {}
        self.orden_topologico: List[str] = []

    def agregar_precedencia(self, tarea_origen: str, tarea_destino: str) -> None:
        """Establece que 'tarea_origen' debe ejecutarse antes que 'tarea_destino'."""
        if tarea_origen not in self.grafo:
            self.grafo[tarea_origen] = []
        if tarea_destino not in self.grafo:
            self.grafo[tarea_destino] = []
        self.grafo[tarea_origen].append(tarea_destino)

    def generar_orden_topologico(self) -> Optional[List[str]]:
        """
        Genera el orden topológico de las tareas usando DFS.
        
        Returns:
            List[str]: Orden topológico de ejecución (de más temprano a más tardío)
            None: Si el grafo tiene ciclos (proyecto inviable)
        """
        estados = {nodo: EstadoTarea.NO_VISITADO for nodo in self.grafo}
        self.orden_topologico = []
        
        for nodo_raiz in self.grafo:
            if estados[nodo_raiz] == EstadoTarea.NO_VISITADO:
                if not self._dfs_recursivo(nodo_raiz, estados):
                    return None  # Ciclo detectado, proyecto inviable
        
        # El orden topológico es el reverso del orden de finalización
        return list(reversed(self.orden_topologico))

    def _dfs_recursivo(self, nodo: str, estados: Dict[str, EstadoTarea]) -> bool:
        """
        DFS recursivo que construye el orden topológico.
        
        Returns:
            bool: True si el grafo es acíclico, False si detecta ciclo
        """
        estados[nodo] = EstadoTarea.PROCESANDO
        
        for vecino in self.grafo[nodo]:
            if estados[vecino] == EstadoTarea.PROCESANDO:
                return False  # Ciclo detectado
            if estados[vecino] == EstadoTarea.NO_VISITADO:
                if not self._dfs_recursivo(vecino, estados):
                    return False
        
        estados[nodo] = EstadoTarea.PROCESADO
        self.orden_topologico.append(nodo)  # Añadir al orden al terminar
        return True

    def mostrar_secuencia(self) -> None:
        """Muestra de forma clara la secuencia de ejecución."""
        orden = self.generar_orden_topologico()
        
        if orden is None:
            print("ERROR: El proyecto tiene dependencias circulares (ciclos).")
            print("No se puede generar un orden topológico válido.")
            return
        
        print("SECUENCIA ÓPTIMA DE EJECUCIÓN (Orden Topológico):")
        print("-" * 60)
        for i, tarea in enumerate(orden, 1):
            print(f"{i:2}. {tarea}")
        print("-" * 60)
        print(f"Total de tareas secuenciadas: {len(orden)}")
        print("\nEl orden topológico garantiza que todas las dependencias se respetan.")


# ===== EJEMPLO DE USO =====
# Proyecto de infraestructura civil
secuenciador = SecuenciadorProyectos()

# Agregamos las dependencias del proyecto
secuenciador.agregar_precedencia("Estudios de Suelo", "Diseño de Cimentación")
secuenciador.agregar_precedencia("Estudios de Suelo", "Planificación de Recursos")
secuenciador.agregar_precedencia("Diseño de Cimentación", "Excavación")
secuenciador.agregar_precedencia("Planificación de Recursos", "Compra de Materiales")
secuenciador.agregar_precedencia("Compra de Materiales", "Fundaciones")
secuenciador.agregar_precedencia("Excavación", "Fundaciones")
secuenciador.agregar_precedencia("Fundaciones", "Levantamiento de Estructura")
secuenciador.agregar_precedencia("Levantamiento de Estructura", "Instalaciones Eléctricas")
secuenciador.agregar_precedencia("Levantamiento de Estructura", "Instalaciones Sanitarias")
secuenciador.agregar_precedencia("Instalaciones Eléctricas", "Acabados")
secuenciador.agregar_precedencia("Instalaciones Sanitarias", "Acabados")

# Mostramos la secuencia
secuenciador.mostrar_secuencia()

print("\n" + "="*60)
print("VERIFICACIÓN DE DEPENDENCIAS:")
print("="*60)
orden = secuenciador.generar_orden_topologico()
if orden:
    # Verificamos que todas las dependencias se respeten
    posicion = {tarea: i for i, tarea in enumerate(orden)}
    for origen in secuenciador.grafo:
        for destino in secuenciador.grafo[origen]:
            if posicion[origen] > posicion[destino]:
                print(f"VIOLACIÓN: {origen} debe ir antes que {destino}")
            else:
                print(f"Correcto: {origen} → {destino} (pos {posicion[origen]} < {posicion[destino]})")
