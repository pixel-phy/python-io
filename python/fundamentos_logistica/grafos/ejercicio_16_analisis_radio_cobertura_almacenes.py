"""Ejercicio 16: Análisis de Radio con Mínimo de Escalas

Una cadena de supermercados analiza su resiliencia. Quieren saber qué tiendas e intermediarios
se encuentran a una distancia máxima de K saltos de su Centro de distribución
principal (CD). Modifica el BFS para limitar la exploración hasta un nivel de profundidad K y 
retorna todos los nodos alzanzables dentro de ese rango perimetral. """

from typing import Dict, List, Set, Tuple, Optional, Any
from collections import deque, defaultdict
from dataclasses import dataclass, field
from enum import Enum
import math

class TipoTienda(Enum):
    """Clasificación de tiendas según su función"""
    CENTRO_DISTRIBUCION = "centro_distribucion"
    ALMACEN_REGIONAL = "almacen_regional"
    TIENDA_MAYORISTA = "tienda_mayorista"
    TIENDA_MENORISTA = "tienda_menorista"
    PUNTO_VENTA = "punto_venta"
    CENTRO_LOGISTICO = "centro_logistico"

class EstadoCobertura(Enum):
    """Estado de cobertura de una tienda"""
    CUBIERTA = "cubierta"
    NO_CUBIERTA = "no_cubierta"
    PARCIALMENTE_CUBIERTA = "parcialmente_cubierta"
    EN_BORDE = "en_borde"

@dataclass
class TiendaInfo:
    """Información detallada de una tienda"""
    nombre: str
    tipo: TipoTienda
    ubicacion: str
    capacidad: float = 0.0
    poblacion_servida: int = 0
    inventario: float = 0.0
    tiempo_apertura: int = 0  # minutos desde apertura

@dataclass
class NodoCobertura:
    """Nodo en el análisis de cobertura"""
    nombre: str
    nivel: int
    camino: List[str]
    tipo: str
    informacion: Optional[TiendaInfo] = None

@dataclass
class ResultadoCobertura:
    """Resultado del análisis de cobertura"""
    centro_distribucion: str
    radio_cobertura: int
    nodos_cubiertos: List[NodoCobertura]
    nodos_por_nivel: Dict[int, List[str]]
    total_nodos_cubiertos: int
    nodos_en_borde: List[str]
    estadisticas: Dict[str, Any]
    resumen: str

class RedCoberturaAlmacenes:
    """
    Red de tiendas para análisis de cobertura con radio K.
    
    Características:
    - BFS limitado por profundidad K
    - Clasificación de nodos por nivel
    - Identificación de nodos en borde
    - Estadísticas de cobertura
    - Análisis de resiliencia
    - Múltiples métricas de cobertura
    """
    
    def __init__(self):
        """Inicializa la red de tiendas"""
        # Lista de adyacencia: tienda -> [tiendas_vecinas]
        self.adyacencia: Dict[str, Set[str]] = defaultdict(set)
        
        # Información detallada de tiendas
        self.tiendas_info: Dict[str, TiendaInfo] = {}
        
        # Distancias geográficas (opcional)
        self.distancias: Dict[Tuple[str, str], float] = {}
        
        # Tiempos de viaje (opcional)
        self.tiempos_viaje: Dict[Tuple[str, str], int] = {}
        
        # Estadísticas de la red
        self.total_tiendas = 0
        self.total_conexiones = 0
        
        # Cache de análisis de cobertura
        self.cache_cobertura: Dict[Tuple[str, int], ResultadoCobertura] = {}
    
    def agregar_tienda(self, nombre: str, tipo: TipoTienda = TipoTienda.TIENDA_MENORISTA,
                       ubicacion: str = "", capacidad: float = 0.0,
                       poblacion_servida: int = 0, inventario: float = 0.0) -> None:
        """
        Agrega una tienda a la red
        
        Args:
            nombre: Identificador de la tienda
            tipo: Clasificación de la tienda
            ubicacion: Ubicación geográfica
            capacidad: Capacidad de almacenamiento
            poblacion_servida: Población que atiende
            inventario: Inventario disponible
        """
        if nombre in self.tiendas_info:
            raise ValueError(f"La tienda '{nombre}' ya existe en la red")
        
        self.tiendas_info[nombre] = TiendaInfo(
            nombre=nombre,
            tipo=tipo,
            ubicacion=ubicacion,
            capacidad=capacidad,
            poblacion_servida=poblacion_servida,
            inventario=inventario
        )
        self.total_tiendas += 1
    
    def agregar_conexion(self, tienda1: str, tienda2: str, 
                        distancia: float = 0.0, tiempo: int = 0) -> None:
        """
        Agrega una conexión bidireccional entre dos tiendas
        
        Args:
            tienda1: Primera tienda
            tienda2: Segunda tienda
            distancia: Distancia en kilómetros
            tiempo: Tiempo de viaje en minutos
        """
        if tienda1 not in self.tiendas_info:
            raise ValueError(f"La tienda '{tienda1}' no existe")
        if tienda2 not in self.tiendas_info:
            raise ValueError(f"La tienda '{tienda2}' no existe")
        if tienda1 == tienda2:
            raise ValueError("No se puede conectar una tienda consigo misma")
        
        self.adyacencia[tienda1].add(tienda2)
        self.adyacencia[tienda2].add(tienda1)
        
        if distancia > 0:
            self.distancias[(tienda1, tienda2)] = distancia
            self.distancias[(tienda2, tienda1)] = distancia
        
        if tiempo > 0:
            self.tiempos_viaje[(tienda1, tienda2)] = tiempo
            self.tiempos_viaje[(tienda2, tienda1)] = tiempo
        
        self.total_conexiones += 1
    
    def analizar_cobertura(self, cd_principal: str, radio_k: int,
                          incluir_estadisticas: bool = True) -> ResultadoCobertura:
        """
        Analiza la cobertura hasta K saltos desde el CD principal
        
        Args:
            cd_principal: Centro de Distribución principal
            radio_k: Número máximo de saltos (radio de cobertura)
            incluir_estadisticas: Si incluye estadísticas detalladas
            
        Returns:
            ResultadoCobertura con información detallada
        """
        # Validar que el CD exista
        if cd_principal not in self.tiendas_info:
            raise ValueError(f"El Centro de Distribución '{cd_principal}' no existe")
        
        if radio_k < 0:
            raise ValueError(f"El radio K debe ser >= 0: {radio_k}")
        
        # Verificar cache
        cache_key = (cd_principal, radio_k)
        if cache_key in self.cache_cobertura:
            return self.cache_cobertura[cache_key]
        
        # Si radio_k = 0, solo el CD
        if radio_k == 0:
            nodo_cd = NodoCobertura(
                nombre=cd_principal,
                nivel=0,
                camino=[cd_principal],
                tipo=self.tiendas_info[cd_principal].tipo.value,
                informacion=self.tiendas_info[cd_principal]
            )
            
            resultado = ResultadoCobertura(
                centro_distribucion=cd_principal,
                radio_cobertura=0,
                nodos_cubiertos=[nodo_cd],
                nodos_por_nivel={0: [cd_principal]},
                total_nodos_cubiertos=1,
                nodos_en_borde=[cd_principal],
                estadisticas={},
                resumen=f"Radio 0: Solo el CD '{cd_principal}' está cubierto"
            )
            
            self.cache_cobertura[cache_key] = resultado
            return resultado
        
        # BFS limitado por profundidad K
        cola: deque = deque()
        cola.append((cd_principal, 0, [cd_principal]))  # (nodo, nivel, camino)
        
        visitados: Set[str] = {cd_principal}
        nodos_cubiertos: List[NodoCobertura] = []
        nodos_por_nivel: Dict[int, List[str]] = defaultdict(list)
        nodos_en_borde: List[str] = []
        
        # Diccionario para rastrear niveles
        niveles: Dict[str, int] = {cd_principal: 0}
        
        while cola:
            nodo_actual, nivel_actual, camino_actual = cola.popleft()
            
            # Registrar nodo
            nodo_info = self.tiendas_info.get(nodo_actual)
            nodo_cobertura = NodoCobertura(
                nombre=nodo_actual,
                nivel=nivel_actual,
                camino=camino_actual.copy(),
                tipo=nodo_info.tipo.value if nodo_info else "desconocido",
                informacion=nodo_info
            )
            nodos_cubiertos.append(nodo_cobertura)
            nodos_por_nivel[nivel_actual].append(nodo_actual)
            
            # Verificar si es nodo en borde (último nivel o sin vecinos no visitados)
            if nivel_actual == radio_k:
                nodos_en_borde.append(nodo_actual)
                continue
            
            # Explorar vecinos dentro del radio K
            for vecino in self.adyacencia.get(nodo_actual, set()):
                if vecino not in visitados:
                    nuevo_nivel = nivel_actual + 1
                    if nuevo_nivel <= radio_k:
                        visitados.add(vecino)
                        niveles[vecino] = nuevo_nivel
                        nuevo_camino = camino_actual + [vecino]
                        cola.append((vecino, nuevo_nivel, nuevo_camino))
        
        # Calcular estadísticas
        estadisticas = {}
        if incluir_estadisticas:
            estadisticas = self._calcular_estadisticas(
                cd_principal, nodos_cubiertos, nodos_por_nivel, radio_k
            )
        
        # Generar resumen
        resumen = self._generar_resumen_cobertura(
            cd_principal, radio_k, nodos_cubiertos, nodos_por_nivel, nodos_en_borde
        )
        
        resultado = ResultadoCobertura(
            centro_distribucion=cd_principal,
            radio_cobertura=radio_k,
            nodos_cubiertos=nodos_cubiertos,
            nodos_por_nivel=dict(nodos_por_nivel),
            total_nodos_cubiertos=len(nodos_cubiertos),
            nodos_en_borde=nodos_en_borde,
            estadisticas=estadisticas,
            resumen=resumen
        )
        
        # Guardar en cache
        self.cache_cobertura[cache_key] = resultado
        return resultado
    
    def _calcular_estadisticas(self, cd_principal: str, 
                               nodos_cubiertos: List[NodoCobertura],
                               nodos_por_nivel: Dict[int, List[str]],
                               radio_k: int) -> Dict[str, Any]:
        """Calcula estadísticas detalladas de cobertura"""
        
        # Conteo por tipo de tienda
        tipos_por_nivel = defaultdict(lambda: defaultdict(int))
        for nodo in nodos_cubiertos:
            tipos_por_nivel[nodo.nivel][nodo.tipo] += 1
        
        # Distribución por tipo (total)
        distribucion_tipos = defaultdict(int)
        for nodo in nodos_cubiertos:
            distribucion_tipos[nodo.tipo] += 1
        
        # Porcentaje de cobertura (si conocemos total de tiendas)
        porcentaje_cobertura = (len(nodos_cubiertos) / self.total_tiendas * 100) if self.total_tiendas > 0 else 0
        
        # Nodos por nivel
        nodos_por_nivel_counts = {
            nivel: len(nodos) for nivel, nodos in nodos_por_nivel.items()
        }
        
        # Densidad de conexiones en la cobertura
        conexiones_en_cobertura = 0
        for nodo in nodos_cubiertos:
            for vecino in self.adyacencia.get(nodo.nombre, set()):
                if vecino in [n.nombre for n in nodos_cubiertos]:
                    conexiones_en_cobertura += 1
        densidad_conexiones = (conexiones_en_cobertura / 2) / (len(nodos_cubiertos) * (len(nodos_cubiertos) - 1) / 2) if len(nodos_cubiertos) > 1 else 0
        
        # Capacidad total cubierta
        capacidad_total = sum(nodo.informacion.capacidad for nodo in nodos_cubiertos if nodo.informacion)
        poblacion_total = sum(nodo.informacion.poblacion_servida for nodo in nodos_cubiertos if nodo.informacion)
        inventario_total = sum(nodo.informacion.inventario for nodo in nodos_cubiertos if nodo.informacion)
        
        return {
            'porcentaje_cobertura': porcentaje_cobertura,
            'distribucion_tipos': dict(distribucion_tipos),
            'tipos_por_nivel': dict(tipos_por_nivel),
            'nodos_por_nivel_counts': nodos_por_nivel_counts,
            'densidad_conexiones': densidad_conexiones,
            'capacidad_total_cubierta': capacidad_total,
            'poblacion_total_cubierta': poblacion_total,
            'inventario_total_cubierto': inventario_total,
            'promedio_nodos_por_nivel': len(nodos_cubiertos) / (radio_k + 1) if radio_k > 0 else 1,
            'nodos_en_borde': len([n for n in nodos_cubiertos if n.nivel == radio_k])
        }
    
    def _generar_resumen_cobertura(self, cd_principal: str, radio_k: int,
                                   nodos_cubiertos: List[NodoCobertura],
                                   nodos_por_nivel: Dict[int, List[str]],
                                   nodos_en_borde: List[str]) -> str:
        """Genera un resumen legible del análisis de cobertura"""
        
        total = len(nodos_cubiertos)
        niveles = len(nodos_por_nivel)
        
        resumen = f"Radio de cobertura {radio_k} desde CD '{cd_principal}': "
        resumen += f"se cubren {total} tiendas en {niveles} nivel(es)"
        
        if total > 0:
            # Nivel máximo alcanzado
            max_nivel = max(nodos_por_nivel.keys()) if nodos_por_nivel else 0
            resumen += f", profundidad máxima: {max_nivel}"
            
            # Nodos en borde
            if nodos_en_borde:
                resumen += f", {len(nodos_en_borde)} tiendas en el borde del radio"
            
            # Porcentaje de cobertura
            porcentaje = (total / self.total_tiendas * 100) if self.total_tiendas > 0 else 0
            resumen += f", cubre el {porcentaje:.1f}% de la red"
        
        return resumen
    
    def obtener_nodos_por_nivel(self, resultado: ResultadoCobertura) -> Dict[int, List[str]]:
        """Obtiene los nodos agrupados por nivel de cobertura"""
        return resultado.nodos_por_nivel
    
    def obtener_nodos_en_borde(self, resultado: ResultadoCobertura) -> List[str]:
        """Obtiene los nodos en el borde del radio de cobertura"""
        return resultado.nodos_en_borde
    
    def encontrar_nodos_no_cubiertos(self, cd_principal: str, radio_k: int) -> List[str]:
        """
        Encuentra los nodos que NO están cubiertos dentro del radio K
        
        Args:
            cd_principal: Centro de Distribución principal
            radio_k: Radio de cobertura
            
        Returns:
            Lista de nodos no cubiertos
        """
        resultado = self.analizar_cobertura(cd_principal, radio_k)
        nodos_cubiertos_nombres = {nodo.nombre for nodo in resultado.nodos_cubiertos}
        
        return [tienda for tienda in self.tiendas_info if tienda not in nodos_cubiertos_nombres]
    
    def encontrar_cobertura_optima(self, cd_principal: str, 
                                  cobertura_objetivo: float = 80.0) -> Dict[str, Any]:
        """
        Encuentra el radio K necesario para alcanzar una cobertura objetivo
        
        Args:
            cd_principal: Centro de Distribución principal
            cobertura_objetivo: Porcentaje de cobertura deseado (0-100)
            
        Returns:
            Dict con el radio óptimo y detalles
        """
        if cobertura_objetivo <= 0 or cobertura_objetivo > 100:
            raise ValueError("El objetivo de cobertura debe estar entre 0 y 100")
        
        # Probar diferentes radios K
        for k in range(0, self.total_tiendas + 1):
            resultado = self.analizar_cobertura(cd_principal, k)
            porcentaje = resultado.estadisticas.get('porcentaje_cobertura', 0)
            
            if porcentaje >= cobertura_objetivo:
                return {
                    'radio_optimo': k,
                    'cobertura_alcanzada': porcentaje,
                    'objetivo': cobertura_objetivo,
                    'nodos_cubiertos': resultado.total_nodos_cubiertos,
                    'nodos_totales': self.total_tiendas,
                    'resultado': resultado
                }
        
        # Si no se alcanza el objetivo con el radio máximo
        resultado = self.analizar_cobertura(cd_principal, self.total_tiendas)
        return {
            'radio_optimo': self.total_tiendas,
            'cobertura_alcanzada': resultado.estadisticas.get('porcentaje_cobertura', 0),
            'objetivo': cobertura_objetivo,
            'nodos_cubiertos': resultado.total_nodos_cubiertos,
            'nodos_totales': self.total_tiendas,
            'resultado': resultado,
            'mensaje': f"No se puede alcanzar {cobertura_objetivo}% de cobertura con esta red"
        }
    
    def analizar_resiliencia(self, cd_principal: str, radio_k: int) -> Dict[str, Any]:
        """
        Analiza la resiliencia de la red en el radio de cobertura
        
        Args:
            cd_principal: Centro de Distribución principal
            radio_k: Radio de cobertura
            
        Returns:
            Dict con métricas de resiliencia
        """
        resultado = self.analizar_cobertura(cd_principal, radio_k)
        
        # Análisis de puntos de fallo
        puntos_fallo = []
        for nodo in resultado.nodos_cubiertos:
            # Si un nodo tiene solo una conexión dentro de la cobertura
            conexiones_dentro = 0
            for vecino in self.adyacencia.get(nodo.nombre, set()):
                if vecino in [n.nombre for n in resultado.nodos_cubiertos]:
                    conexiones_dentro += 1
            
            if conexiones_dentro == 1 and nodo.nivel > 0:
                puntos_fallo.append({
                    'nodo': nodo.nombre,
                    'nivel': nodo.nivel,
                    'tipo': nodo.tipo,
                    'conexiones': conexiones_dentro
                })
        
        # Nodos críticos (con muchas conexiones)
        nodos_criticos = []
        for nodo in resultado.nodos_cubiertos:
            conexiones = len([v for v in self.adyacencia.get(nodo.nombre, set()) 
                            if v in [n.nombre for n in resultado.nodos_cubiertos]])
            if conexiones >= 3:  # Umbral de criticidad
                nodos_criticos.append({
                    'nodo': nodo.nombre,
                    'nivel': nodo.nivel,
                    'conexiones': conexiones
                })
        
        return {
            'radio_cobertura': radio_k,
            'total_nodos_cubiertos': resultado.total_nodos_cubiertos,
            'puntos_fallo': puntos_fallo,
            'nodos_criticos': nodos_criticos,
            'nodos_en_borde': resultado.nodos_en_borde,
            'resiliencia_alta': len(puntos_fallo) == 0,
            'nivel_resiliencia': self._calcular_nivel_resiliencia(puntos_fallo, nodos_criticos, resultado.total_nodos_cubiertos)
        }
    
    def _calcular_nivel_resiliencia(self, puntos_fallo: List[Dict], 
                                   nodos_criticos: List[Dict], 
                                   total_nodos: int) -> str:
        """Calcula el nivel de resiliencia de la red"""
        if total_nodos == 0:
            return "Sin datos"
        
        ratio_puntos_fallo = len(puntos_fallo) / total_nodos
        ratio_nodos_criticos = len(nodos_criticos) / total_nodos
        
        if ratio_puntos_fallo < 0.1 and ratio_nodos_criticos > 0.2:
            return "ALTA"
        elif ratio_puntos_fallo < 0.2 and ratio_nodos_criticos > 0.1:
            return "MEDIA"
        else:
            return "BAJA"
    
    def mostrar_cobertura(self, cd_principal: str, radio_k: int) -> None:
        """
        Muestra de forma formateada el análisis de cobertura
        """
        print(f"\n{'='*80}")
        print(f"ANÁLISIS DE RADIO DE COBERTURA")
        print(f"   Centro de Distribución: {cd_principal}")
        print(f"   Radio de cobertura: {radio_k} saltos")
        print(f"{'='*80}")
        
        try:
            resultado = self.analizar_cobertura(cd_principal, radio_k)
        except ValueError as e:
            print(f"Error: {e}")
            return
        
        print(f"\n{resultado.resumen}")
        
        # Mostrar nodos por nivel
        print(f"\nDISTRIBUCIÓN POR NIVELES:")
        for nivel in sorted(resultado.nodos_por_nivel.keys()):
            nodos = resultado.nodos_por_nivel[nivel]
            icono = "Verde" if nivel == 0 else "Amarillo" if nivel < radio_k else "Rojo"
            if nivel == 0:
                print(f"   Nivel {nivel} (CD): {', '.join(nodos)}")
            elif nivel == radio_k:
                print(f"   Nivel {nivel} (BORDE): {', '.join(nodos)}")
            else:
                print(f"   Nivel {nivel}: {', '.join(nodos)}")
        
        # Mostrar nodos en borde
        if resultado.nodos_en_borde:
            print(f"\nNODOS EN EL BORDE DEL RADIO ({len(resultado.nodos_en_borde)}):")
            print(f"   {', '.join(resultado.nodos_en_borde)}")
        
        # Mostrar estadísticas
        if resultado.estadisticas:
            print(f"\nESTADÍSTICAS:")
            stats = resultado.estadisticas
            print(f"   • Porcentaje de cobertura: {stats.get('porcentaje_cobertura', 0):.1f}%")
            print(f"   • Densidad de conexiones: {stats.get('densidad_conexiones', 0):.2f}")
            print(f"   • Nodos en borde: {stats.get('nodos_en_borde', 0)}")
            print(f"   • Capacidad total cubierta: {stats.get('capacidad_total_cubierta', 0):.1f}")
            print(f"   • Población total cubierta: {stats.get('poblacion_total_cubierta', 0):,}")
            
            # Distribución por tipo
            print(f"\n   Distribución por tipo:")
            for tipo, cantidad in stats.get('distribucion_tipos', {}).items():
                print(f"      • {tipo}: {cantidad}")
        
        # Mostrar nodos no cubiertos
        nodos_no_cubiertos = self.encontrar_nodos_no_cubiertos(cd_principal, radio_k)
        if nodos_no_cubiertos:
            print(f"\nNODOS NO CUBIERTOS ({len(nodos_no_cubiertos)}):")
            # Mostrar primeros 10 para no saturar
            if len(nodos_no_cubiertos) <= 10:
                print(f"   {', '.join(nodos_no_cubiertos)}")
            else:
                print(f"   {', '.join(nodos_no_cubiertos[:10])} ... (+{len(nodos_no_cubiertos) - 10} más)")
        
        print(f"{'='*80}\n")
    
    def mostrar_analisis_resiliencia(self, cd_principal: str, radio_k: int) -> None:
        """Muestra el análisis de resiliencia"""
        print(f"\n{'='*80}")
        print(f"ANÁLISIS DE RESILIENCIA")
        print(f"   Centro de Distribución: {cd_principal}")
        print(f"   Radio de cobertura: {radio_k} saltos")
        print(f"{'='*80}")
        
        resiliencia = self.analizar_resiliencia(cd_principal, radio_k)
        
        print(f"\nNIVEL DE RESILIENCIA: {resiliencia['nivel_resiliencia']}")
        print(f"   Total nodos cubiertos: {resiliencia['total_nodos_cubiertos']}")
        
        if resiliencia['puntos_fallo']:
            print(f"\nPUNTOS DE FALLO POTENCIALES ({len(resiliencia['puntos_fallo'])}):")
            for pf in resiliencia['puntos_fallo']:
                print(f"   • {pf['nodo']} (nivel {pf['nivel']}) - solo {pf['conexiones']} conexión(es)")
        else:
            print("\nNo se detectaron puntos de fallo críticos")
        
        if resiliencia['nodos_criticos']:
            print(f"\nNODOS CRÍTICOS (CENTRALES):")
            for nc in resiliencia['nodos_criticos']:
                print(f"   • {nc['nodo']} (nivel {nc['nivel']}) - {nc['conexiones']} conexiones")
        
        if resiliencia['nodos_en_borde']:
            print(f"\nNODOS EN EL BORDE ({len(resiliencia['nodos_en_borde'])}):")
            print(f"   {', '.join(resiliencia['nodos_en_borde'][:5])}")
            if len(resiliencia['nodos_en_borde']) > 5:
                print(f"   ... (+{len(resiliencia['nodos_en_borde']) - 5} más)")
        
        print(f"{'='*80}\n")


# ============================================================
# EJEMPLOS PRÁCTICOS
# ============================================================

def crear_red_supermercados_ejemplo() -> RedCoberturaAlmacenes:
    """Crea una red de supermercados de ejemplo"""
    red = RedCoberturaAlmacenes()
    
    # Agregar tiendas
    tiendas = [
        # Centro de distribución
        ("CD_Madrid", TipoTienda.CENTRO_DISTRIBUCION, "Madrid", 10000, 500000, 8000),
        
        # Almacenes regionales
        ("AR_Norte", TipoTienda.ALMACEN_REGIONAL, "Burgos", 5000, 200000, 4000),
        ("AR_Sur", TipoTienda.ALMACEN_REGIONAL, "Sevilla", 4500, 180000, 3500),
        ("AR_Este", TipoTienda.ALMACEN_REGIONAL, "Valencia", 4000, 160000, 3000),
        ("AR_Oeste", TipoTienda.ALMACEN_REGIONAL, "Salamanca", 3500, 140000, 2800),
        ("AR_Centro", TipoTienda.ALMACEN_REGIONAL, "Toledo", 3000, 120000, 2500),
        
        # Tiendas mayoristas
        ("TM_Barcelona", TipoTienda.TIENDA_MAYORISTA, "Barcelona", 2000, 80000, 2000),
        ("TM_Bilbao", TipoTienda.TIENDA_MAYORISTA, "Bilbao", 1800, 70000, 1800),
        ("TM_Alicante", TipoTienda.TIENDA_MAYORISTA, "Alicante", 1500, 60000, 1500),
        ("TM_Malaga", TipoTienda.TIENDA_MAYORISTA, "Málaga", 1600, 65000, 1600),
        ("TM_Zaragoza", TipoTienda.TIENDA_MAYORISTA, "Zaragoza", 1700, 68000, 1700),
        
        # Tiendas minoristas
        ("Tienda1", TipoTienda.TIENDA_MENORISTA, "Madrid-Centro", 500, 20000, 500),
        ("Tienda2", TipoTienda.TIENDA_MENORISTA, "Madrid-Norte", 450, 18000, 450),
        ("Tienda3", TipoTienda.TIENDA_MENORISTA, "Madrid-Sur", 400, 16000, 400),
        ("Tienda4", TipoTienda.TIENDA_MENORISTA, "Barcelona-Centro", 500, 20000, 500),
        ("Tienda5", TipoTienda.TIENDA_MENORISTA, "Barcelona-Norte", 450, 18000, 450),
        ("Tienda6", TipoTienda.TIENDA_MENORISTA, "Valencia-Centro", 400, 16000, 400),
        ("Tienda7", TipoTienda.TIENDA_MENORISTA, "Sevilla-Centro", 400, 16000, 400),
        ("Tienda8", TipoTienda.TIENDA_MENORISTA, "Bilbao-Centro", 350, 14000, 350),
        ("Tienda9", TipoTienda.TIENDA_MENORISTA, "Alicante-Centro", 300, 12000, 300),
        ("Tienda10", TipoTienda.TIENDA_MENORISTA, "Málaga-Centro", 300, 12000, 300),
        
        # Puntos de venta
        ("PV1", TipoTienda.PUNTO_VENTA, "Madrid-Usera", 100, 5000, 100),
        ("PV2", TipoTienda.PUNTO_VENTA, "Madrid-Carabanchel", 100, 5000, 100),
        ("PV3", TipoTienda.PUNTO_VENTA, "Barcelona-Gracia", 100, 5000, 100),
        ("PV4", TipoTienda.PUNTO_VENTA, "Valencia-Ruzafa", 100, 5000, 100),
        ("PV5", TipoTienda.PUNTO_VENTA, "Sevilla-Triana", 100, 5000, 100),
        
        # Centros logísticos
        ("CL_Castellon", TipoTienda.CENTRO_LOGISTICO, "Castellón", 2500, 100000, 2200),
        ("CL_Tarragona", TipoTienda.CENTRO_LOGISTICO, "Tarragona", 2300, 90000, 2000),
        ("CL_Almeria", TipoTienda.CENTRO_LOGISTICO, "Almería", 2000, 80000, 1800),
    ]
    
    for nombre, tipo, ubicacion, capacidad, poblacion, inventario in tiendas:
        red.agregar_tienda(nombre, tipo, ubicacion, capacidad, poblacion, inventario)
    
    # Agregar conexiones (rutas de distribución)
    conexiones = [
        # CD -> Almacenes Regionales
        ("CD_Madrid", "AR_Norte", 250, 180),
        ("CD_Madrid", "AR_Sur", 420, 300),
        ("CD_Madrid", "AR_Este", 320, 240),
        ("CD_Madrid", "AR_Oeste", 200, 150),
        ("CD_Madrid", "AR_Centro", 80, 60),
        
        # Almacenes Regionales -> Tiendas Mayoristas
        ("AR_Norte", "TM_Bilbao", 150, 120),
        ("AR_Norte", "TM_Zaragoza", 220, 170),
        ("AR_Este", "TM_Barcelona", 300, 230),
        ("AR_Este", "TM_Alicante", 170, 130),
        ("AR_Sur", "TM_Malaga", 200, 160),
        ("AR_Centro", "TM_Barcelona", 450, 340),
        ("AR_Oeste", "TM_Bilbao", 350, 270),
        
        # Tiendas Mayoristas -> Centros Logísticos
        ("TM_Barcelona", "CL_Tarragona", 100, 75),
        ("TM_Alicante", "CL_Castellon", 150, 115),
        ("TM_Malaga", "CL_Almeria", 180, 140),
        ("TM_Zaragoza", "CL_Castellon", 220, 170),
        
        # Tiendas Mayoristas -> Tiendas Minoristas
        ("TM_Barcelona", "Tienda4", 10, 5),
        ("TM_Barcelona", "Tienda5", 15, 8),
        ("TM_Bilbao", "Tienda8", 5, 3),
        ("TM_Alicante", "Tienda9", 5, 3),
        ("TM_Malaga", "Tienda10", 5, 3),
        ("AR_Centro", "Tienda1", 20, 15),
        ("AR_Centro", "Tienda2", 25, 18),
        ("AR_Centro", "Tienda3", 30, 22),
        ("AR_Este", "Tienda6", 10, 7),
        ("AR_Sur", "Tienda7", 10, 7),
        
        # Tiendas Minoristas -> Puntos de Venta
        ("Tienda1", "PV1", 5, 3),
        ("Tienda1", "PV2", 8, 5),
        ("Tienda4", "PV3", 5, 3),
        ("Tienda6", "PV4", 5, 3),
        ("Tienda7", "PV5", 5, 3),
        
        # Conexiones entre Almacenes Regionales (para redundancia)
        ("AR_Norte", "AR_Este", 350, 270),
        ("AR_Norte", "AR_Oeste", 280, 210),
        ("AR_Este", "AR_Sur", 450, 340),
        ("AR_Sur", "AR_Oeste", 380, 290),
        
        # Conexiones entre Tiendas Mayoristas
        ("TM_Barcelona", "TM_Zaragoza", 280, 210),
        ("TM_Bilbao", "TM_Zaragoza", 200, 150),
        ("TM_Alicante", "TM_Malaga", 320, 240),
    ]
    
    for t1, t2, distancia, tiempo in conexiones:
        red.agregar_conexion(t1, t2, distancia, tiempo)
    
    return red


def crear_red_logistica_simple() -> RedCoberturaAlmacenes:
    """Crea una red simple para demostración básica"""
    red = RedCoberturaAlmacenes()
    
    # Agregar nodos
    nodos = [
        ("CD", TipoTienda.CENTRO_DISTRIBUCION, "Central", 1000, 100000, 5000),
        ("A", TipoTienda.ALMACEN_REGIONAL, "Región A", 500, 50000, 2500),
        ("B", TipoTienda.ALMACEN_REGIONAL, "Región B", 500, 50000, 2500),
        ("C", TipoTienda.ALMACEN_REGIONAL, "Región C", 500, 50000, 2500),
        ("D", TipoTienda.TIENDA_MAYORISTA, "Mayorista D", 200, 20000, 1000),
        ("E", TipoTienda.TIENDA_MAYORISTA, "Mayorista E", 200, 20000, 1000),
        ("F", TipoTienda.TIENDA_MENORISTA, "Tienda F", 100, 10000, 500),
        ("G", TipoTienda.TIENDA_MENORISTA, "Tienda G", 100, 10000, 500),
        ("H", TipoTienda.TIENDA_MENORISTA, "Tienda H", 100, 10000, 500),
        ("I", TipoTienda.PUNTO_VENTA, "PV I", 50, 5000, 200),
        ("J", TipoTienda.PUNTO_VENTA, "PV J", 50, 5000, 200),
        ("K", TipoTienda.PUNTO_VENTA, "PV K", 50, 5000, 200),
        ("L", TipoTienda.PUNTO_VENTA, "PV L", 50, 5000, 200),
    ]
    
    for nombre, tipo, ubicacion, capacidad, poblacion, inventario in nodos:
        red.agregar_tienda(nombre, tipo, ubicacion, capacidad, poblacion, inventario)
    
    # Agregar conexiones
    conexiones = [
        ("CD", "A"), ("CD", "B"), ("CD", "C"),
        ("A", "D"), ("A", "E"),
        ("B", "D"), ("B", "F"),
        ("C", "E"), ("C", "G"),
        ("D", "H"), ("D", "I"),
        ("E", "J"), ("E", "K"),
        ("F", "L"),
        ("G", "L"),
        ("H", "I"),
        ("J", "K"),
        ("A", "C"),  # Conexión adicional
        ("D", "E"),  # Conexión adicional
    ]
    
    for t1, t2 in conexiones:
        red.agregar_conexion(t1, t2)
    
    return red


def demostracion_completa():
    """Demostración completa de todas las funcionalidades"""
    
    print("="*80)
    print("ANÁLISIS DE RADIO DE COBERTURA DE ALMACENES")
    print("="*80)
    
    # Crear red
    red = crear_red_supermercados_ejemplo()
    
    # ============================================
    # Prueba 1: Cobertura con radio K=1
    # ============================================
    print("\n" + "="*80)
    print("Prueba 1: COBERTURA CON RADIO K=1")
    print("="*80)
    
    red.mostrar_cobertura("CD_Madrid", 1)
    
    # ============================================
    # Prueba 2: Cobertura con radio K=2
    # ============================================
    print("\n" + "="*80)
    print("Prueba 2: COBERTURA CON RADIO K=2")
    print("="*80)
    
    red.mostrar_cobertura("CD_Madrid", 2)
    
    # ============================================
    # Prueba 3: Cobertura con radio K=3
    # ============================================
    print("\n" + "="*80)
    print("Prueba 3: COBERTURA CON RADIO K=3")
    print("="*80)
    
    red.mostrar_cobertura("CD_Madrid", 3)
    
    # ============================================
    # Prueba 4: Análisis de resiliencia
    # ============================================
    print("\n" + "="*80)
    print("Prueba 4: ANÁLISIS DE RESILIENCIA")
    print("="*80)
    
    red.mostrar_analisis_resiliencia("CD_Madrid", 2)
    
    # ============================================
    # Prueba 5: Cobertura óptima
    # ============================================
    print("\n" + "="*80)
    print("Prueba 5: COBERTURA ÓPTIMA")
    print("="*80)
    
    optimo = red.encontrar_cobertura_optima("CD_Madrid", 75.0)
    print(f"Análisis de cobertura óptima:")
    print(f"   • Objetivo: {optimo['objetivo']}% de cobertura")
    print(f"   • Radio óptimo: {optimo['radio_optimo']} saltos")
    print(f"   • Cobertura alcanzada: {optimo['cobertura_alcanzada']:.1f}%")
    print(f"   • Nodos cubiertos: {optimo['nodos_cubiertos']} de {optimo['nodos_totales']}")
    
    if 'mensaje' in optimo:
        print(f"   • Mensaje: {optimo['mensaje']}")
    
    # ============================================
    # Prueba 6: Red simple para comparación
    # ============================================
    print("\n" + "="*80)
    print("Prueba 6: RED SIMPLE - COMPARACIÓN DE RADIOS")
    print("="*80)
    
    red_simple = crear_red_logistica_simple()
    
    for k in [0, 1, 2, 3]:
        resultado = red_simple.analizar_cobertura("CD", k)
        print(f"Radio K={k}: {resultado.total_nodos_cubiertos} nodos cubiertos")
        for nivel in sorted(resultado.nodos_por_nivel.keys()):
            print(f"   Nivel {nivel}: {', '.join(resultado.nodos_por_nivel[nivel])}")
        print()
    
    # ============================================
    # Prueba 7: Nodos no cubiertos
    # ============================================
    print("\n" + "="*80)
    print("Prueba 7: NODOS NO CUBIERTOS")
    print("="*80)
    
    no_cubiertos = red.encontrar_nodos_no_cubiertos("CD_Madrid", 2)
    print(f"Nodos no cubiertos con radio K=2:")
    if no_cubiertos:
        print(f"   {', '.join(no_cubiertos[:10])}")
        if len(no_cubiertos) > 10:
            print(f"   ... (+{len(no_cubiertos) - 10} más)")
    else:
        print("   Todos los nodos están cubiertos")


# ============================================================
# FUNCIONES ADICIONALES ÚTILES
# ============================================================

def visualizar_cobertura_ascii(resultado: ResultadoCobertura) -> str:
    """Genera una representación ASCII del árbol de cobertura"""
    if not resultado:
        return "Sin datos de cobertura"
    
    visual = []
    visual.append("ÁRBOL DE COBERTURA")
    visual.append("=" * 60)
    
    for nivel in sorted(resultado.nodos_por_nivel.keys()):
        nodos = resultado.nodos_por_nivel[nivel]
        indent = "  " * nivel
        
        if nivel == 0:
            visual.append(f"{indent} {', '.join(nodos)} (CD)")
        elif nivel == resultado.radio_cobertura:
            visual.append(f"{indent} {', '.join(nodos)} (BORDE)")
        else:
            visual.append(f"{indent} {', '.join(nodos)}")
        
        # Conectar niveles
        if nivel < max(resultado.nodos_por_nivel.keys()):
            visual.append(f"{indent}  ↓")
    
    visual.append("=" * 60)
    visual.append(f"Total nodos: {resultado.total_nodos_cubiertos}")
    visual.append(f"Radio: {resultado.radio_cobertura}")
    
    return "\n".join(visual)


def exportar_cobertura_csv(resultado: ResultadoCobertura, archivo: str) -> None:
    """Exporta los resultados de cobertura a CSV"""
    import csv
    
    with open(archivo, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Nodo', 'Nivel', 'Tipo', 'Camino', 'EnBorde'])
        
        for nodo in resultado.nodos_cubiertos:
            writer.writerow([
                nodo.nombre,
                nodo.nivel,
                nodo.tipo,
                ' → '.join(nodo.camino),
                'Sí' if nodo.nivel == resultado.radio_cobertura else 'No'
            ])


if __name__ == "__main__":
    demostracion_completa()
    
    # Ejemplo adicional de visualización ASCII
    print("\n" + "="*80)
    print("VISUALIZACIÓN ASCII DE COBERTURA")
    print("="*80)
    
    red_simple = crear_red_logistica_simple()
    resultado = red_simple.analizar_cobertura("CD", 2)
    print(visualizar_cobertura_ascii(resultado))
