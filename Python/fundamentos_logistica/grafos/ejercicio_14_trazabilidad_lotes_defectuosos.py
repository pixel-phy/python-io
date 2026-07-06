"""Ejercicio 14: Trazabilidad de Lotes defectuosos 

Una empresa química distribuye reactivos entre varias plantas de mezcla. Si la planta inicial 
genera un lote contaminado, este se envía a sus vecinas directas, y estas a las suyas.
Implementa un BFS que reciba la lista de adyacencia de envíos y el nombre de la planta origen.
Retorna una lista con el orden cronológico en el que las plantas se irán infectando/contaminando.
"""
from typing import Dict, List, Set, Tuple, Optional
from collections import deque, defaultdict
from enum import Enum
from dataclasses import dataclass

class EstadoLote(Enum):
    """Estado de contaminación de una planta"""
    LIMPIO = "limpio"
    CONTAMINADO = "contaminado"
    EN_CONTAMINACION = "en_contaminacion"
    AISLADO = "aislado"

@dataclass
class PlantaInfo:
    """Información detallada de una planta durante la contaminación"""
    nombre: str
    tiempo_contaminacion: Optional[int] = None
    nivel_contaminacion: float = 0.0
    plantas_origen: List[str] = None
    
    def __post_init__(self):
        if self.plantas_origen is None:
            self.plantas_origen = []

class TrazabilidadContaminacion:
    """
    Clase para rastrear la propagación de lotes contaminados en una red de plantas.
    """
    
    def __init__(self):
        """Inicializa la red de plantas"""
        self.adyacencia: Dict[str, Set[str]] = defaultdict(set)
        self.plantas_info: Dict[str, PlantaInfo] = {}
        self.nivel_contaminacion: Dict[str, float] = defaultdict(float)
        self.historial_contaminacion: List[Dict] = []
        self.plantas_aisladas: Set[str] = set()
    
    def agregar_conexion(self, planta1: str, planta2: str) -> None:
        """Agrega una conexión bidireccional entre dos plantas"""
        if planta1 == planta2:
            raise ValueError("No se puede conectar una planta consigo misma")
        
        self.adyacencia[planta1].add(planta2)
        self.adyacencia[planta2].add(planta1)
        
        if planta1 not in self.plantas_info:
            self.plantas_info[planta1] = PlantaInfo(planta1)
        if planta2 not in self.plantas_info:
            self.plantas_info[planta2] = PlantaInfo(planta2)
    
    def aislar_planta(self, planta: str) -> None:
        """Aísla una planta para que no pueda contaminarse"""
        self.plantas_aisladas.add(planta)
    
    def propagar_contaminacion(self, planta_origen: str, 
                               nivel_inicial: float = 100.0,
                               factor_descuento: float = 0.8,
                               incluir_tiempo: bool = True) -> Dict:
        """
        Propaga la contaminación usando un BFS optimizado por capas.
        """
        if planta_origen not in self.adyacencia and planta_origen not in self.plantas_info:
            raise ValueError(f"La planta '{planta_origen}' no existe en la red")
        
        # Reiniciar estados previos en plantas_info para evitar contaminación cruzada de ejecuciones anteriores
        for info in self.plantas_info.values():
            info.tiempo_contaminacion = None
            info.nivel_contaminacion = 0.0
            info.plantas_origen = []

        visitados: Set[str] = set()
        cola: deque = deque([planta_origen])
        orden_contaminacion: List[str] = []
        
        # Diccionarios de retorno rápido requirientes por la interfaz original
        niveles: Dict[str, float] = {}
        tiempo_contaminacion: Dict[str, int] = {}
        origen_contaminacion: Dict[str, List[str]] = defaultdict(list)
        
        if planta_origen not in self.plantas_aisladas:
            visitados.add(planta_origen)
            niveles[planta_origen] = nivel_inicial
            tiempo_contaminacion[planta_origen] = 0
            orden_contaminacion.append(planta_origen)
            origen_contaminacion[planta_origen] = ["ORIGEN"]
            
            # Persistencia directa en el modelo de datos de la planta
            p_info = self.plantas_info[planta_origen]
            p_info.tiempo_contaminacion = 0
            p_info.nivel_contaminacion = nivel_inicial
            
            self.historial_contaminacion.append({
                'tiempo': 0, 'planta': planta_origen, 'nivel': nivel_inicial, 'origen': "ORIGEN"
            })
        
        tiempo_actual = 0
        while cola:
            # Procesar el nivel/ola actual por completo
            for _ in range(len(cola)):
                planta_actual = cola.popleft()
                nivel_actual = niveles[planta_actual]
                
                # El descuento se calcula en base al emisor de la ola actual
                nivel_vecino = nivel_actual * factor_descuento
                if nivel_vecino <= 0.1:
                    continue  # Disipación total del químico contaminante
                
                for vecino in self.adyacencia.get(planta_actual, set()):
                    if vecino not in visitados and vecino not in self.plantas_aisladas:
                        visitados.add(vecino)
                        cola.append(vecino)
                        
                        niveles[vecino] = nivel_vecino
                        tiempo_contaminacion[vecino] = tiempo_actual + 1
                        orden_contaminacion.append(vecino)
                        origen_contaminacion[vecino].append(planta_actual)
                        
                        # Actualizar tracking de la planta info
                        v_info = self.plantas_info[vecino]
                        v_info.tiempo_contaminacion = tiempo_actual + 1
                        v_info.nivel_contaminacion = nivel_vecino
                        v_info.plantas_origen.append(planta_actual)
                        
                        self.historial_contaminacion.append({
                            'tiempo': tiempo_actual + 1, 'planta': vecino, 'nivel': nivel_vecino, 'origen': planta_actual
                        })
                        self.nivel_contaminacion[vecino] = nivel_vecino
            
            tiempo_actual += 1
            
        return {
            'origen': planta_origen,
            'nivel_inicial': nivel_inicial,
            'factor_descuento': factor_descuento,
            'orden_contaminacion': orden_contaminacion,
            'total_contaminadas': len(orden_contaminacion),
            'niveles': niveles,
            'tiempos': tiempo_contaminacion if incluir_tiempo else None,
            'origenes': dict(origen_contaminacion),
            'plantas_aisladas': list(self.plantas_aisladas),
            'plantas_no_contaminadas': [
                p for p in self.plantas_info if p not in visitados and p not in self.plantas_aisladas
            ]
        }

    def propagar_contaminacion_limitada(self, planta_origen: str,
                                        profundidad_maxima: int = 3,
                                        umbral_contaminacion: float = 10.0) -> Dict:
        """Propaga la contaminación hasta una profundidad máxima"""
        resultado = self.propagar_contaminacion(
            planta_origen, 
            nivel_inicial=100.0,
            factor_descuento=0.7
        )
        
        plantas_filtradas = []
        for planta in resultado['orden_contaminacion']:
            tiempo = resultado['tiempos'].get(planta, 0)
            nivel = resultado['niveles'].get(planta, 0)
            
            if tiempo <= profundidad_maxima and nivel >= umbral_contaminacion:
                plantas_filtradas.append(planta)
        
        resultado['orden_contaminacion_limitada'] = plantas_filtradas
        resultado['profundidad_maxima'] = profundidad_maxima
        resultado['umbral_contaminacion'] = umbral_contaminacion
        
        return resultado
    
    def encontrar_rutas_contaminacion(self, planta_origen: str, 
                                      planta_destino: str) -> List[List[str]]:
        """Encuentra todas las rutas posibles de contaminación entre dos plantas"""
        if planta_origen not in self.adyacencia or planta_destino not in self.adyacencia:
            return []
        
        rutas = []
        cola = deque([(planta_origen, [planta_origen])])
        
        while cola:
            actual, ruta = cola.popleft()
            
            if actual == planta_destino:
                rutas.append(ruta)
                continue
            
            for vecino in self.adyacencia.get(actual, set()):
                if vecino not in ruta:
                    cola.append((vecino, ruta + [vecino]))
        
        return rutas
    
    def analizar_impacto(self, planta_origen: str) -> Dict:
        """Realiza un análisis completo del impacto de una contaminación"""
        resultado = self.propagar_contaminacion(planta_origen)
        
        niveles = resultado['niveles']
        tiempos = resultado['tiempos']
        
        if not niveles:
            return {
                'origen': planta_origen,
                'impacto': 'Ninguno',
                'mensaje': 'La contaminación no se propagó a ninguna planta',
                'total_contaminadas': 0,
                'nivel_promedio': 0,
                'nivel_maximo': 0,
                'nivel_minimo': 0,
                'tiempo_promedio': 0,
                'tiempo_maximo': 0,
                'distribucion': {'alta': 0, 'media': 0, 'baja': 0},
                'plantas_criticas': [],
                'orden_contaminacion': [],
                'plantas_aisladas': resultado.get('plantas_aisladas', []),
                'plantas_no_contaminadas': resultado.get('plantas_no_contaminadas', [])
            }
        
        nivel_promedio = sum(niveles.values()) / len(niveles) if niveles else 0
        nivel_maximo = max(niveles.values()) if niveles else 0
        nivel_minimo = min(niveles.values()) if niveles else 0
        
        tiempo_promedio = sum(tiempos.values()) / len(tiempos) if tiempos else 0
        tiempo_maximo = max(tiempos.values()) if tiempos else 0
        
        distribucion = {'alta': 0, 'media': 0, 'baja': 0}
        for nivel in niveles.values():
            if nivel > 70:
                distribucion['alta'] += 1
            elif nivel > 30:
                distribucion['media'] += 1
            else:
                distribucion['baja'] += 1
        
        plantas_criticas = sorted(
            [(p, niveles[p], tiempos[p]) for p in niveles],
            key=lambda x: (x[1], -x[2]),
            reverse=True
        )[:5]
        
        return {
            'origen': planta_origen,
            'impacto': 'Propagado',
            'total_contaminadas': len(niveles),
            'nivel_promedio': nivel_promedio,
            'nivel_maximo': nivel_maximo,
            'nivel_minimo': nivel_minimo,
            'tiempo_promedio': tiempo_promedio,
            'tiempo_maximo': tiempo_maximo,
            'distribucion': distribucion,
            'plantas_criticas': [
                {'planta': p, 'nivel': n, 'tiempo': t}
                for p, n, t in plantas_criticas
            ],
            'orden_contaminacion': resultado['orden_contaminacion'],
            'plantas_aisladas': resultado.get('plantas_aisladas', []),
            'plantas_no_contaminadas': resultado.get('plantas_no_contaminadas', [])
        }
    
    def mostrar_contaminacion(self, planta_origen: str, 
                              nivel_inicial: float = 100.0,
                              factor_descuento: float = 0.8) -> None:
        """Muestra de forma formateada la propagación de contaminación"""
        print(f"\n{'='*80}")
        print(f"🧪 TRAZABILIDAD DE LOTE CONTAMINADO")
        print(f"   Origen: {planta_origen}")
        print(f"   Nivel inicial: {nivel_inicial}%")
        print(f"   Factor de descuento: {factor_descuento}")
        print(f"{'='*80}")
        
        resultado = self.propagar_contaminacion(planta_origen, nivel_inicial, factor_descuento)
        
        if not resultado['orden_contaminacion']:
            print(f"\n❌ No se propagó contaminación desde '{planta_origen}'")
            if resultado['plantas_aisladas']:
                print(f"   Plantas aisladas: {', '.join(resultado['plantas_aisladas'])}")
            return
        
        print(f"\n📊 ORDEN CRONOLÓGICO DE CONTAMINACIÓN:")
        print(f"   Total de plantas contaminadas: {resultado['total_contaminadas']}")
        
        plantas_por_tiempo = defaultdict(list)
        for planta, tiempo in resultado['tiempos'].items():
            plantas_por_tiempo[tiempo].append(planta)
        
        print(f"\n⏱️ CRONOLOGÍA DE CONTAMINACIÓN:")
        for tiempo in sorted(plantas_por_tiempo.keys()):
            plantas = plantas_por_tiempo[tiempo]
            if tiempo == 0:
                print(f"   T=0 (Origen): {', '.join(plantas)} (100%)")
            else:
                print(f"   T={tiempo}: {', '.join(plantas)}")
        
        print(f"\n📈 DETALLE POR PLANTA:")
        for planta in resultado['orden_contaminacion']:
            nivel = resultado['niveles'].get(planta, 0)
            tiempo = resultado['tiempos'].get(planta, 0)
            ori = resultado['origenes'].get(planta, [])
            
            barra = self._crear_barra_contaminacion(nivel)
            
            print(f"   • {planta:15s} | T={tiempo:2d} | {nivel:5.1f}% {barra} | ← {', '.join(ori)}")
        
        if resultado['plantas_no_contaminadas']:
            print(f"\n🟢 PLANTAS NO CONTAMINADAS:")
            print(f"   {', '.join(resultado['plantas_no_contaminadas'])}")
        
        if resultado['plantas_aisladas']:
            print(f"\n🚫 PLANTAS AISLADAS (Protegidas):")
            print(f"   {', '.join(resultado['plantas_aisladas'])}")
        
        print(f"{'='*80}\n")
    
    def mostrar_analisis_impacto(self, planta_origen: str) -> None:
        """Muestra análisis detallado del impacto de contaminación"""
        print(f"\n{'='*80}")
        print(f"📊 ANÁLISIS DE IMPACTO: {planta_origen}")
        print(f"{'='*80}")
        
        analisis = self.analizar_impacto(planta_origen)
        
        if analisis.get('impacto') == 'Ninguno':
            print(f"ℹ️ {analisis.get('mensaje', 'No se detectó propagación')}")
            if analisis.get('plantas_aisladas'):
                print(f"   Plantas aisladas: {', '.join(analisis['plantas_aisladas'])}")
            return
        
        if analisis['total_contaminadas'] == 0:
            print(f"ℹ️ No se propagó contaminación desde '{planta_origen}'")
            if analisis.get('plantas_aisladas'):
                print(f"   Plantas aisladas: {', '.join(analisis['plantas_aisladas'])}")
            return
        
        print(f"\n📈 ESTADÍSTICAS DE CONTAMINACIÓN:")
        print(f"   • Total de plantas afectadas: {analisis['total_contaminadas']}")
        print(f"   • Nivel promedio: {analisis['nivel_promedio']:.1f}%")
        print(f"   • Nivel máximo: {analisis['nivel_maximo']:.1f}%")
        print(f"   • Nivel mínimo: {analisis['nivel_minimo']:.1f}%")
        print(f"   • Tiempo promedio de contaminación: {analisis['tiempo_promedio']:.1f}")
        print(f"   • Tiempo máximo de contaminación: {analisis['tiempo_maximo']}")
        
        print(f"\n📊 DISTRIBUCIÓN DE CONTAMINACIÓN:")
        print(f"   • Alta (>70%): {analisis['distribucion']['alta']} plantas")
        print(f"   • Media (30-70%): {analisis['distribucion']['media']} plantas")
        print(f"   • Baja (<30%): {analisis['distribucion']['baja']} plantas")
        
        if analisis['plantas_criticas']:
            print(f"\n⚠️ PLANTAS CRÍTICAS (Mayor contaminación):")
            for i, planta in enumerate(analisis['plantas_criticas'], 1):
                print(f"   {i}. {planta['planta']:15s} | {planta['nivel']:.1f}% | T={planta['tiempo']}")
        
        if analisis['orden_contaminacion']:
            print(f"\n🔗 ORDEN DE CONTAMINACIÓN:")
            print(f"   {' → '.join(analisis['orden_contaminacion'])}")
        
        if analisis.get('plantas_aisladas'):
            print(f"\n🛡️ PLANTAS AISLADAS (Protegidas):")
            print(f"   {', '.join(analisis['plantas_aisladas'])}")
        
        if analisis.get('plantas_no_contaminadas'):
            print(f"\n🟢 PLANTAS NO CONTAMINADAS:")
            print(f"   {', '.join(analisis['plantas_no_contaminadas'])}")
        
        print(f"{'='*80}\n")
    
    def _crear_barra_contaminacion(self, nivel: float, longitud: int = 20) -> str:
        """Crea una barra visual del nivel de contaminación"""
        if nivel >= 70:
            color = "🔴"
        elif nivel >= 30:
            color = "🟡"
        else:
            color = "🟢"
        
        num_caracteres = int(nivel / 100 * longitud)
        barra = '█' * num_caracteres + '░' * (longitud - num_caracteres)
        return f"{color} [{barra}]"


# ============================================================
# FUNCIONES DE EJEMPLO
# ============================================================

def crear_red_quimica_ejemplo() -> TrazabilidadContaminacion:
    """Crea una red química de ejemplo para demostración"""
    trazabilidad = TrazabilidadContaminacion()
    
    conexiones = [
        ("PlantaA", "PlantaB"),
        ("PlantaA", "PlantaC"),
        ("PlantaB", "PlantaD"),
        ("PlantaB", "PlantaE"),
        ("PlantaC", "PlantaF"),
        ("PlantaD", "PlantaG"),
        ("PlantaE", "PlantaH"),
        ("PlantaF", "PlantaI"),
        ("PlantaG", "PlantaJ"),
        ("PlantaH", "PlantaJ"),
        ("PlantaI", "PlantaJ"),
        ("PlantaD", "PlantaE"),
        ("PlantaC", "PlantaD"),
    ]
    
    for p1, p2 in conexiones:
        trazabilidad.agregar_conexion(p1, p2)
    
    trazabilidad.aislar_planta("PlantaF")
    trazabilidad.aislar_planta("PlantaG")
    
    return trazabilidad


def demostracion_completa():
    """Demostración completa de todas las funcionalidades"""
    
    print("="*80)
    print("🧪 TRAZABILIDAD DE LOTES DEFECTUOSOS")
    print("="*80)
    
    trazabilidad = crear_red_quimica_ejemplo()
    
    # EJEMPLO 1: Propagación BFS básica
    print("\n" + "="*80)
    print("EJEMPLO 1: PROPAGACIÓN BFS BÁSICA")
    print("="*80)
    
    trazabilidad.mostrar_contaminacion("PlantaA", 100.0, 0.7)
    
    # EJEMPLO 2: Análisis de impacto
    print("\n" + "="*80)
    print("EJEMPLO 2: ANÁLISIS DE IMPACTO")
    print("="*80)
    
    trazabilidad.mostrar_analisis_impacto("PlantaA")
    
    # EJEMPLO 3: Rutas de contaminación
    print("\n" + "="*80)
    print("EJEMPLO 3: RUTAS DE CONTAMINACIÓN")
    print("="*80)
    
    rutas = trazabilidad.encontrar_rutas_contaminacion("PlantaA", "PlantaJ")
    print(f"🔍 Rutas de contaminación de 'PlantaA' a 'PlantaJ':")
    for i, ruta in enumerate(rutas, 1):
        print(f"   Ruta {i}: {' → '.join(ruta)}")
    
    # EJEMPLO 4: Propagación limitada
    print("\n" + "="*80)
    print("EJEMPLO 4: PROPAGACIÓN LIMITADA")
    print("="*80)
    
    resultado_limitado = trazabilidad.propagar_contaminacion_limitada(
        "PlantaA", 
        profundidad_maxima=3,
        umbral_contaminacion=20.0
    )
    
    print(f"📊 Propagación limitada a {resultado_limitado['profundidad_maxima']} niveles")
    print(f"   Plantas contaminadas: {', '.join(resultado_limitado['orden_contaminacion_limitada'])}")


if __name__ == "__main__":
    demostracion_completa()
