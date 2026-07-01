"""Ejercicio 20: Trazabilidad de Materia Prima

En una planta química, los materiales se transforman secuencialmente. Si ocurre una contaminación
en un reactor base se requiere listar todos los tanques y subproductos que podrían verse afectados
aguas abajo. Implementa un método que reciba un grafo dirigido de transformación y un nodo origen, y
devuelva mediante DFS iterativo el conjunto de todos los nodos alcanzables. """

from typing import Dict, List, Set, Tuple, Optional, Any
from collections import deque, defaultdict
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

class TipoReactor(Enum):
    """Tipos de reactores en la planta química"""
    REACTOR_BASE = "reactor_base"
    REACTOR_INTERMEDIO = "reactor_intermedio"
    REACTOR_FINAL = "reactor_final"
    TANQUE_ALMACENAMIENTO = "tanque_almacenamiento"
    MEZCLADOR = "mezclador"
    SEPARADOR = "separador"
    DESTILADOR = "destilador"
    ENFRIADOR = "enfriador"
    CALENTADOR = "calentador"

class EstadoContaminacion(Enum):
    """Estado de contaminación de un nodo"""
    LIMPIO = "limpio"
    CONTAMINADO = "contaminado"
    EN_TRANSITO = "en_transito"
    BLOQUEADO = "bloqueado"
    AISLADO = "aislado"

class TipoMaterial(Enum):
    """Tipos de materiales en el proceso"""
    MATERIA_PRIMA = "materia_prima"
    INTERMEDIO = "intermedio"
    PRODUCTO_FINAL = "producto_final"
    SUBPRODUCTO = "subproducto"
    RESIDUO = "residuo"
    CATALIZADOR = "catalizador"

@dataclass
class NodoTransformacion:
    """Representa un nodo en el proceso de transformación"""
    nombre: str
    tipo: TipoReactor
    materiales: List[TipoMaterial]
    capacidad: float = 0.0
    temperatura_operacion: float = 0.0
    presion_operacion: float = 0.0
    eficiencia: float = 1.0
    tiempo_procesamiento: int = 0  # minutos

@dataclass
class ArcoTransformacion:
    """Representa una transformación entre nodos"""
    origen: str
    destino: str
    material_transformado: TipoMaterial
    factor_conversion: float = 1.0
    perdidas: float = 0.0
    requiere_validacion: bool = False

@dataclass
class NodoContaminado:
    """Nodo afectado por la contaminación"""
    nombre: str
    tipo: str
    nivel_contaminacion: float
    profundidad: int
    camino: List[str]
    materiales_afectados: List[str]
    estado: EstadoContaminacion

class TrazabilidadMateriaPrima:
    """
    Sistema de trazabilidad de materia prima en planta química.
    
    Características:
    - DFS iterativo para encontrar nodos alcanzables
    - Seguimiento de niveles de contaminación
    - Identificación de materiales afectados
    - Análisis de impacto en la producción
    - Recomendaciones de contención
    - Simulación de propagación
    """
    
    def __init__(self, nombre_planta: str = "Planta Química"):
        """
        Inicializa la planta química
        
        Args:
            nombre_planta: Nombre identificativo de la planta
        """
        self.nombre_planta = nombre_planta
        self.grafo: Dict[str, Set[str]] = defaultdict(set)  # Adyacencia dirigida
        self.nodos_info: Dict[str, NodoTransformacion] = {}
        self.arco_info: Dict[Tuple[str, str], ArcoTransformacion] = {}
        self.total_nodos = 0
        self.total_transformaciones = 0
        
        # Niveles de contaminación por nodo
        self.nivel_contaminacion: Dict[str, float] = defaultdict(float)
        
        # Materiales por nodo
        self.materiales_por_nodo: Dict[str, Set[TipoMaterial]] = defaultdict(set)
        
        # Cache de trazabilidad
        self.cache_trazabilidad: Dict[str, List[NodoContaminado]] = {}
    
    def agregar_nodo(self, nombre: str, tipo: TipoReactor,
                     materiales: List[TipoMaterial] = None,
                     capacidad: float = 0.0,
                     temperatura: float = 0.0,
                     presion: float = 0.0,
                     eficiencia: float = 1.0,
                     tiempo: int = 0) -> None:
        """
        Agrega un nodo de transformación a la planta
        
        Args:
            nombre: Identificador del nodo
            tipo: Tipo de reactor
            materiales: Materiales presentes en el nodo
            capacidad: Capacidad de procesamiento
            temperatura: Temperatura de operación
            presion: Presión de operación
            eficiencia: Eficiencia del proceso
            tiempo: Tiempo de procesamiento
        """
        if nombre in self.nodos_info:
            raise ValueError(f"El nodo '{nombre}' ya existe en la planta")
        
        if materiales is None:
            materiales = [TipoMaterial.INTERMEDIO]
        
        self.nodos_info[nombre] = NodoTransformacion(
            nombre=nombre,
            tipo=tipo,
            materiales=materiales,
            capacidad=capacidad,
            temperatura_operacion=temperatura,
            presion_operacion=presion,
            eficiencia=eficiencia,
            tiempo_procesamiento=tiempo
        )
        
        for material in materiales:
            self.materiales_por_nodo[nombre].add(material)
        
        self.total_nodos += 1
    
    def agregar_transformacion(self, origen: str, destino: str,
                              material_transformado: TipoMaterial = None,
                              factor_conversion: float = 1.0,
                              perdidas: float = 0.0,
                              requiere_validacion: bool = False) -> None:
        """
        Agrega una transformación dirigida entre dos nodos
        
        Args:
            origen: Nodo de origen
            destino: Nodo de destino
            material_transformado: Material que se transforma
            factor_conversion: Factor de conversión (0-1)
            perdidas: Porcentaje de pérdidas (0-1)
            requiere_validacion: Si requiere validación de calidad
        """
        if origen not in self.nodos_info:
            raise ValueError(f"El nodo origen '{origen}' no existe")
        if destino not in self.nodos_info:
            raise ValueError(f"El nodo destino '{destino}' no existe")
        if origen == destino:
            raise ValueError("No se puede transformar un nodo en sí mismo")
        
        if material_transformado is None:
            material_transformado = TipoMaterial.INTERMEDIO
        
        # Agregar arco dirigido
        self.grafo[origen].add(destino)
        
        # Guardar información del arco
        self.arco_info[(origen, destino)] = ArcoTransformacion(
            origen=origen,
            destino=destino,
            material_transformado=material_transformado,
            factor_conversion=factor_conversion,
            perdidas=perdidas,
            requiere_validacion=requiere_validacion
        )
        
        self.total_transformaciones += 1
        
        # El destino hereda los materiales del origen (con factor de conversión)
        if factor_conversion > 0:
            for material in self.materiales_por_nodo[origen]:
                if material != TipoMaterial.RESIDUO:
                    self.materiales_por_nodo[destino].add(material)
    
    def dfs_iterativo(self, nodo_origen: str, 
                     max_profundidad: Optional[int] = None,
                     incluir_detalles: bool = True) -> List[NodoContaminado]:
        """
        Realiza DFS iterativo desde el nodo origen para encontrar todos los nodos alcanzables
        
        Args:
            nodo_origen: Nodo donde inicia la contaminación
            max_profundidad: Profundidad máxima a explorar (opcional)
            incluir_detalles: Si incluye información detallada
            
        Returns:
            Lista de NodoContaminado con todos los nodos alcanzables
        """
        if nodo_origen not in self.nodos_info:
            raise ValueError(f"El nodo '{nodo_origen}' no existe en la planta")
        
        # Verificar cache
        cache_key = f"{nodo_origen}_{max_profundidad if max_profundidad else 'inf'}"
        if cache_key in self.cache_trazabilidad:
            return self.cache_trazabilidad[cache_key]
        
        # DFS iterativo con pila
        pila: deque = deque()
        pila.append((nodo_origen, 0, [nodo_origen]))  # (nodo, profundidad, camino)
        
        visitados: Set[str] = set()
        nodos_contaminados: List[NodoContaminado] = []
        
        # Para rastrear padres
        padres: Dict[str, str] = {}
        
        while pila:
            nodo_actual, profundidad, camino = pila.pop()
            
            # Verificar límite de profundidad
            if max_profundidad is not None and profundidad > max_profundidad:
                continue
            
            if nodo_actual in visitados:
                continue
            
            visitados.add(nodo_actual)
            
            # Calcular nivel de contaminación (decrece con la profundidad)
            nivel_contaminacion = 100.0 * (0.7 ** profundidad)  # 70% por nivel
            
            # Determinar materiales afectados
            materiales_afectados = [m.value for m in self.materiales_por_nodo.get(nodo_actual, [])]
            
            # Crear nodo contaminado
            nodo_info = self.nodos_info.get(nodo_actual)
            nodo_contaminado = NodoContaminado(
                nombre=nodo_actual,
                tipo=nodo_info.tipo.value if nodo_info else "desconocido",
                nivel_contaminacion=nivel_contaminacion,
                profundidad=profundidad,
                camino=camino.copy(),
                materiales_afectados=materiales_afectados,
                estado=EstadoContaminacion.CONTAMINADO
            )
            nodos_contaminados.append(nodo_contaminado)
            
            # Actualizar nivel de contaminación global
            self.nivel_contaminacion[nodo_actual] = max(
                self.nivel_contaminacion[nodo_actual],
                nivel_contaminacion
            )
            
            # Explorar nodos siguientes (aguas abajo)
            for vecino in self.grafo.get(nodo_actual, set()):
                if vecino not in visitados:
                    padres[vecino] = nodo_actual
                    nuevo_camino = camino + [vecino]
                    pila.append((vecino, profundidad + 1, nuevo_camino))
        
        # Guardar en cache
        self.cache_trazabilidad[cache_key] = nodos_contaminados
        
        return nodos_contaminados
    
    def dfs_recursivo(self, nodo_origen: str,
                     max_profundidad: Optional[int] = None,
                     profundidad_actual: int = 0,
                     camino: Optional[List[str]] = None,
                     visitados: Optional[Set[str]] = None) -> List[NodoContaminado]:
        """
        Versión recursiva de DFS (alternativa al iterativo)
        
        Args:
            nodo_origen: Nodo donde inicia la contaminación
            max_profundidad: Profundidad máxima a explorar
            profundidad_actual: Profundidad actual (uso interno)
            camino: Camino actual (uso interno)
            visitados: Nodos visitados (uso interno)
            
        Returns:
            Lista de NodoContaminado
        """
        if nodo_origen not in self.nodos_info:
            raise ValueError(f"El nodo '{nodo_origen}' no existe")
        
        if camino is None:
            camino = [nodo_origen]
        
        if visitados is None:
            visitados = set()
        
        # Verificar límite de profundidad
        if max_profundidad is not None and profundidad_actual > max_profundidad:
            return []
        
        if nodo_origen in visitados:
            return []
        
        visitados.add(nodo_origen)
        
        # Crear nodo contaminado
        nivel_contaminacion = 100.0 * (0.7 ** profundidad_actual)
        nodo_info = self.nodos_info.get(nodo_origen)
        materiales_afectados = [m.value for m in self.materiales_por_nodo.get(nodo_origen, [])]
        
        resultado = [
            NodoContaminado(
                nombre=nodo_origen,
                tipo=nodo_info.tipo.value if nodo_info else "desconocido",
                nivel_contaminacion=nivel_contaminacion,
                profundidad=profundidad_actual,
                camino=camino.copy(),
                materiales_afectados=materiales_afectados,
                estado=EstadoContaminacion.CONTAMINADO
            )
        ]
        
        # Actualizar nivel de contaminación global
        self.nivel_contaminacion[nodo_origen] = max(
            self.nivel_contaminacion[nodo_origen],
            nivel_contaminacion
        )
        
        # Explorar nodos siguientes
        for vecino in self.grafo.get(nodo_origen, set()):
            if vecino not in visitados:
                nuevo_camino = camino + [vecino]
                resultado.extend(
                    self.dfs_recursivo(
                        vecino,
                        max_profundidad,
                        profundidad_actual + 1,
                        nuevo_camino,
                        visitados
                    )
                )
        
        return resultado
    
    def analizar_impacto(self, nodo_origen: str,
                        max_profundidad: Optional[int] = None) -> Dict[str, Any]:
        """
        Analiza el impacto de la contaminación en el nodo origen
        
        Args:
            nodo_origen: Nodo donde inicia la contaminación
            max_profundidad: Profundidad máxima a analizar
            
        Returns:
            Dict con análisis detallado
        """
        nodos_afectados = self.dfs_iterativo(nodo_origen, max_profundidad)
        
        # Estadísticas por tipo de reactor
        tipos_afectados = defaultdict(int)
        materiales_afectados_total = set()
        
        for nodo in nodos_afectados:
            tipos_afectados[nodo.tipo] += 1
            for material in nodo.materiales_afectados:
                materiales_afectados_total.add(material)
        
        # Niveles de contaminación
        niveles = [n.nivel_contaminacion for n in nodos_afectados]
        nivel_promedio = sum(niveles) / len(niveles) if niveles else 0
        nivel_maximo = max(niveles) if niveles else 0
        nivel_minimo = min(niveles) if niveles else 0
        
        # Profundidades
        profundidades = [n.profundidad for n in nodos_afectados]
        prof_max = max(profundidades) if profundidades else 0
        
        # Identificar nodos críticos (alta contaminación y profundidad temprana)
        nodos_criticos = sorted(
            nodos_afectados,
            key=lambda n: (n.nivel_contaminacion, -n.profundidad),
            reverse=True
        )[:5]
        
        # Identificar rutas de contaminación
        rutas = []
        for nodo in nodos_afectados:
            if nodo.profundidad > 0:
                rutas.append({
                    'destino': nodo.nombre,
                    'camino': ' → '.join(nodo.camino),
                    'nivel': nodo.nivel_contaminacion
                })
        
        return {
            'nodo_origen': nodo_origen,
            'total_afectados': len(nodos_afectados),
            'profundidad_maxima': prof_max,
            'nivel_promedio': nivel_promedio,
            'nivel_maximo': nivel_maximo,
            'nivel_minimo': nivel_minimo,
            'tipos_afectados': dict(tipos_afectados),
            'materiales_afectados': list(materiales_afectados_total),
            'nodos_criticos': [
                {
                    'nombre': n.nombre,
                    'tipo': n.tipo,
                    'nivel': n.nivel_contaminacion,
                    'profundidad': n.profundidad
                }
                for n in nodos_criticos
            ],
            'rutas_criticas': rutas[:5],  # Top 5 rutas
            'nodos_detalle': nodos_afectados
        }
    
    def recomendar_contencion(self, nodo_origen: str) -> List[Dict[str, Any]]:
        """
        Recomienda acciones de contención para detener la contaminación
        
        Args:
            nodo_origen: Nodo donde inicia la contaminación
            
        Returns:
            Lista de recomendaciones
        """
        nodos_afectados = self.dfs_iterativo(nodo_origen)
        
        if not nodos_afectados:
            return [{'mensaje': 'No se detectó propagación de contaminación'}]
        
        recomendaciones = []
        
        # 1. Identificar puntos de corte (nodos con alta conectividad)
        nodos_con_conexiones = {}
        for nodo in nodos_afectados:
            if nodo.profundidad > 0:  # No incluir el origen
                # Contar conexiones salientes
                conexiones = len(self.grafo.get(nodo.nombre, set()))
                if conexiones > 0:
                    nodos_con_conexiones[nodo.nombre] = conexiones
        
        # Ordenar por número de conexiones
        puntos_corte = sorted(
            nodos_con_conexiones.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]
        
        for nodo, conexiones in puntos_corte:
            recomendaciones.append({
                'accion': 'Aislar nodo',
                'nodo': nodo,
                'prioridad': 'ALTA' if conexiones >= 2 else 'MEDIA',
                'motivo': f'Nodo con {conexiones} conexiones salientes - punto crítico de propagación',
                'impacto': 'Detendría la propagación a través de este punto'
            })
        
        # 2. Recomendar verificación de materiales críticos
        materiales_criticos = set()
        for nodo in nodos_afectados[:10]:  # Primeros 10 nodos
            for material in nodo.materiales_afectados:
                if material in ['materia_prima', 'producto_final']:
                    materiales_criticos.add(material)
        
        if materiales_criticos:
            recomendaciones.append({
                'accion': 'Verificar calidad',
                'nodo': 'Todos los afectados',
                'prioridad': 'CRÍTICA',
                'motivo': f'Materiales críticos afectados: {", ".join(materiales_criticos)}',
                'impacto': 'Requiere validación de calidad antes de continuar'
            })
        
        # 3. Recomendar limpieza de nodos con alta contaminación
        nodos_alta_contaminacion = [
            n for n in nodos_afectados 
            if n.nivel_contaminacion > 50 and n.profundidad > 0
        ][:3]
        
        for nodo in nodos_alta_contaminacion:
            recomendaciones.append({
                'accion': 'Limpieza urgente',
                'nodo': nodo.nombre,
                'prioridad': 'ALTA',
                'motivo': f'Nivel de contaminación: {nodo.nivel_contaminacion:.1f}%',
                'impacto': 'Evita contaminación cruzada en productos'
            })
        
        return recomendaciones
    
    def simular_propagacion(self, nodo_origen: str, 
                           nivel_inicial: float = 100.0,
                           factor_decremento: float = 0.7) -> Dict[str, Any]:
        """
        Simula la propagación de contaminación con parámetros personalizados
        
        Args:
            nodo_origen: Nodo donde inicia la contaminación
            nivel_inicial: Nivel inicial de contaminación
            factor_decremento: Factor de decremento por nivel
            
        Returns:
            Dict con resultados de la simulación
        """
        if nodo_origen not in self.nodos_info:
            raise ValueError(f"El nodo '{nodo_origen}' no existe")
        
        # Ejecutar DFS con parámetros personalizados
        # Modificamos temporalmente el cálculo de niveles
        def dfs_con_niveles_personalizados():
            pila = deque([(nodo_origen, 0, [nodo_origen])])
            visitados = set()
            resultados = []
            
            while pila:
                nodo, profundidad, camino = pila.pop()
                
                if nodo in visitados:
                    continue
                
                visitados.add(nodo)
                
                nivel = nivel_inicial * (factor_decremento ** profundidad)
                
                nodo_info = self.nodos_info.get(nodo)
                resultados.append({
                    'nodo': nodo,
                    'tipo': nodo_info.tipo.value if nodo_info else 'desconocido',
                    'nivel_contaminacion': nivel,
                    'profundidad': profundidad,
                    'camino': camino.copy(),
                    'materiales': [m.value for m in self.materiales_por_nodo.get(nodo, [])]
                })
                
                for vecino in self.grafo.get(nodo, set()):
                    if vecino not in visitados:
                        nuevo_camino = camino + [vecino]
                        pila.append((vecino, profundidad + 1, nuevo_camino))
            
            return resultados
        
        resultados = dfs_con_niveles_personalizados()
        
        # Calcular estadísticas
        if resultados:
            niveles = [r['nivel_contaminacion'] for r in resultados]
            
            return {
                'nodo_origen': nodo_origen,
                'nivel_inicial': nivel_inicial,
                'factor_decremento': factor_decremento,
                'total_afectados': len(resultados),
                'profundidad_maxima': max(r['profundidad'] for r in resultados),
                'nivel_promedio': sum(niveles) / len(niveles),
                'nivel_maximo': max(niveles),
                'nivel_minimo': min(niveles),
                'resultados': resultados
            }
        
        return {
            'nodo_origen': nodo_origen,
            'total_afectados': 0,
            'mensaje': 'No se encontraron nodos afectados'
        }
    
    def mostrar_trazabilidad(self, nodo_origen: str,
                            max_profundidad: Optional[int] = None) -> None:
        """
        Muestra de forma formateada la trazabilidad desde el nodo origen
        
        Args:
            nodo_origen: Nodo donde inicia la contaminación
            max_profundidad: Profundidad máxima a mostrar
        """
        print(f"\n{'='*80}")
        print(f"TRAZABILIDAD DE MATERIA PRIMA")
        print(f"   Planta: {self.nombre_planta}")
        print(f"   Nodo origen: {nodo_origen}")
        if max_profundidad:
            print(f"   Profundidad máxima: {max_profundidad}")
        print(f"{'='*80}")
        
        try:
            nodos_afectados = self.dfs_iterativo(nodo_origen, max_profundidad)
        except ValueError as e:
            print(f"Error: {e}")
            return
        
        if not nodos_afectados:
            print(f"\nNo se detectaron nodos afectados aguas abajo")
            return
        
        print(f"\nRESULTADOS:")
        print(f"   • Total de nodos afectados: {len(nodos_afectados)}")
        print(f"   • Profundidad máxima: {max(n.profundidad for n in nodos_afectados)}")
        
        # Mostrar nodos por profundidad
        print(f"\nNODOS POR PROFUNDIDAD:")
        nodos_por_profundidad = defaultdict(list)
        for nodo in nodos_afectados:
            nodos_por_profundidad[nodo.profundidad].append(nodo)
        
        for profundidad in sorted(nodos_por_profundidad.keys()):
            nodos = nodos_por_profundidad[profundidad]
            icono = "VERDE" if profundidad == 0 else "AMARILLO" if profundidad < 3 else "ROJO"
            print(f"\n  Profundidad {profundidad} ({icono}):")
            for nodo in nodos:
                nivel_str = f"{nodo.nivel_contaminacion:.1f}%"
                materiales_str = ", ".join(nodo.materiales_afectados[:3])
                if len(nodo.materiales_afectados) > 3:
                    materiales_str += f" +{len(nodo.materiales_afectados)-3}"
                
                print(f"    • {nodo.nombre} ({nodo.tipo}) - Nivel: {nivel_str}")
                print(f"      Materiales: {materiales_str}")
                print(f"      Camino: {' → '.join(nodo.camino)}")
        
        # Mostrar análisis de impacto
        print(f"\nANÁLISIS DE IMPACTO:")
        analisis = self.analizar_impacto(nodo_origen, max_profundidad)
        
        print(f"   • Nivel promedio de contaminación: {analisis['nivel_promedio']:.1f}%")
        print(f"   • Nivel máximo: {analisis['nivel_maximo']:.1f}%")
        print(f"   • Nivel mínimo: {analisis['nivel_minimo']:.1f}%")
        
        print(f"\n   Tipos de reactores afectados:")
        for tipo, cantidad in analisis['tipos_afectados'].items():
            print(f"      • {tipo}: {cantidad}")
        
        print(f"\n   Materiales afectados:")
        for material in analisis['materiales_afectados'][:5]:
            print(f"      • {material}")
        if len(analisis['materiales_afectados']) > 5:
            print(f"      ... y {len(analisis['materiales_afectados'])-5} más")
        
        # Mostrar nodos críticos
        if analisis['nodos_criticos']:
            print(f"\nNODOS CRÍTICOS (mayor contaminación):")
            for i, nodo in enumerate(analisis['nodos_criticos'][:3], 1):
                print(f"   {i}. {nodo['nombre']}: {nodo['nivel']:.1f}% (profundidad {nodo['profundidad']})")
        
        # Mostrar recomendaciones
        print(f"\nRECOMENDACIONES DE CONTENCIÓN:")
        recomendaciones = self.recomendar_contencion(nodo_origen)
        
        if recomendaciones and 'mensaje' not in recomendaciones[0]:
            for i, rec in enumerate(recomendaciones[:4], 1):
                prioridad_icono = {
                    'CRÍTICA': 'ALERTA',
                    'ALTA': 'ADVERTENCIA',
                    'MEDIA': 'PRECAUCIÓN'
                }.get(rec['prioridad'], 'ALTA')
                
                print(f"   {prioridad_icono} {i}. {rec['accion']} en {rec['nodo']} ({rec['prioridad']})")
                print(f"      {rec['motivo']}")
        else:
            print("   No se requieren acciones inmediatas de contención")
        
        print(f"{'='*80}\n")
    
    def mostrar_simulacion(self, nodo_origen: str,
                          nivel_inicial: float = 100.0,
                          factor_decremento: float = 0.7) -> None:
        """
        Muestra una simulación de contaminación con parámetros personalizados
        """
        print(f"\n{'='*80}")
        print(f"SIMULACIÓN DE CONTAMINACIÓN")
        print(f"   Nodo origen: {nodo_origen}")
        print(f"   Nivel inicial: {nivel_inicial}%")
        print(f"   Factor de decremento: {factor_decremento}")
        print(f"{'='*80}")
        
        simulacion = self.simular_propagacion(nodo_origen, nivel_inicial, factor_decremento)
        
        if simulacion['total_afectados'] == 0:
            print(f"\nNo se detectó propagación de contaminación")
            return
        
        print(f"\nRESULTADOS DE LA SIMULACIÓN:")
        print(f"   • Total de nodos afectados: {simulacion['total_afectados']}")
        print(f"   • Profundidad máxima: {simulacion['profundidad_maxima']}")
        print(f"   • Nivel promedio: {simulacion['nivel_promedio']:.1f}%")
        print(f"   • Nivel máximo: {simulacion['nivel_maximo']:.1f}%")
        print(f"   • Nivel mínimo: {simulacion['nivel_minimo']:.1f}%")
        
        print(f"\nPROPAGACIÓN DETALLADA:")
        for resultado in simulacion['resultados'][:10]:
            barra = self._crear_barra_contaminacion(resultado['nivel_contaminacion'])
            materiales = ", ".join(resultado['materiales'][:2])
            if len(resultado['materiales']) > 2:
                materiales += f" +{len(resultado['materiales'])-2}"
            
            print(f"   • {resultado['nodo']:15s} | P{resultado['profundidad']:2d} | "
                  f"{resultado['nivel_contaminacion']:5.1f}% {barra} | {materiales}")
        
        if len(simulacion['resultados']) > 10:
            print(f"   ... y {len(simulacion['resultados'])-10} nodos más")
        
        print(f"{'='*80}\n")
    
    def _crear_barra_contaminacion(self, nivel: float, longitud: int = 20) -> str:
        """Crea una barra visual del nivel de contaminación"""
        if nivel >= 70:
            color = "ROJO"
        elif nivel >= 40:
            color = "AMARILLO"
        else:
            color = "VERDE"
        
        num_caracteres = int(nivel / 100 * longitud)
        barra = '█' * num_caracteres + '░' * (longitud - num_caracteres)
        return f"{color} [{barra}]"


# ============================================================
# EJEMPLOS PRÁCTICOS
# ============================================================

def crear_planta_quimica_ejemplo() -> TrazabilidadMateriaPrima:
    """Crea una planta química de ejemplo para demostración"""
    planta = TrazabilidadMateriaPrima("Planta Petroquímica")
    
    # Agregar nodos (reactores y tanques)
    nodos = [
        # Reactores base
        ("R1", TipoReactor.REACTOR_BASE, [TipoMaterial.MATERIA_PRIMA], 1000, 150, 10, 0.95, 60),
        ("R2", TipoReactor.REACTOR_BASE, [TipoMaterial.MATERIA_PRIMA], 800, 120, 8, 0.90, 45),
        
        # Reactores intermedios
        ("R3", TipoReactor.REACTOR_INTERMEDIO, [TipoMaterial.INTERMEDIO], 600, 200, 15, 0.92, 30),
        ("R4", TipoReactor.REACTOR_INTERMEDIO, [TipoMaterial.INTERMEDIO], 500, 180, 12, 0.88, 25),
        ("R5", TipoReactor.REACTOR_INTERMEDIO, [TipoMaterial.INTERMEDIO], 400, 160, 10, 0.85, 20),
        
        # Reactores finales
        ("R6", TipoReactor.REACTOR_FINAL, [TipoMaterial.PRODUCTO_FINAL], 300, 100, 5, 0.98, 15),
        ("R7", TipoReactor.REACTOR_FINAL, [TipoMaterial.PRODUCTO_FINAL], 250, 90, 4, 0.97, 10),
        
        # Tanques de almacenamiento
        ("T1", TipoReactor.TANQUE_ALMACENAMIENTO, [TipoMaterial.INTERMEDIO], 2000, 25, 1, 1.0, 0),
        ("T2", TipoReactor.TANQUE_ALMACENAMIENTO, [TipoMaterial.INTERMEDIO], 1500, 25, 1, 1.0, 0),
        ("T3", TipoReactor.TANQUE_ALMACENAMIENTO, [TipoMaterial.PRODUCTO_FINAL], 1000, 25, 1, 1.0, 0),
        ("T4", TipoReactor.TANQUE_ALMACENAMIENTO, [TipoMaterial.SUBPRODUCTO], 500, 25, 1, 1.0, 0),
        
        # Mezcladores
        ("M1", TipoReactor.MEZCLADOR, [TipoMaterial.INTERMEDIO], 400, 30, 2, 0.95, 5),
        ("M2", TipoReactor.MEZCLADOR, [TipoMaterial.INTERMEDIO], 350, 30, 2, 0.93, 5),
        
        # Separadores
        ("S1", TipoReactor.SEPARADOR, [TipoMaterial.INTERMEDIO, TipoMaterial.SUBPRODUCTO], 300, 50, 3, 0.90, 10),
        ("S2", TipoReactor.SEPARADOR, [TipoMaterial.INTERMEDIO, TipoMaterial.SUBPRODUCTO], 250, 45, 3, 0.88, 10),
        
        # Destiladores
        ("D1", TipoReactor.DESTILADOR, [TipoMaterial.PRODUCTO_FINAL], 200, 80, 5, 0.95, 20),
        ("D2", TipoReactor.DESTILADOR, [TipoMaterial.PRODUCTO_FINAL], 150, 75, 4, 0.93, 15),
    ]
    
    for nombre, tipo, materiales, capacidad, temp, pres, eficiencia, tiempo in nodos:
        planta.agregar_nodo(nombre, tipo, materiales, capacidad, temp, pres, eficiencia, tiempo)
    
    # Agregar transformaciones (origen -> destino, material, factor_conversion, perdidas)
    transformaciones = [
        # R1 (reactor base) -> intermedios
        ("R1", "R3", TipoMaterial.INTERMEDIO, 0.95, 0.02, False),
        ("R1", "R4", TipoMaterial.INTERMEDIO, 0.90, 0.03, False),
        ("R1", "T1", TipoMaterial.INTERMEDIO, 0.98, 0.01, False),
        
        # R2 (reactor base) -> intermedios ("R2", "R4", TipoMaterial.INTERMEDIO, 0.92, 0.02, False),
        ("R2", "R5", TipoMaterial.INTERMEDIO, 0.88, 0.03, False),
        ("R2", "T2", TipoMaterial.INTERMEDIO, 0.97, 0.01, False),
        
        # Intermedios -> reactores finales
        ("R3", "R6", TipoMaterial.PRODUCTO_FINAL, 0.90, 0.05, True),
        ("R3", "T3", TipoMaterial.PRODUCTO_FINAL, 0.95, 0.02, False),
        ("R4", "R6", TipoMaterial.PRODUCTO_FINAL, 0.88, 0.05, True),
        ("R4", "R7", TipoMaterial.PRODUCTO_FINAL, 0.85, 0.06, True),
        ("R5", "R7", TipoMaterial.PRODUCTO_FINAL, 0.82, 0.07, True),
        
        # Intermedios -> mezcladores
        ("R3", "M1", TipoMaterial.INTERMEDIO, 0.95, 0.01, False),
        ("R4", "M2", TipoMaterial.INTERMEDIO, 0.93, 0.01, False),
        ("R5", "M1", TipoMaterial.INTERMEDIO, 0.90, 0.02, False),
        ("R5", "M2", TipoMaterial.INTERMEDIO, 0.88, 0.02, False),
        
        # Mezcladores -> separadores
        ("M1", "S1", TipoMaterial.INTERMEDIO, 0.90, 0.03, True),
        ("M2", "S2", TipoMaterial.INTERMEDIO, 0.88, 0.03, True),
        
        # Separadores -> destiladores
        ("S1", "D1", TipoMaterial.PRODUCTO_FINAL, 0.85, 0.08, True),
        ("S1", "T4", TipoMaterial.SUBPRODUCTO, 0.80, 0.05, False),
        ("S2", "D2", TipoMaterial.PRODUCTO_FINAL, 0.82, 0.08, True),
        ("S2", "T4", TipoMaterial.SUBPRODUCTO, 0.78, 0.05, False),
        
        # Destiladores -> productos finales
        ("D1", "T3", TipoMaterial.PRODUCTO_FINAL, 0.98, 0.01, True),
        ("D2", "T3", TipoMaterial.PRODUCTO_FINAL, 0.97, 0.01, True),
        
        # Conexiones entre tanques
        ("T1", "R3", TipoMaterial.INTERMEDIO, 1.0, 0.0, False),
        ("T2", "R4", TipoMaterial.INTERMEDIO, 1.0, 0.0, False),
        ("T1", "M1", TipoMaterial.INTERMEDIO, 1.0, 0.0, False),
        ("T2", "M2", TipoMaterial.INTERMEDIO, 1.0, 0.0, False),
    ]
    
    for origen, destino, material, factor, perdidas, validacion in transformaciones:
        planta.agregar_transformacion(origen, destino, material, factor, perdidas, validacion)
    
    return planta


def crear_planta_simple() -> TrazabilidadMateriaPrima:
    """Crea una planta simple para demostración básica"""
    planta = TrazabilidadMateriaPrima("Planta Simple")
    
    # Nodos
    planta.agregar_nodo("A", TipoReactor.REACTOR_BASE, [TipoMaterial.MATERIA_PRIMA])
    planta.agregar_nodo("B", TipoReactor.REACTOR_INTERMEDIO, [TipoMaterial.INTERMEDIO])
    planta.agregar_nodo("C", TipoReactor.REACTOR_INTERMEDIO, [TipoMaterial.INTERMEDIO])
    planta.agregar_nodo("D", TipoReactor.REACTOR_FINAL, [TipoMaterial.PRODUCTO_FINAL])
    planta.agregar_nodo("E", TipoReactor.REACTOR_FINAL, [TipoMaterial.PRODUCTO_FINAL])
    planta.agregar_nodo("F", TipoReactor.TANQUE_ALMACENAMIENTO, [TipoMaterial.PRODUCTO_FINAL])
    
    # Transformaciones
    planta.agregar_transformacion("A", "B", TipoMaterial.INTERMEDIO)
    planta.agregar_transformacion("A", "C", TipoMaterial.INTERMEDIO)
    planta.agregar_transformacion("B", "D", TipoMaterial.PRODUCTO_FINAL)
    planta.agregar_transformacion("B", "E", TipoMaterial.PRODUCTO_FINAL)
    planta.agregar_transformacion("C", "E", TipoMaterial.PRODUCTO_FINAL)
    planta.agregar_transformacion("D", "F", TipoMaterial.PRODUCTO_FINAL)
    planta.agregar_transformacion("E", "F", TipoMaterial.PRODUCTO_FINAL)
    
    return planta


def demostracion_completa():
    """Demostración completa de todas las funcionalidades"""
    
    print("="*80)
    print("TRAZABILIDAD DE MATERIA PRIMA")
    print("="*80)
    
    # Crear planta
    planta = crear_planta_quimica_ejemplo()
    
    # ============================================
    # EJEMPLO 1: Trazabilidad básica (DFS iterativo)
    # ============================================
    print("\n" + "="*80)
    print("EJEMPLO 1: TRAZABILIDAD BÁSICA")
    print("="*80)
    
    planta.mostrar_trazabilidad("R1")
    
    # ============================================
    # EJEMPLO 2: Trazabilidad con profundidad limitada
    # ============================================
    print("\n" + "="*80)
    print("EJEMPLO 2: TRAZABILIDAD CON PROFUNDIDAD LIMITADA")
    print("="*80)
    
    planta.mostrar_trazabilidad("R1", max_profundidad=2)
    
    # ============================================
    # EJEMPLO 3: Simulación de contaminación
    # ============================================
    print("\n" + "="*80)
    print("EJEMPLO 3: SIMULACIÓN DE CONTAMINACIÓN")
    print("="*80)
    
    planta.mostrar_simulacion("R1", nivel_inicial=100.0, factor_decremento=0.6)
    
    # ============================================
    # EJEMPLO 4: Análisis de impacto
    # ============================================
    print("\n" + "="*80)
    print("EJEMPLO 4: ANÁLISIS DE IMPACTO")
    print("="*80)
    
    impacto = planta.analizar_impacto("R1")
    
    print("ANÁLISIS DE IMPACTO:")
    print(f"   • Total de nodos afectados: {impacto['total_afectados']}")
    print(f"   • Profundidad máxima: {impacto['profundidad_maxima']}")
    print(f"   • Nivel promedio: {impacto['nivel_promedio']:.1f}%")
    print(f"   • Nivel máximo: {impacto['nivel_maximo']:.1f}%")
    
    print(f"\n   Materiales afectados:")
    for material in impacto['materiales_afectados']:
        print(f"      • {material}")
    
    # ============================================
    # EJEMPLO 5: Recomendaciones de contención
    # ============================================
    print("\n" + "="*80)
    print("EJEMPLO 5: RECOMENDACIONES DE CONTENCIÓN")
    print("="*80)
    
    recomendaciones = planta.recomendar_contencion("R1")
    print("RECOMENDACIONES:")
    for i, rec in enumerate(recomendaciones[:5], 1):
        print(f"   {i}. {rec['accion']} - {rec['nodo']} ({rec['prioridad']})")
        print(f"      {rec['motivo']}")
    
    # ============================================
    # EJEMPLO 6: DFS Recursivo (alternativa)
    # ============================================
    print("\n" + "="*80)
    print("EJEMPLO 6: DFS RECURSIVO")
    print("="*80)
    
    nodos_recursivos = planta.dfs_recursivo("R1", max_profundidad=3)
    print(f"DFS Recursivo (profundidad 3):")
    print(f"   • Nodos encontrados: {len(nodos_recursivos)}")
    for nodo in nodos_recursivos[:5]:
        print(f"   • {nodo.nombre}: nivel {nodo.nivel_contaminacion:.1f}%")
    if len(nodos_recursivos) > 5:
        print(f"   ... y {len(nodos_recursivos)-5} más")
    
    # ============================================
    # EJEMPLO 7: Planta simple
    # ============================================
    print("\n" + "="*80)
    print("EJEMPLO 7: PLANTA SIMPLE")
    print("="*80)
    
    planta_simple = crear_planta_simple()
    planta_simple.mostrar_trazabilidad("A")


# ============================================================
# FUNCIONES ADICIONALES ÚTILES
# ============================================================

def exportar_trazabilidad(nodos_afectados: List[NodoContaminado], archivo: str) -> None:
    """
    Exporta los resultados de trazabilidad a un archivo CSV
    
    Args:
        nodos_afectados: Lista de nodos contaminados
        archivo: Nombre del archivo de salida
    """
    import csv
    
    with open(archivo, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Nodo', 'Tipo', 'NivelContaminacion', 'Profundidad', 'Materiales', 'Estado'])
        
        for nodo in nodos_afectados:
            writer.writerow([
                nodo.nombre,
                nodo.tipo,
                f"{nodo.nivel_contaminacion:.2f}",
                nodo.profundidad,
                '; '.join(nodo.materiales_afectados),
                nodo.estado.value
            ])


def generar_reporte_trazabilidad(planta: TrazabilidadMateriaPrima, 
                                nodo_origen: str) -> str:
    """
    Genera un reporte en texto de la trazabilidad
    
    Args:
        planta: Planta química
        nodo_origen: Nodo donde inicia la contaminación
        
    Returns:
        String con el reporte
    """
    nodos_afectados = planta.dfs_iterativo(nodo_origen)
    impacto = planta.analizar_impacto(nodo_origen)
    
    reporte = []
    reporte.append("=" * 60)
    reporte.append(f"REPORTE DE TRAZABILIDAD - {planta.nombre_planta}")
    reporte.append("=" * 60)
    reporte.append(f"Nodo origen: {nodo_origen}")
    reporte.append("")
    reporte.append(f"ESTADÍSTICAS:")
    reporte.append(f"   • Nodos afectados: {len(nodos_afectados)}")
    reporte.append(f"   • Profundidad máxima: {impacto['profundidad_maxima']}")
    reporte.append(f"   • Nivel promedio: {impacto['nivel_promedio']:.1f}%")
    reporte.append("")
    reporte.append(f"NODOS AFECTADOS:")
    
    for nodo in nodos_afectados:
        materiales = ", ".join(nodo.materiales_afectados[:3])
        if len(nodo.materiales_afectados) > 3:
            materiales += f" +{len(nodo.materiales_afectados)-3}"
        
        reporte.append(f"   • {nodo.nombre} (P{nodo.profundidad}): "
                      f"{nodo.nivel_contaminacion:.1f}% - {materiales}")
    
    reporte.append("")
    reporte.append("=" * 60)
    
    return "\n".join(reporte)


if __name__ == "__main__":
    demostracion_completa()
    
    # Ejemplo de reporte
    print("\n" + "="*80)
    print("GENERACIÓN DE REPORTE")
    print("="*80)
    
    planta_reporte = crear_planta_quimica_ejemplo()
    reporte = generar_reporte_trazabilidad(planta_reporte, "R1")
    print(reporte)
