"""Restricciones de Capacidad en Arcos

En optimización de redes, los arcos tienen capacidades máximas de carga. 
Modifica la estructura del grafo para que cada arista tenga un costo_unitario y una 
capacidad_maxima. Diseña un método que reciba un flujo propuesto:
    1. Si la ruta existe.
    2. Si viola la restricción de capacidad.
    3. El costo total del envío (Flujo x Costo Unitario).
"""

from typing import Dict, List, Tuple, Optional, Set, Any
from collections import defaultdict, deque
import math
from enum import Enum

class EstadoCapacidad(Enum):
    """Estados posibles de capacidad en una ruta"""
    DISPONIBLE = "disponible"           # Capacidad suficiente
    CAPACIDAD_EXCEDIDA = "capacidad_excedida"  # Excede la capacidad
    CAPACIDAD_LIMITE = "capacidad_limite"      # Está al límite
    RUTA_NO_EXISTE = "ruta_no_existe"

class RedCapacitada:
    """
    Red de transporte con capacidades máximas en arcos.
    
    Características:
    - Arcos con costo unitario y capacidad máxima
    - Verificación de flujo propuesto
    - Cálculo de costo total
    - Múltiples algoritmos de búsqueda de rutas
    - Análisis de capacidad residual
    """
    
    def __init__(self):
        """Inicializa la red capacitada"""
        # Estructura principal: origen -> {destino -> (costo_unitario, capacidad_max)}
        self.arcos: Dict[str, Dict[str, Tuple[float, float]]] = defaultdict(dict)
        
        # Capacidad utilizada actualmente (para seguimiento)
        self.capacidad_utilizada: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
        
        # Conjunto de nodos
        self.nodos: Set[str] = set()
        
        # Estadísticas
        self.total_arcos = 0
        self.capacidad_total = 0.0
        
        # Cache para búsquedas rápidas
        self.rutas_por_destino: Dict[str, List[Tuple[str, float, float]]] = defaultdict(list)
    
    def agregar_arco(self, origen: str, destino: str, 
                     costo_unitario: float, capacidad_max: float) -> None:
        """
        Agrega un arco con costo unitario y capacidad máxima
        
        Args:
            origen: Nodo origen
            destino: Nodo destino
            costo_unitario: Costo por unidad de flujo
            capacidad_max: Capacidad máxima del arco
        """
        # Validaciones
        if costo_unitario < 0:
            raise ValueError(f"El costo unitario no puede ser negativo: {costo_unitario}")
        if capacidad_max < 0:
            raise ValueError(f"La capacidad máxima no puede ser negativa: {capacidad_max}")
        if origen == destino:
            raise ValueError("Origen y destino no pueden ser el mismo nodo")
        
        # Agregar arco
        self.arcos[origen][destino] = (costo_unitario, capacidad_max)
        
        # Actualizar nodos
        self.nodos.add(origen)
        self.nodos.add(destino)
        
        # Actualizar estadísticas
        self.total_arcos += 1
        self.capacidad_total += capacidad_max
        
        # Actualizar índice inverso
        self.rutas_por_destino[destino].append((origen, costo_unitario, capacidad_max))
    
    def agregar_arco_bidireccional(self, nodo1: str, nodo2: str, 
                                   costo_unitario: float, capacidad_max: float) -> None:
        """
        Agrega un arco bidireccional (dos arcos dirigidos)
        """
        self.agregar_arco(nodo1, nodo2, costo_unitario, capacidad_max)
        self.agregar_arco(nodo2, nodo1, costo_unitario, capacidad_max)
    
    def verificar_flujo(self, origen: str, destino: str, flujo: float) -> Dict:
        """
        Verifica si se puede enviar un flujo de origen a destino
        
        Args:
            origen: Nodo origen
            destino: Nodo destino
            flujo: Cantidad de flujo a enviar
            
        Returns:
            Dict con información detallada de la verificación
        """
        # Validar que el flujo sea positivo
        if flujo <= 0:
            raise ValueError(f"El flujo debe ser positivo: {flujo}")
        
        # Verificar que los nodos existan
        if origen not in self.nodos:
            return {
                'exitoso': False,
                'estado': EstadoCapacidad.RUTA_NO_EXISTE,
                'mensaje': f"El nodo origen '{origen}' no existe en la red",
                'ruta': None,
                'costo_total': None,
                'capacidades': None
            }
        
        if destino not in self.nodos:
            return {
                'exitoso': False,
                'estado': EstadoCapacidad.RUTA_NO_EXISTE,
                'mensaje': f"El nodo destino '{destino}' no existe en la red",
                'ruta': None,
                'costo_total': None,
                'capacidades': None
            }
        
        # Verificar si existe ruta directa
        if destino in self.arcos.get(origen, {}):
            return self._verificar_flujo_directo(origen, destino, flujo)
        
        # Buscar ruta con múltiples saltos (algoritmo de búsqueda)
        ruta = self._encontrar_ruta(origen, destino)
        
        if not ruta:
            return {
                'exitoso': False,
                'estado': EstadoCapacidad.RUTA_NO_EXISTE,
                'mensaje': f"No existe ruta de '{origen}' a '{destino}' en la red",
                'ruta': None,
                'costo_total': None,
                'capacidades': None
            }
        
        return self._verificar_flujo_ruta(ruta, flujo)
    
    def _verificar_flujo_directo(self, origen: str, destino: str, flujo: float) -> Dict:
        """Verifica flujo en una ruta directa"""
        costo_unitario, capacidad_max = self.arcos[origen][destino]
        capacidad_disponible = capacidad_max - self.capacidad_utilizada[origen][destino]
        
        # Verificar capacidad
        if flujo > capacidad_disponible:
            return {
                'exitoso': False,
                'estado': EstadoCapacidad.CAPACIDAD_EXCEDIDA,
                'mensaje': f"El flujo de {flujo} excede la capacidad disponible ({capacidad_disponible:.2f})",
                'ruta': [origen, destino],
                'costo_total': flujo * costo_unitario,
                'capacidades': {
                    'capacidad_max': capacidad_max,
                    'capacidad_utilizada': self.capacidad_utilizada[origen][destino],
                    'capacidad_disponible': capacidad_disponible,
                    'flujo_solicitado': flujo,
                    'excede_por': flujo - capacidad_disponible
                },
                'costo_unitario': costo_unitario,
                'estado_capacidad': EstadoCapacidad.CAPACIDAD_EXCEDIDA
            }
        
        # Verificar si está al límite
        estado = EstadoCapacidad.CAPACIDAD_LIMITE if abs(flujo - capacidad_disponible) < 0.001 else EstadoCapacidad.DISPONIBLE
        
        return {
            'exitoso': True,
            'estado': estado,
            'mensaje': f"Flujo de {flujo} puede enviarse de '{origen}' a '{destino}'",
            'ruta': [origen, destino],
            'costo_total': flujo * costo_unitario,
            'capacidades': {
                'capacidad_max': capacidad_max,
                'capacidad_utilizada': self.capacidad_utilizada[origen][destino],
                'capacidad_disponible': capacidad_disponible,
                'flujo_solicitado': flujo,
                'porcentaje_uso': (flujo / capacidad_max * 100) if capacidad_max > 0 else 0
            },
            'costo_unitario': costo_unitario,
            'estado_capacidad': estado
        }
    
    def _verificar_flujo_ruta(self, ruta: List[str], flujo: float) -> Dict:
        """Verifica flujo a través de una ruta con múltiples arcos"""
        # Verificar capacidad en cada arco de la ruta
        capacidades_arcos = []
        costo_total = 0
        capacidad_minima = float('inf')
        arco_critico = None
        
        for i in range(len(ruta) - 1):
            origen = ruta[i]
            destino = ruta[i + 1]
            
            if destino not in self.arcos.get(origen, {}):
                return {
                    'exitoso': False,
                    'estado': EstadoCapacidad.RUTA_NO_EXISTE,
                    'mensaje': f"El arco '{origen}->{destino}' no existe en la ruta",
                    'ruta': ruta,
                    'costo_total': None,
                    'capacidades': None
                }
            
            costo_unitario, capacidad_max = self.arcos[origen][destino]
            capacidad_disponible = capacidad_max - self.capacidad_utilizada[origen][destino]
            
            # Verificar capacidad en este arco
            if flujo > capacidad_disponible:
                return {
                    'exitoso': False,
                    'estado': EstadoCapacidad.CAPACIDAD_EXCEDIDA,
                    'mensaje': f"Flujo excede capacidad en arco '{origen}->{destino}': "
                              f"{flujo} > {capacidad_disponible:.2f} disponible",
                    'ruta': ruta,
                    'costo_total': flujo * costo_unitario,
                    'capacidades': {
                        'arco_critico': (origen, destino),
                        'capacidad_max': capacidad_max,
                        'capacidad_utilizada': self.capacidad_utilizada[origen][destino],
                        'capacidad_disponible': capacidad_disponible,
                        'flujo_solicitado': flujo,
                        'excede_por': flujo - capacidad_disponible
                    },
                    'costo_unitario': costo_unitario,
                    'estado_capacidad': EstadoCapacidad.CAPACIDAD_EXCEDIDA
                }
            
            # Acumular costo
            costo_total += flujo * costo_unitario
            
            # Guardar información del arco
            capacidades_arcos.append({
                'origen': origen,
                'destino': destino,
                'costo_unitario': costo_unitario,
                'capacidad_max': capacidad_max,
                'capacidad_utilizada': self.capacidad_utilizada[origen][destino],
                'capacidad_disponible': capacidad_disponible,
                'porcentaje_uso': (flujo / capacidad_max * 100) if capacidad_max > 0 else 0
            })
            
            # Actualizar capacidad mínima
            if capacidad_disponible < capacidad_minima:
                capacidad_minima = capacidad_disponible
                arco_critico = (origen, destino)
        
        # Determinar estado general
        estado = EstadoCapacidad.DISPONIBLE
        if abs(flujo - capacidad_minima) < 0.001:
            estado = EstadoCapacidad.CAPACIDAD_LIMITE
        
        return {
            'exitoso': True,
            'estado': estado,
            'mensaje': f"Flujo de {flujo} puede enviarse a través de {len(ruta)-1} arcos",
            'ruta': ruta,
            'costo_total': costo_total,
            'capacidades': {
                'arcos': capacidades_arcos,
                'capacidad_minima': capacidad_minima,
                'arco_critico': arco_critico,
                'flujo_solicitado': flujo
            },
            'estado_capacidad': estado
        }
    
    def _encontrar_ruta(self, origen: str, destino: str) -> Optional[List[str]]:
        """
        Encuentra una ruta de origen a destino usando BFS
        
        Returns:
            Lista de nodos en la ruta o None si no existe
        """
        if origen == destino:
            return [origen]
        
        visited = {origen}
        queue = deque([(origen, [origen])])
        
        while queue:
            node, path = queue.popleft()
            
            for vecino in self.arcos.get(node, {}):
                if vecino not in visited:
                    if vecino == destino:
                        return path + [vecino]
                    visited.add(vecino)
                    queue.append((vecino, path + [vecino]))
        
        return None
    
    def _encontrar_ruta_min_costo(self, origen: str, destino: str) -> Optional[List[str]]:
        """
        Encuentra la ruta de mínimo costo usando Dijkstra
        
        Returns:
            Lista de nodos en la ruta o None si no existe
        """
        if origen == destino:
            return [origen]
        
        # Distancias y predecesores
        dist = {nodo: float('inf') for nodo in self.nodos}
        prev = {nodo: None for nodo in self.nodos}
        dist[origen] = 0
        
        # Cola de prioridad
        pq = [(0, origen)]
        visited = set()
        
        while pq:
            d, u = pq.pop(0)  # Simple implementación, usar heap para mejor performance
            
            if u in visited:
                continue
            visited.add(u)
            
            if u == destino:
                break
            
            for v, (costo, _) in self.arcos.get(u, {}).items():
                if v in visited:
                    continue
                
                # Verificar capacidad disponible
                capacidad_disponible = self.arcos[u][v][1] - self.capacidad_utilizada[u][v]
                if capacidad_disponible <= 0:
                    continue
                
                nueva_dist = d + costo
                if nueva_dist < dist[v]:
                    dist[v] = nueva_dist
                    prev[v] = u
                    pq.append((nueva_dist, v))
                    pq.sort(key=lambda x: x[0])
        
        # Reconstruir ruta
        if prev[destino] is None and origen != destino:
            return None
        
        ruta = []
        actual = destino
        while actual is not None:
            ruta.insert(0, actual)
            actual = prev[actual]
        
        return ruta
    
    def enviar_flujo(self, origen: str, destino: str, flujo: float) -> Dict:
        """
        Envía un flujo a través de la red (actualiza capacidades utilizadas)
        
        Args:
            origen: Nodo origen
            destino: Nodo destino
            flujo: Cantidad a enviar
            
        Returns:
            Dict con resultado del envío
        """
        # Primero verificar si es posible
        verificacion = self.verificar_flujo(origen, destino, flujo)
        
        if not verificacion['exitoso']:
            return {
                'exitoso': False,
                'mensaje': f"No se pudo enviar el flujo: {verificacion['mensaje']}",
                'verificacion': verificacion
            }
        
        # Actualizar capacidades utilizadas
        ruta = verificacion['ruta']
        for i in range(len(ruta) - 1):
            o = ruta[i]
            d = ruta[i + 1]
            self.capacidad_utilizada[o][d] += flujo
        
        return {
            'exitoso': True,
            'mensaje': f" Flujo de {flujo} enviado exitosamente de '{origen}' a '{destino}'",
            'flujo_enviado': flujo,
            'ruta': ruta,
            'costo_total': verificacion['costo_total'],
            'verificacion': verificacion
        }
    
    def capacidad_residual(self, origen: str, destino: str) -> float:
        """
        Calcula la capacidad residual en un arco específico
        """
        if origen not in self.arcos:
            return 0.0
        if destino not in self.arcos[origen]:
            return 0.0
        
        capacidad_max = self.arcos[origen][destino][1]
        utilizada = self.capacidad_utilizada[origen][destino]
        return capacidad_max - utilizada
    
    def flujo_maximo_posible(self, origen: str, destino: str) -> float:
        """
        Calcula el flujo máximo posible entre dos nodos
        (considerando todas las rutas y capacidades)
        """
        if origen not in self.nodos or destino not in self.nodos:
            return 0.0
        
        # Si hay ruta directa
        if destino in self.arcos.get(origen, {}):
            return self.capacidad_residual(origen, destino)
        
        # Encontrar todas las rutas posibles (simplificado)
        flujo_total = 0.0
        rutas = self._encontrar_todas_rutas(origen, destino)
        
        for ruta in rutas:
            # Encontrar capacidad mínima en la ruta
            cap_min = float('inf')
            for i in range(len(ruta) - 1):
                o = ruta[i]
                d = ruta[i + 1]
                cap_res = self.capacidad_residual(o, d)
                cap_min = min(cap_min, cap_res)
            
            if cap_min > 0:
                flujo_total += cap_min
        
        return flujo_total
    
    def _encontrar_todas_rutas(self, origen: str, destino: str, 
                               ruta_actual: Optional[List[str]] = None) -> List[List[str]]:
        """Encuentra todas las rutas simples entre origen y destino"""
        if ruta_actual is None:
            ruta_actual = [origen]
        
        if origen == destino:
            return [ruta_actual]
        
        rutas = []
        for vecino in self.arcos.get(origen, {}):
            if vecino not in ruta_actual:
                # Verificar capacidad disponible
                if self.capacidad_residual(origen, vecino) <= 0:
                    continue
                nuevas_rutas = self._encontrar_todas_rutas(vecino, destino, ruta_actual + [vecino])
                rutas.extend(nuevas_rutas)
        
        return rutas
    
    def mostrar_verificacion(self, origen: str, destino: str, flujo: float) -> None:
        """
        Muestra de forma formateada la verificación de un flujo
        """
        print(f"\n")
        print(f"VERIFICACIÓN DE FLUJO: {origen} → {destino}")
        print(f"   Flujo solicitado: {flujo} toneladas")
        print(f"{'='*80}")
        
        resultado = self.verificar_flujo(origen, destino, flujo)
        
        if not resultado['exitoso']:
            print(f"{resultado['mensaje']}")
            if resultado['ruta']:
                print(f"   Ruta: {' → '.join(resultado['ruta'])}")
            return
        
        print(f"{resultado['mensaje']}")
        print(f"\nDETALLES DEL FLUJO:")
        print(f"   • Costo total: ${resultado['costo_total']:,.2f}")
        
        if len(resultado['ruta']) == 2:
            # Ruta directa
            caps = resultado['capacidades']
            print(f"   • Capacidad máxima: {caps['capacidad_max']:.2f}")
            print(f"   • Capacidad utilizada: {caps['capacidad_utilizada']:.2f}")
            print(f"   • Capacidad disponible: {caps['capacidad_disponible']:.2f}")
            print(f"   • Uso: {caps['porcentaje_uso']:.1f}%")
        else:
            # Ruta múltiple
            print(f"\nRUTA DETALLADA:")
            for arco in resultado['capacidades']['arcos']:
                print(f"   • {arco['origen']} → {arco['destino']}: "
                      f"costo ${arco['costo_unitario']:.2f}/ton, "
                      f"cap. {arco['capacidad_max']:.2f}, "
                      f"uso {arco['porcentaje_uso']:.1f}%")
            
            caps = resultado['capacidades']
            print(f"\nARCO CRÍTICO: {caps['arco_critico'][0]} → {caps['arco_critico'][1]}")
            print(f"   Capacidad mínima: {caps['capacidad_minima']:.2f}")
        
        estado = resultado['estado_capacidad']
        if estado == EstadoCapacidad.DISPONIBLE:
            print(f"\nESTADO: Disponible - Flujo puede enviarse sin problemas")
        elif estado == EstadoCapacidad.CAPACIDAD_LIMITE:
            print(f"\nESTADO: Límite - Flujo está al límite de capacidad")
        elif estado == EstadoCapacidad.CAPACIDAD_EXCEDIDA:
            print(f"\nESTADO: Excedido - Flujo supera la capacidad disponible")
        
        print(f"\n")


# Pruebas:

def crear_red_logistica_ejemplo() -> RedCapacitada:
    """
    Crea una red logística con capacidades para demostración
    """
    red = RedCapacitada()
    
    # Agregar arcos dirigidos (origen, destino, costo_unitario, capacidad_max)
    arcos = [
        # Desde Planta A
        ("PlantaA", "CD1", 2.50, 100.0),
        ("PlantaA", "CD2", 3.00, 80.0),
        ("PlantaA", "CD3", 4.00, 60.0),
        
        # Desde Planta B
        ("PlantaB", "CD1", 3.50, 90.0),
        ("PlantaB", "CD2", 2.80, 70.0),
        ("PlantaB", "CD3", 3.20, 50.0),
        
        # Desde CD1
        ("CD1", "Cliente1", 1.50, 150.0),
        ("CD1", "Cliente2", 2.00, 100.0),
        ("CD1", "Cliente3", 1.80, 80.0),
        
        # Desde CD2
        ("CD2", "Cliente1", 2.20, 120.0),
        ("CD2", "Cliente2", 1.50, 90.0),
        ("CD2", "Cliente4", 2.50, 70.0),
        
        # Desde CD3
        ("CD3", "Cliente3", 1.20, 100.0),
        ("CD3", "Cliente4", 1.80, 85.0),
        ("CD3", "Cliente5", 2.00, 60.0),
        
        # Conexiones adicionales
        ("CD1", "CD4", 0.80, 200.0),
        ("CD2", "CD4", 1.00, 180.0),
        ("CD4", "Cliente5", 1.20, 150.0),
        ("CD4", "Cliente6", 1.50, 120.0),
    ]
    
    for origen, destino, costo, capacidad in arcos:
        red.agregar_arco(origen, destino, costo, capacidad)
    
    return red


def crear_red_compleja() -> RedCapacitada:
    """
    Crea una red más compleja con múltiples nodos intermedios
    """
    red = RedCapacitada()
    
    # Nodos: Puertos, Almacenes, Centros de distribución, Clientes
    nodos = ["P1", "P2", "A1", "A2", "A3", "CD1", "CD2", "CD3", 
             "C1", "C2", "C3", "C4", "C5", "C6"]
    
    for nodo in nodos:
        # Los nodos se crean automáticamente al agregar arcos
        pass
    
    # Arcos con diferentes capacidades y costos
    arcos = [
        ("P1", "A1", 5.0, 500.0),
        ("P1", "A2", 4.5, 400.0),
        ("P2", "A2", 6.0, 300.0),
        ("P2", "A3", 5.5, 350.0),
        ("A1", "CD1", 2.0, 300.0),
        ("A1", "CD2", 2.5, 250.0),
        ("A2", "CD1", 1.8, 350.0),
        ("A2", "CD3", 2.2, 280.0),
        ("A3", "CD2", 1.5, 320.0),
        ("A3", "CD3", 2.0, 290.0),
        ("CD1", "C1", 1.0, 200.0),
        ("CD1", "C2", 1.2, 180.0),
        ("CD1", "C3", 1.5, 150.0),
        ("CD2", "C2", 1.0, 160.0),
        ("CD2", "C4", 1.3, 140.0),
        ("CD2", "C5", 1.8, 120.0),
        ("CD3", "C3", 0.8, 170.0),
        ("CD3", "C5", 1.2, 130.0),
        ("CD3", "C6", 1.5, 110.0),
    ]
    
    for origen, destino, costo, capacidad in arcos:
        red.agregar_arco(origen, destino, costo, capacidad)
    
    return red


def demostracion_completa():
    """Demostración completa de todas las funcionalidades"""
    
    print("SISTEMA DE RESTRICCIONES DE CAPACIDAD EN ARCOS")
    
    # Crear red de ejemplo
    red = crear_red_logistica_ejemplo()
    
    # Prueba 1: Flujo directo - Capacidad suficiente
    print("\n")
    print("Prueba 1: FLUJO DIRECTO - CAPACIDAD SUFICIENTE")

    red.mostrar_verificacion("PlantaA", "CD1", 50.0)
    
    # Prueba 2: Flujo directo - Excede capacidad
    print("\n")
    print("Prueba 2: FLUJO DIRECTO - EXCEDE CAPACIDAD")

    red.mostrar_verificacion("PlantaA", "CD1", 120.0)

    # Prueba 3: Flujo directo - Capacidad límite
    #
    print("\n")
    print("Prueba 3: FLUJO DIRECTO - CAPACIDAD LÍMITE")

    red.mostrar_verificacion("PlantaA", "CD1", 99.5)
    
    # Prueba 4: Ruta con múltiples saltos

    print("\n")
    print("Prueba 4: RUTA CON MÚLTIPLES SALTOS")

    red.mostrar_verificacion("PlantaA", "Cliente1", 45.0)
    
    # EJEMPLO 5: Envío de flujo (actualiza capacidades)

    print("\n")
    print("Prueba 5: ENVÍO DE FLUJO Y ACTUALIZACIÓN")

    
    # Enviar flujo
    resultado_envio = red.enviar_flujo("PlantaA", "CD1", 60.0)
    if resultado_envio['exitoso']:
        print(f"{resultado_envio['mensaje']}")
        print(f"   Costo total: ${resultado_envio['costo_total']:,.2f}")
    
    # Verificar nuevamente después del envío
    print("\nVERIFICACIÓN DESPUÉS DEL ENVÍO:")
    red.mostrar_verificacion("PlantaA", "CD1", 40.0)
    
    # Prueba 6: Flujo máximo posible

    print("\n")
    print("Prueba 6: FLUJO MÁXIMO POSIBLE")

    
    flujo_max = red.flujo_maximo_posible("PlantaA", "Cliente1")
    print(f"Flujo máximo posible de 'PlantaA' a 'Cliente1': {flujo_max:.2f} toneladas")
    
    # Prueba 7: Red compleja
    
    print("\n")
    print("Prueba 7: RED COMPLEJA CON MÚLTIPLES RUTAS")
    
    red_compleja = crear_red_compleja()
    
    # Verificar flujo a través de red compleja
    red_compleja.mostrar_verificacion("P1", "C1", 150.0)
    red_compleja.mostrar_verificacion("P2", "C6", 100.0)
    
    # Prueba 8: Capacidad residual

    print("\n")
    print("Prueba 8: CAPACIDAD RESIDUAL")

    
    arcos_para_revisar = [
        ("PlantaA", "CD1"),
        ("PlantaA", "CD2"),
        ("CD1", "Cliente1")
    ]
    
    print("Capacidades residuales:")
    for origen, destino in arcos_para_revisar:
        residual = red.capacidad_residual(origen, destino)
        if residual > 0:
            print(f"   • {origen} → {destino}: {residual:.2f} toneladas disponibles")
        else:
            print(f"   • {origen} → {destino}: CAPACIDAD COMPLETA")


# Funciones adicionales

def simular_envios(red: RedCapacitada, envios: List[Tuple[str, str, float]]) -> None:
    """
    Simula una serie de envíos a través de la red
    """
    print("\n")
    print("SIMULACIÓN DE ENVÍOS")
    
    for i, (origen, destino, flujo) in enumerate(envios, 1):
        print(f"\n Envío #{i}: {origen} → {destino} ({flujo} toneladas)")
        
        resultado = red.enviar_flujo(origen, destino, flujo)
        
        if resultado['exitoso']:
            print(f"Envío exitoso")
            print(f"Costo: ${resultado['costo_total']:,.2f}")
            print(f"Ruta: {' → '.join(resultado['ruta'])}")
        else:
            print(f"Envío fallido: {resultado['mensaje']}")


if __name__ == "__main__":
    demostracion_completa()
    
    # Demostración adicional de simulación
    print("\n")
    print("SIMULACIÓN DE ENVÍOS SECUENCIALES")
    
    red_sim = crear_red_logistica_ejemplo()
    
    envios = [
        ("PlantaA", "CD1", 30.0),
        ("PlantaA", "CD1", 40.0),
        ("PlantaA", "CD1", 35.0),  # Este debería fallar por capacidad
        ("PlantaB", "CD2", 50.0),
        ("PlantaA", "Cliente1", 25.0),
    ]
    
    simular_envios(red_sim, envios)
