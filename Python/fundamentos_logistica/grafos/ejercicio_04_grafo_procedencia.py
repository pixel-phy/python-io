""" Grafo de Procedencia de Proyectos (CPM/PERT)
Para optimizar una línea de ensamblaje, ciertas áreas deben realizarse antes que otras
(Grafo Dirigido Acíclico). Crea una clase ProjectNetwork. Añade un método que reciba una tarea y 
devuelva una lista de todas sus procedencias inmediatas y otra de sus sucesoras inmediatas. 
"""

from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict, deque
import enum

class EstadoTarea(enum.Enum):
    """Estados posibles de una tarea en el proyecto"""
    PENDIENTE = "pendiente"
    EN_PROGRESO = "en_progreso"
    COMPLETADA = "completada"
    BLOQUEADA = "bloqueada"

class ProjectNetwork:
    """
    Clase que representa una red de procedencia de proyectos (CPM/PERT).
    
    Características:
    - Grafo Dirigido Acíclico (DAG)
    - Permite gestionar dependencias entre tareas
    - Calcula predecesores y sucesores inmediatos
    - Soporta análisis de rutas críticas
    - Validación de ciclos (garantiza DAG)
    """
    
    def __init__(self, nombre_proyecto: str = "Proyecto"):
        """
        Inicializa la red del proyecto
        
        Args:
            nombre_proyecto: Nombre descriptivo del proyecto
        """
        self.nombre_proyecto = nombre_proyecto
        self.tareas: Dict[str, Dict] = {}  # Almacena información de cada tarea
        self.predecesores: Dict[str, Set[str]] = defaultdict(set)  # Tarea -> {predecesores}
        self.sucesores: Dict[str, Set[str]] = defaultdict(set)  # Tarea -> {sucesores}
        self.duraciones: Dict[str, float] = {}  # Tarea -> duración estimada
        self.estados: Dict[str, EstadoTarea] = {}  # Tarea -> estado actual
        
        # Para cálculos CPM
        self.temprano_inicio: Dict[str, float] = {}
        self.temprano_fin: Dict[str, float] = {}
        self.tardio_inicio: Dict[str, float] = {}
        self.tardio_fin: Dict[str, float] = {}
        self.holgura: Dict[str, float] = {}
        
    def agregar_tarea(self, nombre: str, duracion: float = 1.0, 
                      descripcion: str = "") -> None:
        """
        Agrega una nueva tarea al proyecto
        
        Args:
            nombre: Identificador único de la tarea
            duracion: Tiempo estimado de ejecución
            descripcion: Descripción opcional de la tarea
        """
        if nombre in self.tareas:
            raise ValueError(f"La tarea '{nombre}' ya existe en el proyecto")
        
        self.tareas[nombre] = {
            'nombre': nombre,
            'duracion': duracion,
            'descripcion': descripcion,
            'estado': EstadoTarea.PENDIENTE
        }
        self.duraciones[nombre] = duracion
        self.estados[nombre] = EstadoTarea.PENDIENTE
        self.predecesores[nombre] = set()
        self.sucesores[nombre] = set()
    
    def agregar_dependencia(self, tarea_origen: str, tarea_destino: str) -> None:
        """
        Agrega una dependencia: tarea_origen -> tarea_destino
        (tarea_origen debe completarse antes que tarea_destino)
        
        Args:
            tarea_origen: Tarea precedente
            tarea_destino: Tarea sucesora
        """
        # Validar que ambas tareas existan
        if tarea_origen not in self.tareas:
            raise ValueError(f"La tarea origen '{tarea_origen}' no existe")
        if tarea_destino not in self.tareas:
            raise ValueError(f"La tarea destino '{tarea_destino}' no existe")
        
        # Validar que no se cree un ciclo (mantener DAG)
        if self._crea_ciclo(tarea_origen, tarea_destino):
            raise ValueError(f"Agregar dependencia '{tarea_origen}->{tarea_destino}' crearía un ciclo")
        
        # Agregar dependencia
        self.sucesores[tarea_origen].add(tarea_destino)
        self.predecesores[tarea_destino].add(tarea_origen)
    
    def _crea_ciclo(self, origen: str, destino: str) -> bool:
        """
        Verifica si agregar la arista origen->destino crearía un ciclo
        
        Args:
            origen: Tarea de origen
            destino: Tarea de destino
        
        Returns:
            bool: True si crea ciclo, False en caso contrario
        """
        # Si destino ya tiene un camino a origen, se crearía ciclo
        visitados = set()
        pila = [destino]
        
        while pila:
            actual = pila.pop()
            if actual == origen:
                return True
            if actual in visitados:
                continue
            visitados.add(actual)
            # Agregar todos los sucesores de actual
            pila.extend(self.sucesores.get(actual, []))
        
        return False
    
    def obtener_predecesores_inmediatos(self, tarea: str) -> List[str]:
        """
        Retorna los predecesores inmediatos de una tarea
        
        Args:
            tarea: Nombre de la tarea
            
        Returns:
            List[str]: Lista de tareas que deben completarse antes
        """
        if tarea not in self.tareas:
            raise ValueError(f"La tarea '{tarea}' no existe en el proyecto")
        
        return sorted(list(self.predecesores.get(tarea, set())))
    
    def obtener_sucesores_inmediatos(self, tarea: str) -> List[str]:
        """
        Retorna los sucesores inmediatos de una tarea
        
        Args:
            tarea: Nombre de la tarea
            
        Returns:
            List[str]: Lista de tareas que dependen de esta
        """
        if tarea not in self.tareas:
            raise ValueError(f"La tarea '{tarea}' no existe en el proyecto")
        
        return sorted(list(self.sucesores.get(tarea, set())))
    
    def obtener_predecesores_todos(self, tarea: str) -> Set[str]:
        """
        Retorna TODOS los predecesores (directos e indirectos) de una tarea
        
        Args:
            tarea: Nombre de la tarea
            
        Returns:
            Set[str]: Conjunto de todas las tareas precedentes
        """
        if tarea not in self.tareas:
            raise ValueError(f"La tarea '{tarea}' no existe en el proyecto")
        
        todos_predecesores = set()
        pila = list(self.predecesores.get(tarea, set()))
        
        while pila:
            actual = pila.pop()
            if actual not in todos_predecesores:
                todos_predecesores.add(actual)
                pila.extend(self.predecesores.get(actual, set()))
        
        return todos_predecesores
    
    def obtener_sucesores_todos(self, tarea: str) -> Set[str]:
        """
        Retorna TODOS los sucesores (directos e indirectos) de una tarea
        
        Args:
            tarea: Nombre de la tarea
            
        Returns:
            Set[str]: Conjunto de todas las tareas sucesoras
        """
        if tarea not in self.tareas:
            raise ValueError(f"La tarea '{tarea}' no existe en el proyecto")
        
        todos_sucesores = set()
        pila = list(self.sucesores.get(tarea, set()))
        
        while pila:
            actual = pila.pop()
            if actual not in todos_sucesores:
                todos_sucesores.add(actual)
                pila.extend(self.sucesores.get(actual, set()))
        
        return todos_sucesores
    
    def calcular_cpm(self) -> Dict:
        """
        Calcula los parámetros CPM (Critical Path Method)
        
        Returns:
            Dict con toda la información del análisis CPM
        """
        # Verificar que el grafo sea acíclico
        if not self._es_dag():
            raise ValueError("El grafo contiene ciclos, no se puede calcular CPM")
        
        # Encontrar tareas iniciales (sin predecesores)
        tareas_iniciales = [t for t in self.tareas if not self.predecesores.get(t, set())]
        if not tareas_iniciales:
            raise ValueError("No hay tareas iniciales en el proyecto")
        
        # PASO 1: Calcular tiempos tempranos (forward pass)
        self.temprano_inicio = {}
        self.temprano_fin = {}
        
        # Orden topológico
        orden_topologico = self._orden_topologico()
        
        for tarea in orden_topologico:
            if tarea in tareas_iniciales:
                self.temprano_inicio[tarea] = 0
            else:
                # El inicio temprano es el máximo de los fines tempranos de sus predecesores
                max_fin = 0
                for pred in self.predecesores.get(tarea, set()):
                    if pred in self.temprano_fin:
                        max_fin = max(max_fin, self.temprano_fin[pred])
                self.temprano_inicio[tarea] = max_fin
            
            self.temprano_fin[tarea] = self.temprano_inicio[tarea] + self.duraciones[tarea]
        
        # Duración total del proyecto
        duracion_total = max(self.temprano_fin.values()) if self.temprano_fin else 0
        
        # PASO 2: Calcular tiempos tardíos (backward pass)
        self.tardio_fin = {}
        self.tardio_inicio = {}
        
        # Inicializar tareas finales (sin sucesores)
        tareas_finales = [t for t in self.tareas if not self.sucesores.get(t, set())]
        
        for tarea in reversed(orden_topologico):
            if tarea in tareas_finales:
                self.tardio_fin[tarea] = duracion_total
            else:
                # El fin tardío es el mínimo de los inicios tardíos de sus sucesores
                min_inicio = float('inf')
                for suc in self.sucesores.get(tarea, set()):
                    if suc in self.tardio_inicio:
                        min_inicio = min(min_inicio, self.tardio_inicio[suc])
                self.tardio_fin[tarea] = min_inicio
            
            self.tardio_inicio[tarea] = self.tardio_fin[tarea] - self.duraciones[tarea]
        
        # PASO 3: Calcular holguras
        self.holgura = {}
        for tarea in self.tareas:
            self.holgura[tarea] = self.tardio_inicio[tarea] - self.temprano_inicio[tarea]
        
        # PASO 4: Identificar ruta crítica
        ruta_critica = [t for t in self.tareas if abs(self.holgura[tarea]) < 1e-9]
        
        return {
            'duracion_total': duracion_total,
            'ruta_critica': sorted(ruta_critica),
            'temprano_inicio': self.temprano_inicio,
            'temprano_fin': self.temprano_fin,
            'tardio_inicio': self.tardio_inicio,
            'tardio_fin': self.tardio_fin,
            'holgura': self.holgura
        }
    
    def _orden_topologico(self) -> List[str]:
        """
        Realiza un ordenamiento topológico del DAG usando Kahn's algorithm
        
        Returns:
            List[str]: Lista de tareas en orden topológico
        """
        # Calcular grados de entrada
        grados_entrada = {t: len(self.predecesores.get(t, set())) for t in self.tareas}
        
        # Cola de tareas sin predecesores
        cola = deque([t for t in self.tareas if grados_entrada[t] == 0])
        orden = []
        
        while cola:
            tarea = cola.popleft()
            orden.append(tarea)
            
            # Reducir grados de entrada de los sucesores
            for sucesor in self.sucesores.get(tarea, set()):
                grados_entrada[sucesor] -= 1
                if grados_entrada[sucesor] == 0:
                    cola.append(sucesor)
        
        if len(orden) != len(self.tareas):
            raise ValueError("El grafo tiene ciclos (no es DAG)")
        
        return orden
    
    def _es_dag(self) -> bool:
        """
        Verifica si el grafo es acíclico (DAG)
        
        Returns:
            bool: True si es DAG, False en caso contrario
        """
        try:
            self._orden_topologico()
            return True
        except ValueError:
            return False
    
    def obtener_nivel(self, tarea: str) -> int:
        """
        Calcula el nivel de profundidad de una tarea en el DAG
        
        Args:
            tarea: Nombre de la tarea
            
        Returns:
            int: Nivel (0 para tareas iniciales)
        """
        if tarea not in self.tareas:
            raise ValueError(f"La tarea '{tarea}' no existe en el proyecto")
        
        if not self.predecesores.get(tarea, set()):
            return 0
        
        return 1 + max(self.obtener_nivel(pred) for pred in self.predecesores[tarea])
    
    def tareas_por_nivel(self) -> Dict[int, List[str]]:
        """
        Agrupa tareas por nivel de profundidad
        
        Returns:
            Dict[int, List[str]]: Nivel -> Lista de tareas
        """
        niveles = defaultdict(list)
        for tarea in self.tareas:
            nivel = self.obtener_nivel(tarea)
            niveles[nivel].append(tarea)
        
        return dict(niveles)
    
    def mostrar_informacion_tarea(self, tarea: str, detallado: bool = False) -> None:
        """
        Muestra información detallada de una tarea
        
        Args:
            tarea: Nombre de la tarea
            detallado: Si muestra información adicional de CPM
        """
        if tarea not in self.tareas:
            print(f"La tarea '{tarea}' no existe en el proyecto")
            return
        
        print(f"\n{'='*60}")
        print(f"TAREA: {tarea}")
        
        # Información básica
        info = self.tareas[tarea]
        print(f"Descripción: {info['descripcion'] or 'Sin descripción'}")
        print(f"Duración: {info['duracion']} unidades")
        print(f"Estado: {info['estado'].value}")
        
        # Predecesores inmediatos
        preds = self.obtener_predecesores_inmediatos(tarea)
        print(f"\nPREDECESORES INMEDIATOS ({len(preds)}):")
        if preds:
            for p in preds:
                print(f"   • {p}")
        else:
            print("   └─ Ninguno (tarea inicial)")
        
        # Sucesores inmediatos
        sucs = self.obtener_sucesores_inmediatos(tarea)
        print(f"\nSUCESORES INMEDIATOS ({len(sucs)}):")
        if sucs:
            for s in sucs:
                print(f"   • {s}")
        else:
            print("   └─ Ninguno (tarea final)")
        
        # Todos los predecesores (indirectos)
        todos_preds = self.obtener_predecesores_todos(tarea)
        if todos_preds:
            print(f"\nTODOS LOS PREDECESORES ({len(todos_preds)}):")
            print(f"   {', '.join(sorted(todos_preds))}")
        
        # Todos los sucesores (indirectos)
        todos_sucs = self.obtener_sucesores_todos(tarea)
        if todos_sucs:
            print(f"\nTODOS LOS SUCESORES ({len(todos_sucs)}):")
            print(f"   {', '.join(sorted(todos_sucs))}")
        
        # Nivel en el grafo
        nivel = self.obtener_nivel(tarea)
        print(f"\nNivel en el proyecto: {nivel}")
        
        # Información CPM si está disponible y se solicita
        if detallado and self.temprano_inicio:
            print(f"\nANÁLISIS CPM:")
            print(f"   • Inicio temprano: {self.temprano_inicio[tarea]:.1f}")
            print(f"   • Fin temprano: {self.temprano_fin[tarea]:.1f}")
            print(f"   • Inicio tardío: {self.tardio_inicio[tarea]:.1f}")
            print(f"   • Fin tardío: {self.tardio_fin[tarea]:.1f}")
            print(f"   • Holgura: {self.holgura[tarea]:.1f}")
            
            if abs(self.holgura[tarea]) < 1e-9:
                print("¡TAREA EN RUTA CRÍTICA!")
        
        print(f"\n")
    
    def mostrar_red(self) -> None:
        """Muestra un resumen de toda la red del proyecto"""
        print(f"RED DE PROYECTO: {self.nombre_proyecto}")
        print(f"Total de tareas: {len(self.tareas)}")
        
        # Mostrar tareas por nivel
        niveles = self.tareas_por_nivel()
        print(f"\nTAREAS POR NIVEL:")
        for nivel in sorted(niveles.keys()):
            print(f"  Nivel {nivel}: {', '.join(sorted(niveles[nivel]))}")
        
        # Mostrar dependencias
        print(f"\nDEPENDENCIAS:")
        for tarea in sorted(self.tareas):
            preds = self.obtener_predecesores_inmediatos(tarea)
            if preds:
                print(f"  {tarea} ← {', '.join(preds)}")
            else:
                print(f"  {tarea} ← (inicial)")
        
        # Mostrar estadísticas
        if self.temprano_inicio:
            cpm = self.calcular_cpm()
            print(f"\nESTADÍSTICAS CPM:")
            print(f"  • Duración total del proyecto: {cpm['duracion_total']:.1f} unidades")
            print(f"  • Tareas en ruta crítica: {', '.join(cpm['ruta_critica'])}")
        
        print(f"\n")


# Pruebas

def crear_proyecto_ensamblaje() -> ProjectNetwork:
    """Crea un proyecto de ensamblaje de ejemplo"""
    proyecto = ProjectNetwork("Línea de Ensamblaje Automotriz")
    
    # Agregar tareas con duraciones
    tareas = [
        ("Diseño", 5.0, "Diseño del producto final"),
        ("Ingeniería", 4.0, "Ingeniería detallada"),
        ("Prototipo", 3.0, "Fabricación del prototipo"),
        ("Pruebas", 2.0, "Pruebas de calidad"),
        ("Suministros", 6.0, "Adquisición de materiales"),
        ("Fabricación", 8.0, "Fabricación de componentes"),
        ("Ensamblaje", 4.0, "Ensamblaje final"),
        ("ControlCalidad", 2.0, "Control de calidad final"),
        ("Empaque", 1.0, "Empaque y envío")
    ]
    
    for nombre, duracion, desc in tareas:
        proyecto.agregar_tarea(nombre, duracion, desc)
    
    # Agregar dependencias
    dependencias = [
        ("Diseño", "Ingeniería"),
        ("Diseño", "Prototipo"),
        ("Ingeniería", "Fabricación"),
        ("Ingeniería", "Suministros"),
        ("Prototipo", "Pruebas"),
        ("Suministros", "Fabricación"),
        ("Pruebas", "Fabricación"),
        ("Fabricación", "Ensamblaje"),
        ("Ensamblaje", "ControlCalidad"),
        ("ControlCalidad", "Empaque")
    ]
    
    for origen, destino in dependencias:
        proyecto.agregar_dependencia(origen, destino)
    
    return proyecto


def crear_proyecto_software() -> ProjectNetwork:
    """Crea un proyecto de desarrollo de software de ejemplo"""
    proyecto = ProjectNetwork("Desarrollo de Software")
    
    # Tareas
    proyecto.agregar_tarea("Requisitos", 3.0, "Recolección de requisitos")
    proyecto.agregar_tarea("DiseñoArquitectura", 4.0, "Diseño de arquitectura")
    proyecto.agregar_tarea("DiseñoBD", 2.0, "Diseño de base de datos")
    proyecto.agregar_tarea("DesarrolloBackend", 10.0, "Desarrollo del backend")
    proyecto.agregar_tarea("DesarrolloFrontend", 8.0, "Desarrollo del frontend")
    proyecto.agregar_tarea("APIs", 5.0, "Desarrollo de APIs")
    proyecto.agregar_tarea("PruebasUnitarias", 4.0, "Pruebas unitarias")
    proyecto.agregar_tarea("Integracion", 3.0, "Integración de sistemas")
    proyecto.agregar_tarea("PruebasQA", 5.0, "Pruebas de calidad")
    proyecto.agregar_tarea("Despliegue", 2.0, "Despliegue en producción")
    proyecto.agregar_tarea("Documentacion", 3.0, "Documentación del sistema")
    
    # Dependencias
    dependencias = [
        ("Requisitos", "DiseñoArquitectura"),
        ("Requisitos", "DiseñoBD"),
        ("DiseñoArquitectura", "DesarrolloBackend"),
        ("DiseñoArquitectura", "DesarrolloFrontend"),
        ("DiseñoBD", "DesarrolloBackend"),
        ("DiseñoBD", "APIs"),
        ("DesarrolloBackend", "PruebasUnitarias"),
        ("DesarrolloFrontend", "PruebasUnitarias"),
        ("APIs", "PruebasUnitarias"),
        ("PruebasUnitarias", "Integracion"),
        ("Integracion", "PruebasQA"),
        ("PruebasQA", "Despliegue"),
        ("Despliegue", "Documentacion")
    ]
    
    for origen, destino in dependencias:
        proyecto.agregar_dependencia(origen, destino)
    
    return proyecto


if __name__ == "__main__":

    print("ANÁLISIS DE RED DE PROYECTO (CPM/PERT)")
    
    # Crear proyecto de ensamblaje
    proyecto = crear_proyecto_ensamblaje()
    
    # Mostrar información de una tarea específica
    proyecto.mostrar_informacion_tarea("Fabricación", detallado=True)
    
    # Mostrar predecesores y sucesores de otra tarea
    print("\n")
    print("ANÁLISIS DE TAREA: Ensamblaje")
    
    predecesores = proyecto.obtener_predecesores_inmediatos("Ensamblaje")
    sucesores = proyecto.obtener_sucesores_inmediatos("Ensamblaje")
    
    print(f"Predecesores inmediatos: {predecesores}")
    print(f"Sucesores inmediatos: {sucesores}")
    
    # Mostrar todos los predecesores de una tarea
    todos_preds = proyecto.obtener_predecesores_todos("Ensamblaje")
    print(f"\nTodos los predecesores de 'Ensamblaje':")
    print(f"   {', '.join(sorted(todos_preds))}")
    
    # Calcular y mostrar CPM
    print("\n")
    print("ANÁLISIS CPM DEL PROYECTO")
    
    cpm = proyecto.calcular_cpm()
    print(f"Duración total del proyecto: {cpm['duracion_total']:.1f} unidades")
    print(f"Ruta crítica: {' → '.join(cpm['ruta_critica'])}")
    
    # Mostrar holguras
    print(f"\nHOLGURAS DE TAREAS:")
    for tarea, holgura in sorted(cpm['holgura'].items(), key=lambda x: x[1]):
        if abs(holgura) < 1e-9:
            print(f"  • {tarea}: {holgura:.1f} (Crítica)")
        else:
            print(f"  • {tarea}: {holgura:.1f}")
    
    # Mostrar vista completa de la red
    proyecto.mostrar_red()
    
    # Ejemplo de otro proyecto
    print("\n")
    print("PROYECTO DE DESARROLLO DE SOFTWARE")
    
    proyecto_software = crear_proyecto_software()
    proyecto_software.mostrar_informacion_tarea("DesarrolloBackend", detallado=True)
