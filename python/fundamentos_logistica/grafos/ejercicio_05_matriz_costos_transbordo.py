""" Matriz de Costos de Transbordo desde Incidencia

Imagina que te dan una lista cruda de aristas que representan rutas de camiones con el formato:
(Origen, Destino, Costo). Diseña un componente que procese esta lista y construya una estructura
que permita responder eficientemente a la pregunta: ¿Existe una ruta directa de A hacia B?
Si es así, ¿Cuál es su costo y qué porcentaje representa respecto al costo total de todas las
rutas que salen de A?
"""

from typing import Dict, List, Tuple, Optional, Set
from collections import defaultdict
import math
from enum import Enum

class TipoRuta(Enum):
    """Tipos de rutas según su importancia"""
    CRITICA = "crítica"  # > 50% del total
    IMPORTANTE = "importante"  # > 20% del total
    SECUNDARIA = "secundaria"  # > 5% del total
    MENOR = "menor"  # <= 5% del total

class MatrizCostosTransbordo:
    """
    Componente para gestionar costos de rutas de camiones.
    
    Características:
    - Procesamiento eficiente de lista de aristas
    - Consulta rápida de rutas directas
    - Cálculo de porcentajes sobre costos totales
    - Estadísticas y análisis de rutas
    - Soporte para múltiples métricas
    """
    
    def __init__(self):
        """Inicializa la matriz de costos"""
        # Estructura principal: origen -> {destino -> costo}
        self.rutas: Dict[str, Dict[str, float]] = defaultdict(dict)
        
        # Costos totales por origen (para cálculo de porcentajes)
        self.costo_total_por_origen: Dict[str, float] = defaultdict(float)
        
        # Conjunto de todos los nodos (orígenes y destinos)
        self.nodos: Set[str] = set()
        
        # Estadísticas adicionales
        self.total_rutas = 0
        self.costo_total_global = 0.0
        
        # Índices para búsquedas rápidas
        self.rutas_por_destino: Dict[str, List[Tuple[str, float]]] = defaultdict(list)
        self.rutas_por_costo: List[Tuple[float, str, str]] = []  # (costo, origen, destino)
    
    def procesar_rutas(self, lista_rutas: List[Tuple[str, str, float]]) -> None:
        """
        Procesa una lista de rutas crudas y construye la estructura de datos
        
        Args:
            lista_rutas: Lista de tuplas (Origen, Destino, Costo)
        """
        for origen, destino, costo in lista_rutas:
            self.agregar_ruta(origen, destino, costo)
    
    def agregar_ruta(self, origen: str, destino: str, costo: float) -> None:
        """
        Agrega una ruta individual a la estructura
        
        Args:
            origen: Nodo de origen
            destino: Nodo de destino
            costo: Costo de la ruta (debe ser >= 0)
        """
        # Validaciones
        if costo < 0:
            raise ValueError(f"El costo no puede ser negativo: {costo}")
        if origen == destino:
            raise ValueError("Origen y destino no pueden ser el mismo nodo")
        
        # Actualizar estructura principal
        self.rutas[origen][destino] = costo
        
        # Actualizar nodos
        self.nodos.add(origen)
        self.nodos.add(destino)
        
        # Actualizar costos totales
        self.costo_total_por_origen[origen] += costo
        
        # Actualizar estadísticas
        self.total_rutas += 1
        self.costo_total_global += costo
        
        # Actualizar índices
        self.rutas_por_destino[destino].append((origen, costo))
        self.rutas_por_costo.append((costo, origen, destino))
    
    def consultar_ruta(self, origen: str, destino: str) -> Dict:
        """
        Consulta si existe una ruta directa de origen a destino
        
        Args:
            origen: Nodo de origen
            destino: Nodo de destino
            
        Returns:
            Dict con información de la ruta
        """
        # Verificar existencia de nodos
        if origen not in self.nodos:
            return {
                'existe': False,
                'origen': origen,
                'destino': destino,
                'mensaje': f"El nodo origen '{origen}' no existe en la red"
            }
        
        if destino not in self.nodos:
            return {
                'existe': False,
                'origen': origen,
                'destino': destino,
                'mensaje': f"El nodo destino '{destino}' no existe en la red"
            }
        
        # Verificar existencia de ruta
        if destino not in self.rutas.get(origen, {}):
            return {
                'existe': False,
                'origen': origen,
                'destino': destino,
                'mensaje': f"No existe ruta directa de '{origen}' a '{destino}'"
            }
        
        # Obtener costo y calcular porcentaje
        costo = self.rutas[origen][destino]
        costo_total_origen = self.costo_total_por_origen[origen]
        porcentaje = (costo / costo_total_origen * 100) if costo_total_origen > 0 else 0
        
        # Calcular tipo de ruta según porcentaje
        tipo = self._clasificar_ruta(porcentaje)
        
        return {
            'existe': True,
            'origen': origen,
            'destino': destino,
            'costo': costo,
            'costo_total_origen': costo_total_origen,
            'porcentaje': porcentaje,
            'tipo': tipo.value,
            'mensaje': f"Ruta encontrada: {origen} -> {destino}, costo: {costo:.2f}, {porcentaje:.1f}% del total de {origen}"
        }
    
    def _clasificar_ruta(self, porcentaje: float) -> TipoRuta:
        """
        Clasifica una ruta según su porcentaje del costo total del origen
        """
        if porcentaje > 50:
            return TipoRuta.CRITICA
        elif porcentaje > 20:
            return TipoRuta.IMPORTANTE
        elif porcentaje > 5:
            return TipoRuta.SECUNDARIA
        else:
            return TipoRuta.MENOR
    
    def obtener_rutas_origen(self, origen: str) -> Dict[str, Dict]:
        """
        Obtiene todas las rutas que salen de un origen con sus porcentajes
        
        Args:
            origen: Nodo de origen
            
        Returns:
            Dict con información de todas las rutas del origen
        """
        if origen not in self.nodos:
            raise ValueError(f"El nodo '{origen}' no existe en la red")
        
        if origen not in self.rutas:
            return {
                'origen': origen,
                'total_rutas': 0,
                'costo_total': 0,
                'rutas': {}
            }
        
        costo_total = self.costo_total_por_origen[origen]
        rutas_info = {}
        
        for destino, costo in self.rutas[origen].items():
            porcentaje = (costo / costo_total * 100) if costo_total > 0 else 0
            rutas_info[destino] = {
                'costo': costo,
                'porcentaje': porcentaje,
                'tipo': self._clasificar_ruta(porcentaje).value
            }
        
        return {
            'origen': origen,
            'total_rutas': len(rutas_info),
            'costo_total': costo_total,
            'rutas': rutas_info
        }
    
    def obtener_rutas_destino(self, destino: str) -> Dict:
        """
        Obtiene todas las rutas que llegan a un destino
        
        Args:
            destino: Nodo de destino
            
        Returns:
            Dict con información de rutas entrantes
        """
        if destino not in self.nodos:
            raise ValueError(f"El nodo '{destino}' no existe en la red")
        
        rutas_entrantes = self.rutas_por_destino.get(destino, [])
        
        return {
            'destino': destino,
            'total_rutas': len(rutas_entrantes),
            'rutas': [
                {
                    'origen': origen,
                    'costo': costo
                }
                for origen, costo in sorted(rutas_entrantes, key=lambda x: x[1])
            ]
        }
    
    def obtener_top_rutas(self, n: int = 5) -> List[Dict]:
        """
        Obtiene las n rutas más costosas de la red
        
        Args:
            n: Número de rutas a retornar
            
        Returns:
            Lista de las n rutas más costosas
        """
        rutas_ordenadas = sorted(self.rutas_por_costo, key=lambda x: x[0], reverse=True)
        top = rutas_ordenadas[:n]
        
        return [
            {
                'costo': costo,
                'origen': origen,
                'destino': destino,
                'porcentaje': self._calcular_porcentaje_global(costo)
            }
            for costo, origen, destino in top
        ]
    
    def _calcular_porcentaje_global(self, costo: float) -> float:
        """Calcula el porcentaje de un costo respecto al total global"""
        return (costo / self.costo_total_global * 100) if self.costo_total_global > 0 else 0
    
    def analisis_origen(self, origen: str) -> Dict:
        """
        Realiza un análisis completo de un nodo origen
        
        Args:
            origen: Nodo a analizar
            
        Returns:
            Dict con análisis detallado
        """
        if origen not in self.nodos:
            raise ValueError(f"El nodo '{origen}' no existe en la red")
        
        if origen not in self.rutas:
            return {
                'origen': origen,
                'tiene_rutas': False,
                'mensaje': f"El nodo '{origen}' no tiene rutas de salida"
            }
        
        rutas_info = self.obtener_rutas_origen(origen)
        total_rutas = rutas_info['total_rutas']
        costo_total = rutas_info['costo_total']
        
        # Calcular estadísticas
        costos = [info['costo'] for info in rutas_info['rutas'].values()]
        if costos:
            costo_min = min(costos)
            costo_max = max(costos)
            costo_promedio = sum(costos) / len(costos)
            costo_mediana = sorted(costos)[len(costos) // 2]
        else:
            costo_min = costo_max = costo_promedio = costo_mediana = 0
        
        # Clasificar rutas por tipo
        clasificacion = defaultdict(int)
        for info in rutas_info['rutas'].values():
            clasificacion[info['tipo']] += 1
        
        # Identificar ruta principal
        ruta_principal = None
        if costos:
            ruta_principal = max(rutas_info['rutas'].items(), 
                                key=lambda x: x[1]['costo'])
        
        return {
            'origen': origen,
            'tiene_rutas': True,
            'total_rutas': total_rutas,
            'costo_total': costo_total,
            'costo_promedio': costo_promedio,
            'costo_mediana': costo_mediana,
            'costo_minimo': costo_min,
            'costo_maximo': costo_max,
            'clasificacion_rutas': dict(clasificacion),
            'ruta_mas_costosa': {
                'destino': ruta_principal[0],
                'costo': ruta_principal[1]['costo'],
                'porcentaje': ruta_principal[1]['porcentaje']
            } if ruta_principal else None,
            'distribucion_porcentajes': [
                {
                    'destino': destino,
                    'porcentaje': info['porcentaje']
                }
                for destino, info in sorted(rutas_info['rutas'].items(), 
                                           key=lambda x: x[1]['porcentaje'], 
                                           reverse=True)
            ]
        }
    
    def comparar_origenes(self, origen1: str, origen2: str) -> Dict:
        """
        Compara dos nodos origen en términos de sus rutas
        
        Args:
            origen1: Primer nodo
            origen2: Segundo nodo
            
        Returns:
            Dict con comparación detallada
        """
        analisis1 = self.analisis_origen(origen1)
        analisis2 = self.analisis_origen(origen2)
        
        # Encontrar destinos comunes
        destinos1 = set(self.rutas.get(origen1, {}).keys())
        destinos2 = set(self.rutas.get(origen2, {}).keys())
        destinos_comunes = destinos1 & destinos2
        
        return {
            'origen1': origen1,
            'origen2': origen2,
            'comparacion': {
                'total_rutas': (analisis1.get('total_rutas', 0), 
                               analisis2.get('total_rutas', 0)),
                'costo_total': (analisis1.get('costo_total', 0), 
                               analisis2.get('costo_total', 0)),
                'costo_promedio': (analisis1.get('costo_promedio', 0), 
                                  analisis2.get('costo_promedio', 0))
            },
            'destinos_comunes': list(destinos_comunes),
            'destinos_exclusivos': {
                'origen1': list(destinos1 - destinos2),
                'origen2': list(destinos2 - destinos1)
            }
        }
    
    def mostrar_consulta(self, origen: str, destino: str) -> None:
        """
        Muestra de forma formateada la consulta de una ruta
        """
        print(f"\n")
        print(f"CONSULTA DE RUTA: {origen} → {destino}")
        
        resultado = self.consultar_ruta(origen, destino)
        
        if not resultado['existe']:
            print(f"{resultado['mensaje']}")
            return
        
        print(f"{resultado['mensaje']}")
        print(f"\nANÁLISIS:")
        print(f"   • Costo de la ruta: ${resultado['costo']:,.2f}")
        print(f"   • Costo total desde {origen}: ${resultado['costo_total_origen']:,.2f}")
        print(f"   • Porcentaje: {resultado['porcentaje']:.2f}%")
        print(f"   • Clasificación: {resultado['tipo'].upper()}")
        
        # Barra de porcentaje visual
        barra = self._crear_barra_porcentaje(resultado['porcentaje'])
        print(f"   • Representación: {barra}")
        
        print(f"\n")
    
    def _crear_barra_porcentaje(self, porcentaje: float, longitud: int = 40) -> str:
        """Crea una barra visual del porcentaje"""
        num_caracteres = int(porcentaje / 100 * longitud)
        barra = '█' * num_caracteres + '░' * (longitud - num_caracteres)
        return f"[{barra}] {porcentaje:.1f}%"
    
    def mostrar_analisis_origen(self, origen: str) -> None:
        """
        Muestra análisis completo de un origen
        """
        print(f"\n")
        print(f"ANÁLISIS DEL NODO ORIGEN: {origen}")
        
        try:
            analisis = self.analisis_origen(origen)
            
            if not analisis.get('tiene_rutas', False):
                print(f"{analisis.get('mensaje', 'Nodo sin rutas')}")
                return
            
            print(f"\nESTADÍSTICAS GENERALES:")
            print(f"   • Total de rutas: {analisis['total_rutas']}")
            print(f"   • Costo total: ${analisis['costo_total']:,.2f}")
            print(f"   • Costo promedio: ${analisis['costo_promedio']:,.2f}")
            print(f"   • Costo mediana: ${analisis['costo_mediana']:,.2f}")
            print(f"   • Costo mínimo: ${analisis['costo_minimo']:,.2f}")
            print(f"   • Costo máximo: ${analisis['costo_maximo']:,.2f}")
            
            print(f"\nCLASIFICACIÓN DE RUTAS:")
            for tipo, cantidad in analisis['clasificacion_rutas'].items():
                print(f"   • {tipo.upper()}: {cantidad} ruta(s)")
            
            print(f"\nDISTRIBUCIÓN DE COSTOS:")
            for item in analisis['distribucion_porcentajes'][:5]:  # Top 5
                barra = self._crear_barra_porcentaje(item['porcentaje'], 30)
                print(f"   • {item['destino']:20s} {barra}")
            
            if analisis['ruta_mas_costosa']:
                rc = analisis['ruta_mas_costosa']
                print(f"\n RUTA MÁS COSTOSA:")
                print(f"   • Destino: {rc['destino']}")
                print(f"   • Costo: ${rc['costo']:,.2f}")
                print(f"   • Porcentaje: {rc['porcentaje']:.2f}%")
            
        except ValueError as e:
            print(f"Error: {e}")
        
        print(f"\n")
    
    def mostrar_resumen_red(self) -> None:
        """Muestra un resumen de toda la red"""
        print(f"\n")
        print(f"RESUMEN DE LA RED DE TRANSBORDO")
        
        print(f"\nESTADÍSTICAS GENERALES:")
        print(f"   • Total de nodos: {len(self.nodos)}")
        print(f"   • Total de rutas: {self.total_rutas}")
        print(f"   • Costo total global: ${self.costo_total_global:,.2f}")
        print(f"   • Costo promedio por ruta: ${(self.costo_total_global/self.total_rutas) if self.total_rutas > 0 else 0:,.2f}")
        
        # Top rutas más costosas
        print(f"\n TOP 5 RUTAS MÁS COSTOSAS:")
        top_rutas = self.obtener_top_rutas(5)
        for i, ruta in enumerate(top_rutas, 1):
            print(f"   {i}. {ruta['origen']} → {ruta['destino']}: ${ruta['costo']:,.2f} ({ruta['porcentaje']:.2f}% global)")
        
        # Nodos con más rutas
        print(f"\n NODOS CON MÁS RUTAS DE SALIDA:")
        nodos_ordenados = sorted(
            [(nodo, len(self.rutas.get(nodo, {}))) for nodo in self.nodos],
            key=lambda x: x[1],
            reverse=True
        )
        for nodo, cantidad in nodos_ordenados[:5]:
            if cantidad > 0:
                print(f"   • {nodo}: {cantidad} ruta(s)")
        
        print(f"\n")


# Prueba

def crear_red_distribucion_ejemplo() -> List[Tuple[str, str, float]]:
    """
    Crea una red de distribución de ejemplo con rutas de camiones
    """
    return [
        # Rutas desde el nodo "CD_Madrid"
        ("CD_Madrid", "Barcelona", 350.50),
        ("CD_Madrid", "Valencia", 280.00),
        ("CD_Madrid", "Sevilla", 530.75),
        ("CD_Madrid", "Bilbao", 410.20),
        ("CD_Madrid", "Málaga", 620.00),
        
        # Rutas desde "CD_Barcelona"
        ("CD_Barcelona", "Zaragoza", 180.00),
        ("CD_Barcelona", "Madrid", 320.00),
        ("CD_Barcelona", "Valencia", 250.50),
        ("CD_Barcelona", "Toulouse", 550.00),
        
        # Rutas desde "CD_Valencia"
        ("CD_Valencia", "Madrid", 260.00),
        ("CD_Valencia", "Barcelona", 220.00),
        ("CD_Valencia", "Murcia", 180.50),
        ("CD_Valencia", "Alicante", 120.00),
        
        # Rutas desde "CD_Sevilla"
        ("CD_Sevilla", "Madrid", 490.00),
        ("CD_Sevilla", "Málaga", 160.00),
        ("CD_Sevilla", "Lisboa", 450.00),
        ("CD_Sevilla", "Cádiz", 100.00),
        
        # Algunas rutas adicionales
        ("CD_Málaga", "Sevilla", 150.00),
        ("CD_Málaga", "Madrid", 580.00),
        ("CD_Bilbao", "Barcelona", 380.00),
        ("CD_Bilbao", "Zaragoza", 290.00),
        ("CD_Zaragoza", "Barcelona", 170.00),
        ("CD_Zaragoza", "Madrid", 310.00)
    ]


def crear_red_logistica_ejemplo() -> List[Tuple[str, str, float]]:
    """
    Crea una red logística con costos más variados para demostración
    """
    return [
        ("Puerto1", "AlmacenA", 1200.00),
        ("Puerto1", "AlmacenB", 850.00),
        ("Puerto1", "AlmacenC", 450.00),
        ("Puerto1", "AlmacenD", 320.00),
        ("Puerto2", "AlmacenA", 950.00),
        ("Puerto2", "AlmacenE", 780.00),
        ("AlmacenA", "Cliente1", 250.00),
        ("AlmacenA", "Cliente2", 380.00),
        ("AlmacenA", "Cliente3", 150.00),
        ("AlmacenB", "Cliente1", 320.00),
        ("AlmacenB", "Cliente4", 290.00),
        ("AlmacenB", "Cliente5", 410.00),
        ("AlmacenC", "Cliente2", 280.00),
        ("AlmacenC", "Cliente6", 220.00),
        ("AlmacenD", "Cliente3", 180.00),
        ("AlmacenD", "Cliente7", 350.00),
        ("AlmacenE", "Cliente4", 430.00),
        ("AlmacenE", "Cliente8", 560.00),
    ]


def demostracion_completa():
    """Demostración completa de todas las funcionalidades"""
    
    print("SISTEMA DE MATRIZ DE COSTOS DE TRANSBORDO")
    
    # Crear la matriz con datos de ejemplo
    matriz = MatrizCostosTransbordo()
    rutas = crear_red_distribucion_ejemplo()
    matriz.procesar_rutas(rutas)
    
    print(f"Red procesada: {len(rutas)} rutas cargadas")
    
    # Prueba 1: Consulta de ruta directa
    print("\n")
    print("PRUEBA 1: CONSULTA DE RUTA DIRECTA")
    
    # Consultar una ruta que existe
    matriz.mostrar_consulta("CD_Madrid", "Sevilla")
    
    # Consultar una ruta que no existe
    matriz.mostrar_consulta("CD_Madrid", "Lisboa")
    
    # Consultar con nodo que no existe
    matriz.mostrar_consulta("CD_Paris", "Madrid")
    
    # Prueba 2: Análisis detallado de un origen
    matriz.mostrar_analisis_origen("CD_Madrid")
    
    # Prueba 3: Comparación de orígenes
    print("\n")
    print("Prueba 3: COMPARACIÓN DE ORÍGENES")
    
    comparacion = matriz.comparar_origenes("CD_Madrid", "CD_Valencia")
    print(f"\nComparación entre {comparacion['origen1']} y {comparacion['origen2']}:")
    print(f"   • Rutas: {comparacion['comparacion']['total_rutas'][0]} vs {comparacion['comparacion']['total_rutas'][1]}")
    print(f"   • Costo total: ${comparacion['comparacion']['costo_total'][0]:,.2f} vs ${comparacion['comparacion']['costo_total'][1]:,.2f}")
    print(f"   • Costo promedio: ${comparacion['comparacion']['costo_promedio'][0]:,.2f} vs ${comparacion['comparacion']['costo_promedio'][1]:,.2f}")
    
    if comparacion['destinos_comunes']:
        print(f"   • Destinos comunes: {', '.join(comparacion['destinos_comunes'])}")
    
    if comparacion['destinos_exclusivos']['origen1']:
        print(f"   • Destinos exclusivos de {comparacion['origen1']}: {', '.join(comparacion['destinos_exclusivos']['origen1'])}")
    
    # Prueba 4: Resumen de la red

    matriz.mostrar_resumen_red()
    
    # Prueba 5: Trabajo con la red logística

    print("\n")
    print("Prueba 5: RED LOGÍSTICA COMPLEJA")
    
    matriz_logistica = MatrizCostosTransbordo()
    rutas_logisticas = crear_red_logistica_ejemplo()
    matriz_logistica.procesar_rutas(rutas_logisticas)
    
    # Mostrar análisis de un nodo importante
    matriz_logistica.mostrar_analisis_origen("Puerto1")
    
    # Consulta específica
    matriz_logistica.mostrar_consulta("AlmacenA", "Cliente3")
    
    # EJEMPLO 6: Uso avanzado - Filtrado por tipo

    print("\n")
    print("Prueba 6: RUTAS CRÍTICAS POR ORIGEN")
    
    for origen in ["CD_Madrid", "CD_Sevilla", "CD_Valencia"]:
        info = matriz.obtener_rutas_origen(origen)
        print(f"\n{origen}:")
        rutas_criticas = [
            (dest, data) for dest, data in info['rutas'].items() 
            if data['tipo'] == 'crítica'
        ]
        if rutas_criticas:
            for dest, data in rutas_criticas:
                print(f"{dest}: {data['porcentaje']:.1f}% (${data['costo']:,.2f})")
        else:
            print("   No hay rutas críticas (>50%)")


if __name__ == "__main__":
    demostracion_completa()
