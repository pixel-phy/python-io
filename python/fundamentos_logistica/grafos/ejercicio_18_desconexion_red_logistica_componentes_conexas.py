"""Ejercicio 18: Desconexión de Red Logística y Componentes Conexas

A veces, las huelgas de transporte o desastres naturales dividen un país en sub-regiones
aisladas, impidiendo que los camiones viajen de una zona a otra. Escribe un algoritmo basado
en BFS que reciba una red de carreteras (lista de adyacencia no dirigida) e identifique cuántas
regiones logísticas independientes (componentes conexas) han quedado asiladas y cuáles 
son las ciudades que integran cada región. """

from typing import Dict, List, Set, Tuple, Optional, Any
from collections import deque, defaultdict
from dataclasses import dataclass, field
from enum import Enum
import math

class EstadoRegion(Enum):
    """Estado de una región logística"""
    OPERATIVA = "operativa"
    AISLADA = "aislada"
    PARCIALMENTE_CONECTADA = "parcialmente_conectada"
    CRITICA = "critica"

@dataclass
class Ciudad:
    """Información de una ciudad en la red"""
    nombre: str
    poblacion: int = 0
    capacidad_logistica: float = 0.0
    tiene_puerto: bool = False
    tiene_aeropuerto: bool = False
    es_capital: bool = False

@dataclass
class RegionLogistica:
    """Representa una región logística aislada"""
    id: int
    ciudades: List[str]
    tamaño: int
    estado: EstadoRegion
    ciudades_info: Dict[str, Ciudad] = field(default_factory=dict)
    conexiones_internas: int = 0
    capacidad_total: float = 0.0
    poblacion_total: int = 0
    tiene_infraestructura_critica: bool = False

class RedLogisticaDesconectada:
    """
    Análisis de desconexión de red logística y componentes conexas.
    
    Características:
    - Identificación de componentes conexas mediante BFS
    - Análisis de regiones aisladas
    - Estadísticas por región
    - Identificación de puntos críticos
    - Simulación de desconexiones
    - Recomendaciones de conectividad
    """
    
    def __init__(self, nombre: str = "Red Logística Nacional"):
        """
        Inicializa la red logística
        
        Args:
            nombre: Nombre identificativo de la red
        """
        self.nombre = nombre
        self.adyacencia: Dict[str, Set[str]] = defaultdict(set)
        self.ciudades_info: Dict[str, Ciudad] = {}
        self.total_ciudades = 0
        self.total_carreteras = 0
        
        # Cache de análisis
        self.cache_componentes: Dict[str, List[RegionLogistica]] = {}
        self.cache_estadisticas: Dict[str, Dict] = {}
    
    def agregar_ciudad(self, nombre: str, poblacion: int = 0, 
                       capacidad_logistica: float = 0.0,
                       tiene_puerto: bool = False,
                       tiene_aeropuerto: bool = False,
                       es_capital: bool = False) -> None:
        """
        Agrega una ciudad a la red
        
        Args:
            nombre: Nombre de la ciudad
            poblacion: Número de habitantes
            capacidad_logistica: Capacidad de procesamiento logístico
            tiene_puerto: Si tiene puerto marítimo
            tiene_aeropuerto: Si tiene aeropuerto
            es_capital: Si es capital de región/provincia
        """
        if nombre in self.ciudades_info:
            raise ValueError(f"La ciudad '{nombre}' ya existe en la red")
        
        self.ciudades_info[nombre] = Ciudad(
            nombre=nombre,
            poblacion=poblacion,
            capacidad_logistica=capacidad_logistica,
            tiene_puerto=tiene_puerto,
            tiene_aeropuerto=tiene_aeropuerto,
            es_capital=es_capital
        )
        self.total_ciudades += 1
    
    def agregar_carretera(self, ciudad1: str, ciudad2: str) -> None:
        """
        Agrega una carretera bidireccional entre dos ciudades
        
        Args:
            ciudad1: Primera ciudad
            ciudad2: Segunda ciudad
        """
        if ciudad1 not in self.ciudades_info:
            raise ValueError(f"La ciudad '{ciudad1}' no existe")
        if ciudad2 not in self.ciudades_info:
            raise ValueError(f"La ciudad '{ciudad2}' no existe")
        if ciudad1 == ciudad2:
            raise ValueError("No se puede conectar una ciudad consigo misma")
        
        self.adyacencia[ciudad1].add(ciudad2)
        self.adyacencia[ciudad2].add(ciudad1)
        self.total_carreteras += 1
    
    def eliminar_ciudad(self, ciudad: str) -> None:
        """
        Simula la desconexión de una ciudad (elimina la ciudad y sus conexiones)
        
        Args:
            ciudad: Ciudad a eliminar
        """
        if ciudad not in self.ciudades_info:
            raise ValueError(f"La ciudad '{ciudad}' no existe")
        
        # Eliminar todas las conexiones de la ciudad
        for vecino in list(self.adyacencia.get(ciudad, set())):
            self.adyacencia[vecino].discard(ciudad)
            self.total_carreteras -= 1
        
        # Eliminar la ciudad
        self.adyacencia.pop(ciudad, None)
        self.ciudades_info.pop(ciudad, None)
        self.total_ciudades -= 1
    
    def eliminar_carretera(self, ciudad1: str, ciudad2: str) -> None:
        """
        Simula la desconexión de una carretera
        
        Args:
            ciudad1: Primera ciudad
            ciudad2: Segunda ciudad
        """
        if ciudad1 not in self.adyacencia or ciudad2 not in self.adyacencia:
            raise ValueError("Una de las ciudades no existe o no está conectada")
        
        if ciudad2 in self.adyacencia[ciudad1]:
            self.adyacencia[ciudad1].discard(ciudad2)
            self.adyacencia[ciudad2].discard(ciudad1)
            self.total_carreteras -= 1
    
    def encontrar_componentes_conexas(self, 
                                     incluir_detalles: bool = True) -> List[RegionLogistica]:
        """
        Encuentra todas las componentes conexas de la red usando BFS
        
        Args:
            incluir_detalles: Si incluye información detallada de cada región
            
        Returns:
            Lista de RegionLogistica con todas las componentes
        """
        if not self.ciudades_info:
            return []
        
        # Verificar cache
        cache_key = f"comp_{self.total_ciudades}_{self.total_carreteras}"
        if cache_key in self.cache_componentes:
            return self.cache_componentes[cache_key]
        
        visitados: Set[str] = set()
        componentes: List[RegionLogistica] = []
        region_id = 0
        
        for ciudad in self.ciudades_info:
            if ciudad not in visitados:
                # BFS para encontrar todos los nodos de esta componente
                componente_nodos: List[str] = []
                cola: deque = deque([ciudad])
                visitados.add(ciudad)
                
                while cola:
                    nodo_actual = cola.popleft()
                    componente_nodos.append(nodo_actual)
                    
                    for vecino in self.adyacencia.get(nodo_actual, set()):
                        if vecino not in visitados:
                            visitados.add(vecino)
                            cola.append(vecino)
                
                # Crear región
                region = self._crear_region(region_id, componente_nodos, incluir_detalles)
                componentes.append(region)
                region_id += 1
        
        # Guardar en cache
        self.cache_componentes[cache_key] = componentes
        
        # Actualizar estadísticas
        self._actualizar_estadisticas(componentes)
        
        return componentes
    
    def _crear_region(self, region_id: int, nodos: List[str], 
                     incluir_detalles: bool) -> RegionLogistica:
        """
        Crea un objeto RegionLogistica a partir de una lista de nodos
        """
        # Calcular conexiones internas
        conexiones_internas = 0
        for ciudad in nodos:
            for vecino in self.adyacencia.get(ciudad, set()):
                if vecino in nodos:
                    conexiones_internas += 1
        conexiones_internas //= 2  # Cada conexión se cuenta dos veces
        
        # Calcular estadísticas
        poblacion_total = 0
        capacidad_total = 0.0
        tiene_infraestructura_critica = False
        ciudades_info = {}
        
        for ciudad in nodos:
            info = self.ciudades_info.get(ciudad)
            if info:
                poblacion_total += info.poblacion
                capacidad_total += info.capacidad_logistica
                if info.tiene_puerto or info.tiene_aeropuerto or info.es_capital:
                    tiene_infraestructura_critica = True
                if incluir_detalles:
                    ciudades_info[ciudad] = info
        
        # Determinar estado de la región
        estado = self._determinar_estado_region(nodos, conexiones_internas)
        
        return RegionLogistica(
            id=region_id,
            ciudades=nodos,
            tamaño=len(nodos),
            estado=estado,
            ciudades_info=ciudades_info if incluir_detalles else {},
            conexiones_internas=conexiones_internas,
            capacidad_total=capacidad_total,
            poblacion_total=poblacion_total,
            tiene_infraestructura_critica=tiene_infraestructura_critica
        )
    
    def _determinar_estado_region(self, nodos: List[str], conexiones_internas: int) -> EstadoRegion:
        """
        Determina el estado de una región basado en su tamaño y conectividad
        """
        if len(nodos) == 1:
            return EstadoRegion.AISLADA
        
        # Calcular densidad de conexiones
        max_conexiones = len(nodos) * (len(nodos) - 1) / 2
        densidad = conexiones_internas / max_conexiones if max_conexiones > 0 else 0
        
        if densidad >= 0.7:
            return EstadoRegion.OPERATIVA
        elif densidad >= 0.4:
            return EstadoRegion.PARCIALMENTE_CONECTADA
        else:
            return EstadoRegion.CRITICA
    
    def _actualizar_estadisticas(self, componentes: List[RegionLogistica]) -> None:
        """Actualiza estadísticas globales"""
        stats = {
            'total_regiones': len(componentes),
            'ciudades_totales': self.total_ciudades,
            'regiones_operativas': 0,
            'regiones_aisladas': 0,
            'regiones_criticas': 0,
            'mayor_region': None,
            'menor_region': None,
            'poblacion_total': 0,
            'capacidad_total': 0
        }
        
        for region in componentes:
            if region.estado == EstadoRegion.OPERATIVA:
                stats['regiones_operativas'] += 1
            elif region.estado == EstadoRegion.AISLADA:
                stats['regiones_aisladas'] += 1
            elif region.estado == EstadoRegion.CRITICA:
                stats['regiones_criticas'] += 1
            
            stats['poblacion_total'] += region.poblacion_total
            stats['capacidad_total'] += region.capacidad_total
            
            # Mayor y menor región
            if not stats['mayor_region'] or region.tamaño > stats['mayor_region'].tamaño:
                stats['mayor_region'] = region
            if not stats['menor_region'] or region.tamaño < stats['menor_region'].tamaño:
                stats['menor_region'] = region
        
        self.cache_estadisticas['global'] = stats
    
    def analizar_desconexiones(self) -> Dict[str, Any]:
        """
        Analiza el impacto de las desconexiones en la red
        
        Returns:
            Dict con análisis detallado
        """
        componentes = self.encontrar_componentes_conexas()
        stats = self.cache_estadisticas.get('global', {})
        
        # Identificar ciudades críticas (conectan muchas regiones)
        ciudades_criticas = self._identificar_ciudades_criticas()
        
        # Calcular índice de fragmentación
        indice_fragmentacion = len(componentes) / self.total_ciudades if self.total_ciudades > 0 else 0
        
        # Identificar regiones que necesitan atención
        regiones_atencion = [
            region for region in componentes 
            if region.estado in [EstadoRegion.AISLADA, EstadoRegion.CRITICA]
        ]
        
        return {
            'total_regiones': len(componentes),
            'ciudades_totales': self.total_ciudades,
            'indice_fragmentacion': indice_fragmentacion,
            'regiones_operativas': stats.get('regiones_operativas', 0),
            'regiones_aisladas': stats.get('regiones_aisladas', 0),
            'regiones_criticas': stats.get('regiones_criticas', 0),
            'ciudades_criticas': ciudades_criticas,
            'regiones_atencion': regiones_atencion,
            'mayor_region': stats.get('mayor_region'),
            'menor_region': stats.get('menor_region'),
            'poblacion_total_aislada': sum(r.poblacion_total for r in regiones_atencion),
            'capacidad_total_aislada': sum(r.capacidad_total for r in regiones_atencion),
            'nivel_afectacion': self._calcular_nivel_afectacion(componentes)
        }
    
    def _identificar_ciudades_criticas(self) -> List[Dict[str, Any]]:
        """
        Identifica ciudades que son críticas para la conectividad
        """
        ciudades_criticas = []
        
        for ciudad in self.ciudades_info:
            # Si eliminar esta ciudad desconecta la red
            if self._es_ciudad_critica(ciudad):
                # Calcular impacto de su desconexión
                componentes_originales = len(self.encontrar_componentes_conexas())
                
                # Simular eliminación
                vecinos = list(self.adyacencia.get(ciudad, set()))
                for vecino in vecinos:
                    self.adyacencia[vecino].discard(ciudad)
                self.adyacencia.pop(ciudad, None)
                
                nuevos_componentes = self.encontrar_componentes_conexas()
                
                # Restaurar
                for vecino in vecinos:
                    self.adyacencia[vecino].add(ciudad)
                self.adyacencia[ciudad] = set(vecinos)
                
                ciudades_criticas.append({
                    'ciudad': ciudad,
                    'impacto': len(nuevos_componentes) - componentes_originales,
                    'conexiones': len(vecinos),
                    'info': self.ciudades_info[ciudad]
                })
        
        # Ordenar por impacto (descendente)
        ciudades_criticas.sort(key=lambda x: x['impacto'], reverse=True)
        
        return ciudades_criticas[:5]  # Top 5
    
    def _es_ciudad_critica(self, ciudad: str) -> bool:
        """
        Verifica si una ciudad es crítica (su eliminación desconecta la red)
        """
        if ciudad not in self.adyacencia:
            return False
        
        # Si tiene más de 2 conexiones, podría ser crítica
        if len(self.adyacencia[ciudad]) >= 2:
            # Verificar si sus vecinos están conectados entre sí sin la ciudad
            vecinos = list(self.adyacencia[ciudad])
            if len(vecinos) >= 2:
                # BFS desde el primer vecino sin pasar por ciudad
                visitados = set()
                cola = deque([vecinos[0]])
                visitados.add(vecinos[0])
                
                while cola:
                    nodo = cola.popleft()
                    if nodo == ciudad:
                        continue
                    for vecino in self.adyacencia.get(nodo, set()):
                        if vecino not in visitados and vecino != ciudad:
                            visitados.add(vecino)
                            cola.append(vecino)
                
                # Si algún vecino no fue visitado, la ciudad es crítica
                return not all(v in visitados for v in vecinos[1:])
        
        return False
    
    def _calcular_nivel_afectacion(self, componentes: List[RegionLogistica]) -> str:
        """
        Calcula el nivel de afectación de la red
        """
        if len(componentes) <= 1:
            return "NINGUNA"
        
        ratio_aisladas = sum(1 for c in componentes if c.estado == EstadoRegion.AISLADA) / len(componentes)
        ratio_criticas = sum(1 for c in componentes if c.estado == EstadoRegion.CRITICA) / len(componentes)
        
        if ratio_aisladas > 0.3 or ratio_criticas > 0.5:
            return "CRÍTICA"
        elif ratio_aisladas > 0.1 or ratio_criticas > 0.2:
            return "ALTA"
        elif len(componentes) > 3:
            return "MEDIA"
        else:
            return "BAJA"
    
    def simular_desconexion(self, ciudades_afectadas: Set[str]) -> Dict[str, Any]:
        """
        Simula la desconexión de un conjunto de ciudades
        
        Args:
            ciudades_afectadas: Conjunto de ciudades afectadas
            
        Returns:
            Dict con resultados de la simulación
        """
        # Guardar estado original
        adyacencia_original = {k: set(v) for k, v in self.adyacencia.items()}
        ciudades_original = dict(self.ciudades_info)
        
        try:
            # Eliminar ciudades afectadas
            for ciudad in ciudades_afectadas:
                if ciudad in self.ciudades_info:
                    self.eliminar_ciudad(ciudad)
            
            # Analizar nueva configuración
            componentes = self.encontrar_componentes_conexas()
            analisis = self.analizar_desconexiones()
            
            return {
                'ciudades_afectadas': list(ciudades_afectadas),
                'componentes': componentes,
                'analisis': analisis,
                'ciudades_restantes': list(self.ciudades_info.keys())
            }
        
        finally:
            # Restaurar estado original
            self.adyacencia = adyacencia_original
            self.ciudades_info = ciudades_original
            self.total_ciudades = len(ciudades_original)
            # Recalcular total de carreteras
            self.total_carreteras = sum(len(v) for v in self.adyacencia.values()) // 2
            # Limpiar cache
            self.cache_componentes = {}
            self.cache_estadisticas = {}
    
    def recomendar_conexiones(self, max_conexiones: int = 3) -> List[Dict[str, Any]]:
        """
        Recomienda nuevas conexiones para mejorar la conectividad
        
        Args:
            max_conexiones: Número máximo de conexiones a recomendar
            
        Returns:
            Lista de conexiones recomendadas
        """
        componentes = self.encontrar_componentes_conexas()
        
        if len(componentes) <= 1:
            return [{'mensaje': 'La red ya está completamente conectada'}]
        
        recomendaciones = []
        
        # Ordenar regiones por tamaño (de mayor a menor)
        regiones_ordenadas = sorted(componentes, key=lambda r: r.tamaño, reverse=True)
        
        # Conectar las regiones más grandes con las más pequeñas
        for i in range(len(regiones_ordenadas) - 1):
            if len(recomendaciones) >= max_conexiones:
                break
            
            region1 = regiones_ordenadas[i]
            region2 = regiones_ordenadas[i + 1]
            
            # Encontrar la mejor ciudad de cada región para conectar
            ciudad1 = self._mejor_ciudad_conexion(region1)
            ciudad2 = self._mejor_ciudad_conexion(region2)
            
            if ciudad1 and ciudad2:
                recomendaciones.append({
                    'ciudad1': ciudad1,
                    'ciudad2': ciudad2,
                    'region1_id': region1.id,
                    'region2_id': region2.id,
                    'beneficio': region1.tamaño + region2.tamaño,
                    'prioridad': 'ALTA' if i < 2 else 'MEDIA'
                })
        
        return recomendaciones
    
    def _mejor_ciudad_conexion(self, region: RegionLogistica) -> Optional[str]:
        """
        Encuentra la mejor ciudad de una región para hacer conexiones
        """
        if not region.ciudades:
            return None
        
        # Priorizar ciudades con infraestructura crítica
        for ciudad in region.ciudades:
            info = self.ciudades_info.get(ciudad)
            if info and (info.tiene_puerto or info.tiene_aeropuerto or info.es_capital):
                return ciudad
        
        # Si no hay infraestructura crítica, usar la primera ciudad
        return region.ciudades[0]
    
    def mostrar_componentes(self, incluir_detalles: bool = True) -> None:
        """
        Muestra de forma formateada las componentes conexas
        """
        print(f"\n{'='*80}")
        print(f"ANÁLISIS DE COMPONENTES CONEXAS")
        print(f"   Red: {self.nombre}")
        print(f"   Total ciudades: {self.total_ciudades}")
        print(f"   Total carreteras: {self.total_carreteras}")
        print(f"{'='*80}")
        
        componentes = self.encontrar_componentes_conexas()
        
        if not componentes:
            print("No hay ciudades en la red")
            return
        
        print(f"\nRESULTADOS:")
        print(f"   • Componentes encontradas: {len(componentes)}")
        
        # Mostrar estadísticas de cada componente
        for i, region in enumerate(componentes, 1):
            estado_icono = {
                EstadoRegion.OPERATIVA: "Verde",
                EstadoRegion.PARCIALMENTE_CONECTADA: "Amarillo",
                EstadoRegion.AISLADA: "Rojo",
                EstadoRegion.CRITICA: "Advertencia"
            }.get(region.estado, "?")
            
            print(f"\nREGIÓN {i}: {estado_icono} {region.estado.value.upper()}")
            print(f"   • Ciudades: {len(region.ciudades)}")
            print(f"   • Conexiones internas: {region.conexiones_internas}")
            print(f"   • Población: {region.poblacion_total:,}")
            print(f"   • Capacidad logística: {region.capacidad_total:.1f}")
            
            if region.tiene_infraestructura_critica:
                print(f"   • Tiene infraestructura crítica (puerto/aeropuerto/capital)")
            
            if incluir_detalles:
                print(f"   • Ciudades: {', '.join(region.ciudades)}")
                if region.ciudades_info:
                    print(f"   • Detalles:")
                    for ciudad in region.ciudades[:5]:  # Mostrar primeras 5
                        info = region.ciudades_info.get(ciudad)
                        if info:
                            detalles = []
                            if info.es_capital:
                                detalles.append("Capital")
                            if info.tiene_puerto:
                                detalles.append("Puerto")
                            if info.tiene_aeropuerto:
                                detalles.append("Aeropuerto")
                            print(f"     - {ciudad}: {', '.join(detalles) if detalles else 'Ciudad normal'}")
                    if len(region.ciudades) > 5:
                        print(f"     - ... y {len(region.ciudades) - 5} ciudades más")
        
        # Mostrar análisis general
        analisis = self.analizar_desconexiones()
        
        print(f"\nANÁLISIS DE DESCONEXIÓN:")
        print(f"   • Nivel de afectación: {analisis['nivel_afectacion']}")
        print(f"   • Índice de fragmentación: {analisis['indice_fragmentacion']:.2f}")
        print(f"   • Regiones operativas: {analisis['regiones_operativas']}")
        print(f"   • Regiones aisladas: {analisis['regiones_aisladas']}")
        print(f"   • Regiones críticas: {analisis['regiones_criticas']}")
        print(f"   • Población en regiones afectadas: {analisis['poblacion_total_aislada']:,}")
        
        # Mostrar ciudades críticas
        if analisis['ciudades_criticas']:
            print(f"\nCIUDADES CRÍTICAS (Top 3):")
            for i, ciudad in enumerate(analisis['ciudades_criticas'][:3], 1):
                print(f"   {i}. {ciudad['ciudad']}: {ciudad['conexiones']} conexiones, "
                      f"impacto +{ciudad['impacto']} componentes")
        
        # Mostrar recomendaciones
        recomendaciones = self.recomendar_conexiones(3)
        if recomendaciones and 'mensaje' not in recomendaciones[0]:
            print(f"\nRECOMENDACIONES DE CONEXIÓN:")
            for i, rec in enumerate(recomendaciones, 1):
                print(f"   {i}. Conectar {rec['ciudad1']} ↔ {rec['ciudad2']} "
                      f"(Prioridad: {rec['prioridad']})")
        
        print(f"{'='*80}\n")
    
    def mostrar_simulacion(self, ciudades_afectadas: Set[str]) -> None:
        """
        Muestra una simulación de desconexión
        """
        print(f"\n{'='*80}")
        print(f"SIMULACIÓN DE DESCONEXIÓN")
        print(f"   Ciudades afectadas: {', '.join(ciudades_afectadas)}")
        print(f"{'='*80}")
        
        resultado = self.simular_desconexion(ciudades_afectadas)
        
        print(f"\nRESULTADOS DE LA SIMULACIÓN:")
        print(f"   • Ciudades restantes: {len(resultado['ciudades_restantes'])}")
        print(f"   • Componentes resultantes: {len(resultado['componentes'])}")
        print(f"   • Nivel de afectación: {resultado['analisis']['nivel_afectacion']}")
        print(f"   • Regiones aisladas: {resultado['analisis']['regiones_aisladas']}")
        print(f"   • Población afectada: {resultado['analisis']['poblacion_total_aislada']:,}")
        
        print(f"\nCOMPONENTES RESULTANTES:")
        for i, region in enumerate(resultado['componentes'], 1):
            estado_icono = {
                EstadoRegion.OPERATIVA: "Verde",
                EstadoRegion.PARCIALMENTE_CONECTADA: "Amarilla",
                EstadoRegion.AISLADA: "Rojo",
                EstadoRegion.CRITICA: "Advertencia"
            }.get(region.estado, "?")
            
            print(f"   Región {i}: {estado_icono} {len(region.ciudades)} ciudades - {region.estado.value}")
            print(f"      {', '.join(region.ciudades[:5])}")
            if len(region.ciudades) > 5:
                print(f"      ... y {len(region.ciudades) - 5} más")
        
        print(f"{'='*80}\n")


# ============================================================
# EJEMPLOS PRÁCTICOS
# ============================================================

def crear_red_logistica_ejemplo() -> RedLogisticaDesconectada:
    """Crea una red logística de ejemplo"""
    red = RedLogisticaDesconectada("Red Logística Nacional")
    
    # Agregar ciudades (nombre, población, capacidad_logística, tiene_puerto, tiene_aeropuerto, es_capital)
    ciudades = [
        ("Madrid", 3200000, 5000, False, True, True),
        ("Barcelona", 1600000, 4000, True, True, False),
        ("Valencia", 800000, 3000, True, False, False),
        ("Sevilla", 700000, 2500, False, True, False),
        ("Zaragoza", 700000, 2000, False, False, False),
        ("Málaga", 600000, 1800, True, False, False),
        ("Murcia", 450000, 1500, False, False, False),
        ("Palma", 400000, 1200, True, True, False),
        ("Bilbao", 350000, 1500, True, False, False),
        ("Alicante", 330000, 1200, True, False, False),
        ("Córdoba", 330000, 1000, False, False, False),
        ("Valladolid", 300000, 1000, False, False, False),
        ("Vigo", 300000, 1100, True, False, False),
        ("Gijón", 270000, 900, False, False, False),
        ("Hospitalet", 260000, 800, False, False, False),
        ("La Coruña", 250000, 900, True, False, False),
        ("Granada", 240000, 800, False, False, False),
        ("Sabadell", 210000, 700, False, False, False),
        ("Santander", 180000, 700, True, False, False),
        ("Jerez", 180000, 600, False, False, False),
    ]
    
    for nombre, poblacion, capacidad, puerto, aeropuerto, capital in ciudades:
        red.agregar_ciudad(nombre, poblacion, capacidad, puerto, aeropuerto, capital)
    
    # Agregar carreteras
    carreteras = [
        # Conexiones principales
        ("Madrid", "Barcelona"), ("Madrid", "Valencia"), ("Madrid", "Sevilla"),
        ("Madrid", "Zaragoza"), ("Madrid", "Bilbao"), ("Madrid", "Valladolid"),
        ("Barcelona", "Zaragoza"), ("Barcelona", "Valencia"), ("Barcelona", "Sabadell"),
        ("Valencia", "Alicante"), ("Valencia", "Murcia"),
        ("Sevilla", "Málaga"), ("Sevilla", "Córdoba"), ("Sevilla", "Jerez"),
        ("Zaragoza", "Bilbao"), ("Zaragoza", "Valladolid"),
        ("Málaga", "Granada"), ("Málaga", "Córdoba"),
        ("Bilbao", "Santander"), ("Bilbao", "Valladolid"),
        ("Alicante", "Murcia"), ("Murcia", "Granada"),
        
        # Conexiones periféricas
        ("Vigo", "La Coruña"), ("Vigo", "Gijón"),
        ("La Coruña", "Gijón"), ("Gijón", "Santander"),
        ("Palma", "Barcelona"),  # Conexión marítima
        ("Palma", "Valencia"),    # Conexión marítima
        
        # Conexiones adicionales
        ("Córdoba", "Granada"), ("Córdoba", "Jerez"),
        ("Sabadell", "Hospitalet"), ("Hospitalet", "Barcelona"),
        
        # Aislar algunas ciudades para demostración
        ("Vigo", "La Coruña"), ("Vigo", "Gijón"),
        ("La Coruña", "Gijón"), ("Gijón", "Santander"),
    ]
    
    for c1, c2 in carreteras:
        red.agregar_carretera(c1, c2)
    
    return red


def crear_red_fragmentada() -> RedLogisticaDesconectada:
    """Crea una red con fragmentación natural para demostración"""
    red = RedLogisticaDesconectada("Red Fragmentada")
    
    # Región Norte (conectada internamente)
    ciudades_norte = [
        ("Bilbao", 350000, 1500, True, False, False),
        ("Santander", 180000, 700, True, False, False),
        ("Vigo", 300000, 1100, True, False, False),
        ("La Coruña", 250000, 900, True, False, False),
        ("Gijón", 270000, 900, False, False, False),
    ]
    
    # Región Centro (conectada internamente)
    ciudades_centro = [
        ("Madrid", 3200000, 5000, False, True, True),
        ("Zaragoza", 700000, 2000, False, False, False),
        ("Valladolid", 300000, 1000, False, False, False),
        ("Segovia", 150000, 500, False, False, False),
        ("Toledo", 85000, 400, False, False, False),
    ]
    
    # Región Este (conectada internamente)
    ciudades_este = [
        ("Barcelona", 1600000, 4000, True, True, False),
        ("Valencia", 800000, 3000, True, False, False),
        ("Alicante", 330000, 1200, True, False, False),
        ("Murcia", 450000, 1500, False, False, False),
        ("Palma", 400000, 1200, True, True, False),
    ]
    
    # Región Sur (conectada internamente)
    ciudades_sur = [
        ("Sevilla", 700000, 2500, False, True, False),
        ("Málaga", 600000, 1800, True, False, False),
        ("Córdoba", 330000, 1000, False, False, False),
        ("Granada", 240000, 800, False, False, False),
        ("Jerez", 180000, 600, False, False, False),
    ]
    
    # Agregar todas las ciudades
    for ciudad, poblacion, capacidad, puerto, aeropuerto, capital in (
        ciudades_norte + ciudades_centro + ciudades_este + ciudades_sur
    ):
        red.agregar_ciudad(ciudad, poblacion, capacidad, puerto, aeropuerto, capital)
    
    # Conexiones dentro de cada región
    conexiones_regionales = [
        # Norte
        ("Bilbao", "Santander"), ("Bilbao", "Vigo"),
        ("Santander", "Gijón"), ("Gijón", "Vigo"),
        ("Vigo", "La Coruña"), ("La Coruña", "Gijón"),
        
        # Centro
        ("Madrid", "Zaragoza"), ("Madrid", "Valladolid"),
        ("Madrid", "Segovia"), ("Madrid", "Toledo"),
        ("Zaragoza", "Valladolid"), ("Segovia", "Toledo"),
        
        # Este
        ("Barcelona", "Valencia"), ("Barcelona", "Palma"),
        ("Valencia", "Alicante"), ("Valencia", "Murcia"),
        ("Alicante", "Murcia"), ("Palma", "Valencia"),
        
        # Sur
        ("Sevilla", "Málaga"), ("Sevilla", "Córdoba"),
        ("Sevilla", "Jerez"), ("Málaga", "Granada"),
        ("Córdoba", "Granada"), ("Córdoba", "Jerez"),
    ]
    
    for c1, c2 in conexiones_regionales:
        red.agregar_carretera(c1, c2)
    
    # Algunas conexiones entre regiones (limitadas)
    conexiones_interregionales = [
        ("Madrid", "Barcelona"),  # Centro-Este
        ("Madrid", "Sevilla"),    # Centro-Sur
        ("Madrid", "Bilbao"),     # Centro-Norte
        ("Zaragoza", "Barcelona"), # Centro-Este adicional
    ]
    
    for c1, c2 in conexiones_interregionales:
        red.agregar_carretera(c1, c2)
    
    return red


def demostracion_completa():
    """Demostración completa de todas las funcionalidades"""
    
    print("="*80)
    print("ANÁLISIS DE DESCONEXIÓN DE RED LOGÍSTICA")
    print("="*80)
    
    # ============================================
    # EJEMPLO 1: Red completa
    # ============================================
    print("\n" + "="*80)
    print("EJEMPLO 1: RED LOGÍSTICA COMPLETA")
    print("="*80)
    
    red = crear_red_logistica_ejemplo()
    red.mostrar_componentes(incluir_detalles=True)
    
    # ============================================
    # EJEMPLO 2: Red fragmentada
    # ============================================
    print("\n" + "="*80)
    print("EJEMPLO 2: RED FRAGMENTADA")
    print("="*80)
    
    red_fragmentada = crear_red_fragmentada()
    red_fragmentada.mostrar_componentes(incluir_detalles=False)
    
    # ============================================
    # EJEMPLO 3: Simulación de desconexión
    # ============================================
    print("\n" + "="*80)
    print("EJEMPLO 3: SIMULACIÓN DE DESCONEXIÓN")
    print("="*80)
    
    red.mostrar_simulacion({"Madrid", "Barcelona"})
    
    # ============================================
    # EJEMPLO 4: Análisis detallado
    # ============================================
    print("\n" + "="*80)
    print("EJEMPLO 4: ANÁLISIS DETALLADO")
    print("="*80)
    
    analisis = red.analizar_desconexiones()
    
    print("ANÁLISIS DE DESCONEXIONES:")
    print(f"   • Total regiones: {analisis['total_regiones']}")
    print(f"   • Índice de fragmentación: {analisis['indice_fragmentacion']:.2f}")
    print(f"   • Regiones operativas: {analisis['regiones_operativas']}")
    print(f"   • Regiones aisladas: {analisis['regiones_aisladas']}")
    print(f"   • Regiones críticas: {analisis['regiones_criticas']}")
    print(f"   • Nivel de afectación: {analisis['nivel_afectacion']}")
    
    if analisis['ciudades_criticas']:
        print(f"\nCiudades críticas:")
        for ciudad in analisis['ciudades_criticas']:
            print(f"      • {ciudad['ciudad']}: {ciudad['conexiones']} conexiones")
    
    # ============================================
    # EJEMPLO 5: Recomendaciones de conexión
    # ============================================
    print("\n" + "="*80)
    print("EJEMPLO 5: RECOMENDACIONES DE CONEXIÓN")
    print("="*80)
    
    recomendaciones = red_fragmentada.recomendar_conexiones(3)
    print("Conexiones recomendadas:")
    for i, rec in enumerate(recomendaciones, 1):
        if 'mensaje' in rec:
            print(f"   • {rec['mensaje']}")
        else:
            print(f"   {i}. {rec['ciudad1']} ↔ {rec['ciudad2']} (Prioridad: {rec['prioridad']})")
    
    # ============================================
    # EJEMPLO 6: Comparación antes/después
    # ============================================
    print("\n" + "="*80)
    print("EJEMPLO 6: COMPARACIÓN ANTES/DESPUÉS DE DESCONEXIÓN")
    print("="*80)
    
    print("Estado inicial:")
    componentes_iniciales = red_fragmentada.encontrar_componentes_conexas()
    print(f"   • Componentes: {len(componentes_iniciales)}")
    print(f"   • Ciudades: {red_fragmentada.total_ciudades}")
    
    # Simular desconexión de ciudades clave
    ciudades_afectadas = {"Madrid", "Zaragoza", "Valladolid"}
    print(f"\nDesconectando: {', '.join(ciudades_afectadas)}")
    
    resultado = red_fragmentada.simular_desconexion(ciudades_afectadas)
    print(f"\nEstado después de la desconexión:")
    print(f"   • Componentes: {len(resultado['componentes'])}")
    print(f"   • Ciudades restantes: {len(resultado['ciudades_restantes'])}")
    print(f"   • Nivel de afectación: {resultado['analisis']['nivel_afectacion']}")
    print(f"   • Regiones aisladas: {resultado['analisis']['regiones_aisladas']}")


# ============================================================
# FUNCIONES ADICIONALES ÚTILES
# ============================================================

def exportar_componentes(componentes: List[RegionLogistica], archivo: str) -> None:
    """
    Exporta las componentes conexas a un archivo CSV
    
    Args:
        componentes: Lista de regiones logísticas
        archivo: Nombre del archivo de salida
    """
    import csv
    
    with open(archivo, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Region', 'Ciudad', 'Poblacion', 'Capacidad', 'TienePuerto', 'TieneAeropuerto', 'EsCapital'])
        
        for region in componentes:
            for ciudad in region.ciudades:
                info = region.ciudades_info.get(ciudad, {})
                writer.writerow([
                    region.id,
                    ciudad,
                    info.poblacion if hasattr(info, 'poblacion') else 0,
                    info.capacidad_logistica if hasattr(info, 'capacidad_logistica') else 0,
                    info.tiene_puerto if hasattr(info, 'tiene_puerto') else False,
                    info.tiene_aeropuerto if hasattr(info, 'tiene_aeropuerto') else False,
                    info.es_capital if hasattr(info, 'es_capital') else False
                ])


def generar_reporte_desconexion(red: RedLogisticaDesconectada) -> str:
    """
    Genera un reporte en texto del análisis de desconexión
    
    Args:
        red: Red logística a analizar
        
    Returns:
        String con el reporte
    """
    componentes = red.encontrar_componentes_conexas()
    analisis = red.analizar_desconexiones()
    
    reporte = []
    reporte.append("=" * 60)
    reporte.append(f"REPORTE DE DESCONEXIÓN - {red.nombre}")
    reporte.append("=" * 60)
    reporte.append("")
    reporte.append(f"ESTADÍSTICAS GENERALES:")
    reporte.append(f"   • Ciudades totales: {red.total_ciudades}")
    reporte.append(f"   • Carreteras totales: {red.total_carreteras}")
    reporte.append(f"   • Regiones identificadas: {len(componentes)}")
    reporte.append(f"   • Nivel de afectación: {analisis['nivel_afectacion']}")
    reporte.append("")
    reporte.append(f"DISTRIBUCIÓN DE REGIONES:")
    reporte.append(f"   • Operativas: {analisis['regiones_operativas']}")
    reporte.append(f"   • Aisladas: {analisis['regiones_aisladas']}")
    reporte.append(f"   • Críticas: {analisis['regiones_criticas']}")
    reporte.append("")
    
    for i, region in enumerate(componentes, 1):
        reporte.append(f"REGIÓN {i}:")
        reporte.append(f"   • Tamaño: {region.tamaño} ciudades")
        reporte.append(f"   • Estado: {region.estado.value}")
        reporte.append(f"   • Población: {region.poblacion_total:,}")
        reporte.append(f"   • Capacidad: {region.capacidad_total:.1f}")
        reporte.append(f"   • Conexiones internas: {region.conexiones_internas}")
        reporte.append(f"   • Ciudades: {', '.join(region.ciudades)}")
        reporte.append("")
    
    if analisis['ciudades_criticas']:
        reporte.append("CIUDADES CRÍTICAS:")
        for ciudad in analisis['ciudades_criticas']:
            reporte.append(f"   • {ciudad['ciudad']}: {ciudad['conexiones']} conexiones")
        reporte.append("")
    
    recomendaciones = red.recomendar_conexiones(3)
    if recomendaciones and 'mensaje' not in recomendaciones[0]:
        reporte.append("RECOMENDACIONES:")
        for rec in recomendaciones:
            reporte.append(f"   • Conectar {rec['ciudad1']} ↔ {rec['ciudad2']} (Prioridad: {rec['prioridad']})")
    
    reporte.append("")
    reporte.append("=" * 60)
    
    return "\n".join(reporte)


if __name__ == "__main__":
    demostracion_completa()
    
    # Ejemplo de reporte
    print("\n" + "="*80)
    print("GENERACIÓN DE REPORTE")
    print("="*80)
    
    red_reporte = crear_red_fragmentada()
    reporte = generar_reporte_desconexion(red_reporte)
    print(reporte)
