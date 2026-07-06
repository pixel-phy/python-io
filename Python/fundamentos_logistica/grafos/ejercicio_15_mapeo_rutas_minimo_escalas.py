"""Ejercicio 15: Mapeo de Rutas con Mínimo de Escalas

Un operador logístico de carga aérea necesita enviar un contenedor desde un Hub Origen
hasta un Hub Destino. Dado que el costo de aterrizaje y despegue es fijo por aeropuerto,
se busca la ruta que haga el menor número de escalas posibles. Modifica el BFS para que 
devuelva no solo los nodos visitados, sino la lista exacta de paradas (camino) desde el origen
hasta el destino con menos saltos. """

from typing import Dict, List, Set, Tuple, Optional, Deque
from collections import deque, defaultdict
from dataclasses import dataclass
from enum import Enum
import json

class TipoAeropuerto(Enum):
    """Clasificación de aeropuertos según su función"""
    HUB_PRINCIPAL = "hub_principal"
    HUB_SECUNDARIO = "hub_secundario"
    AEROPUERTO_REGIONAL = "aeropuerto_regional"
    AEROPUERTO_INTERNACIONAL = "aeropuerto_internacional"

@dataclass
class AeropuertoInfo:
    """Información detallada de un aeropuerto"""
    nombre: str
    tipo: TipoAeropuerto
    ciudad: str
    pais: str
    capacidad: float = 0.0
    tiempo_escala_minimo: int = 45  # minutos mínimos para escala

@dataclass
class RutaEncontrada:
    """Representa una ruta encontrada con sus detalles"""
    ruta: List[str]
    num_escalas: int
    num_saltos: int
    aeropuertos_intermedios: List[str]
    tiempo_total_estimado: int  # minutos
    descripcion: str

class RedAeroportuaria:
    """
    Red de aeropuertos para encontrar rutas con mínimo de escalas.
    
    Características:
    - BFS para encontrar ruta con menos saltos
    - Registro de camino completo
    - Información detallada de aeropuertos
    - Múltiples métricas de optimización
    - Soporte para restricciones adicionales
    """
    
    def __init__(self):
        """Inicializa la red aeroportuaria"""
        # Lista de adyacencia: aeropuerto -> [aeropuertos_vecinos]
        self.adyacencia: Dict[str, Set[str]] = defaultdict(set)
        
        # Información detallada de aeropuertos
        self.aeropuertos_info: Dict[str, AeropuertoInfo] = {}
        
        # Distancias geográficas (para cálculos adicionales)
        self.distancias: Dict[Tuple[str, str], float] = {}
        
        # Tiempos de vuelo estimados (minutos)
        self.tiempos_vuelo: Dict[Tuple[str, str], int] = {}
        
        # Estadísticas de la red
        self.total_aeropuertos = 0
        self.total_conexiones = 0
        
        # Cache de rutas encontradas
        self.cache_rutas: Dict[Tuple[str, str], RutaEncontrada] = {}
    
    def agregar_aeropuerto(self, nombre: str, tipo: TipoAeropuerto = TipoAeropuerto.AEROPUERTO_REGIONAL,
                          ciudad: str = "", pais: str = "", capacidad: float = 0.0) -> None:
        """
        Agrega un aeropuerto a la red
        
        Args:
            nombre: Código/nombre del aeropuerto
            tipo: Clasificación del aeropuerto
            ciudad: Ciudad donde se encuentra
            pais: País del aeropuerto
            capacidad: Capacidad de operación
        """
        if nombre in self.aeropuertos_info:
            raise ValueError(f"El aeropuerto '{nombre}' ya existe en la red")
        
        self.aeropuertos_info[nombre] = AeropuertoInfo(
            nombre=nombre,
            tipo=tipo,
            ciudad=ciudad,
            pais=pais,
            capacidad=capacidad
        )
        self.total_aeropuertos += 1
    
    def agregar_conexion(self, aeropuerto1: str, aeropuerto2: str, 
                        distancia: float = 0.0, tiempo_vuelo: int = 0) -> None:
        """
        Agrega una conexión bidireccional entre dos aeropuertos
        
        Args:
            aeropuerto1: Primer aeropuerto
            aeropuerto2: Segundo aeropuerto
            distancia: Distancia en kilómetros
            tiempo_vuelo: Tiempo de vuelo en minutos
        """
        if aeropuerto1 not in self.aeropuertos_info:
            raise ValueError(f"El aeropuerto '{aeropuerto1}' no existe")
        if aeropuerto2 not in self.aeropuertos_info:
            raise ValueError(f"El aeropuerto '{aeropuerto2}' no existe")
        if aeropuerto1 == aeropuerto2:
            raise ValueError("No se puede conectar un aeropuerto consigo mismo")
        
        # Agregar conexión bidireccional
        self.adyacencia[aeropuerto1].add(aeropuerto2)
        self.adyacencia[aeropuerto2].add(aeropuerto1)
        
        # Guardar distancia y tiempo
        if distancia > 0:
            self.distancias[(aeropuerto1, aeropuerto2)] = distancia
            self.distancias[(aeropuerto2, aeropuerto1)] = distancia
        
        if tiempo_vuelo > 0:
            self.tiempos_vuelo[(aeropuerto1, aeropuerto2)] = tiempo_vuelo
            self.tiempos_vuelo[(aeropuerto2, aeropuerto1)] = tiempo_vuelo
        
        self.total_conexiones += 1
    
    def encontrar_ruta_min_escalas(self, origen: str, destino: str) -> Optional[RutaEncontrada]:
        """
        Encuentra la ruta con el mínimo número de escalas usando BFS
        
        Args:
            origen: Aeropuerto de origen
            destino: Aeropuerto de destino
            
        Returns:
            RutaEncontrada o None si no existe ruta
        """
        # Validar que los aeropuertos existan
        if origen not in self.aeropuertos_info:
            raise ValueError(f"El aeropuerto origen '{origen}' no existe")
        if destino not in self.aeropuertos_info:
            raise ValueError(f"El aeropuerto destino '{destino}' no existe")
        
        # Verificar cache
        if (origen, destino) in self.cache_rutas:
            return self.cache_rutas[(origen, destino)]
        
        # Si origen y destino son el mismo
        if origen == destino:
            ruta = RutaEncontrada(
                ruta=[origen],
                num_escalas=0,
                num_saltos=0,
                aeropuertos_intermedios=[],
                tiempo_total_estimado=0,
                descripcion="Origen y destino son el mismo aeropuerto"
            )
            self.cache_rutas[(origen, destino)] = ruta
            return ruta
        
        # BFS para encontrar la ruta más corta en número de saltos
        cola: Deque[Tuple[str, List[str]]] = deque()
        cola.append((origen, [origen]))
        visitados: Set[str] = {origen}
        
        # Para rastrear el nivel de profundidad
        niveles: Dict[str, int] = {origen: 0}
        
        # Para rastrear el padre de cada nodo (para reconstruir camino)
        padres: Dict[str, str] = {}
        
        while cola:
            aeropuerto_actual, camino_actual = cola.popleft()
            nivel_actual = niveles[aeropuerto_actual]
            
            # Explorar vecinos
            for vecino in self.adyacencia.get(aeropuerto_actual, set()):
                if vecino not in visitados:
                    visitados.add(vecino)
                    padres[vecino] = aeropuerto_actual
                    niveles[vecino] = nivel_actual + 1
                    nuevo_camino = camino_actual + [vecino]
                    
                    # Si encontramos el destino, retornamos la ruta
                    if vecino == destino:
                        # Calcular estadísticas de la ruta
                        num_saltos = len(nuevo_camino) - 1
                        num_escalas = max(0, num_saltos - 1)  # Escalas = saltos - 1
                        aeropuertos_intermedios = nuevo_camino[1:-1] if len(nuevo_camino) > 2 else []
                        
                        # Calcular tiempo total estimado
                        tiempo_total = self._calcular_tiempo_total(nuevo_camino)
                        
                        # Generar descripción
                        descripcion = self._generar_descripcion_ruta(nuevo_camino, num_escalas)
                        
                        ruta = RutaEncontrada(
                            ruta=nuevo_camino,
                            num_escalas=num_escalas,
                            num_saltos=num_saltos,
                            aeropuertos_intermedios=aeropuertos_intermedios,
                            tiempo_total_estimado=tiempo_total,
                            descripcion=descripcion
                        )
                        
                        # Guardar en cache
                        self.cache_rutas[(origen, destino)] = ruta
                        return ruta
                    
                    cola.append((vecino, nuevo_camino))
        
        # No se encontró ruta
        return None
    
    def _calcular_tiempo_total(self, ruta: List[str]) -> int:
        """
        Calcula el tiempo total estimado para una ruta
        Incluye tiempo de vuelo + tiempo de escala
        """
        if len(ruta) < 2:
            return 0
        
        tiempo_total = 0
        
        # Tiempo de vuelo entre aeropuertos
        for i in range(len(ruta) - 1):
            tiempo_vuelo = self.tiempos_vuelo.get((ruta[i], ruta[i+1]), 60)  # 60 min por defecto
            tiempo_total += tiempo_vuelo
        
        # Tiempo de escala en aeropuertos intermedios
        for i in range(1, len(ruta) - 1):
            aeropuerto = ruta[i]
            tiempo_escala = self.aeropuertos_info[aeropuerto].tiempo_escala_minimo
            tiempo_total += tiempo_escala
        
        return tiempo_total
    
    def _generar_descripcion_ruta(self, ruta: List[str], num_escalas: int) -> str:
        """Genera una descripción legible de la ruta"""
        if len(ruta) == 1:
            return "Origen y destino son el mismo aeropuerto"
        
        if num_escalas == 0:
            return f"Vuelo directo de {ruta[0]} a {ruta[-1]}"
        
        descripcion = f"Ruta con {num_escalas} escala(s): {ruta[0]}"
        for i in range(1, len(ruta) - 1):
            descripcion += f" → {ruta[i]} (escala)"
        descripcion += f" → {ruta[-1]}"
        
        return descripcion
    
    def encontrar_todas_rutas_min_escalas(self, origen: str, destino: str) -> List[RutaEncontrada]:
        """
        Encuentra TODAS las rutas con el mínimo número de escalas
        
        Args:
            origen: Aeropuerto de origen
            destino: Aeropuerto de destino
            
        Returns:
            Lista de todas las rutas con el mínimo de escalas
        """
        if origen not in self.aeropuertos_info or destino not in self.aeropuertos_info:
            return []
        
        if origen == destino:
            return [RutaEncontrada(
                ruta=[origen],
                num_escalas=0,
                num_saltos=0,
                aeropuertos_intermedios=[],
                tiempo_total_estimado=0,
                descripcion="Origen y destino son el mismo aeropuerto"
            )]
        
        # BFS para encontrar todas las rutas más cortas
        cola: Deque[Tuple[str, List[str]]] = deque()
        cola.append((origen, [origen]))
        visitados: Dict[str, int] = {origen: 0}  # aeropuerto -> nivel
        rutas_encontradas: List[List[str]] = []
        nivel_destino = None
        
        while cola:
            aeropuerto_actual, camino_actual = cola.popleft()
            nivel_actual = len(camino_actual) - 1
            
            # Si ya superamos el nivel del destino, no continuamos
            if nivel_destino is not None and nivel_actual > nivel_destino:
                continue
            
            for vecino in self.adyacencia.get(aeropuerto_actual, set()):
                nuevo_nivel = nivel_actual + 1
                
                # Si encontramos el destino en este nivel
                if vecino == destino:
                    if nivel_destino is None:
                        nivel_destino = nuevo_nivel
                    
                    if nuevo_nivel == nivel_destino:
                        ruta_completa = camino_actual + [vecino]
                        rutas_encontradas.append(ruta_completa)
                    continue
                
                # Si el vecino no ha sido visitado en este nivel o menor
                if vecino not in visitados or visitados[vecino] >= nuevo_nivel:
                    visitados[vecino] = nuevo_nivel
                    cola.append((vecino, camino_actual + [vecino]))
        
        # Convertir a objetos RutaEncontrada
        resultados = []
        for ruta in rutas_encontradas:
            num_saltos = len(ruta) - 1
            num_escalas = max(0, num_saltos - 1)
            resultados.append(RutaEncontrada(
                ruta=ruta,
                num_escalas=num_escalas,
                num_saltos=num_saltos,
                aeropuertos_intermedios=ruta[1:-1] if len(ruta) > 2 else [],
                tiempo_total_estimado=self._calcular_tiempo_total(ruta),
                descripcion=self._generar_descripcion_ruta(ruta, num_escalas)
            ))
        
        return resultados
    
    def encontrar_ruta_con_restricciones(self, origen: str, destino: str,
                                         max_escalas: Optional[int] = None,
                                         aeropuertos_prohibidos: Optional[Set[str]] = None,
                                         aeropuertos_requeridos: Optional[Set[str]] = None) -> Optional[RutaEncontrada]:
        """
        Encuentra la mejor ruta con restricciones adicionales
        
        Args:
            origen: Aeropuerto de origen
            destino: Aeropuerto de destino
            max_escalas: Número máximo de escalas permitido
            aeropuertos_prohibidos: Aeropuertos que no se pueden usar
            aeropuertos_requeridos: Aeropuertos que deben incluirse en la ruta
            
        Returns:
            RutaEncontrada o None si no existe
        """
        if origen not in self.aeropuertos_info or destino not in self.aeropuertos_info:
            return None
        
        # BFS con restricciones
        cola: Deque[Tuple[str, List[str]]] = deque()
        cola.append((origen, [origen]))
        visitados: Set[str] = {origen}
        
        while cola:
            aeropuerto_actual, camino_actual = cola.popleft()
            
            # Verificar límite de escalas
            if max_escalas is not None and len(camino_actual) - 2 > max_escalas:
                continue
            
            for vecino in self.adyacencia.get(aeropuerto_actual, set()):
                # Verificar aeropuertos prohibidos
                if aeropuertos_prohibidos and vecino in aeropuertos_prohibidos:
                    continue
                
                if vecino not in visitados:
                    visitados.add(vecino)
                    nuevo_camino = camino_actual + [vecino]
                    
                    if vecino == destino:
                        # Verificar que todos los aeropuertos requeridos estén en la ruta
                        if aeropuertos_requeridos:
                            if not all(req in nuevo_camino for req in aeropuertos_requeridos):
                                continue
                        
                        num_saltos = len(nuevo_camino) - 1
                        num_escalas = max(0, num_saltos - 1)
                        
                        return RutaEncontrada(
                            ruta=nuevo_camino,
                            num_escalas=num_escalas,
                            num_saltos=num_saltos,
                            aeropuertos_intermedios=nuevo_camino[1:-1] if len(nuevo_camino) > 2 else [],
                            tiempo_total_estimado=self._calcular_tiempo_total(nuevo_camino),
                            descripcion=self._generar_descripcion_ruta(nuevo_camino, num_escalas)
                        )
                    
                    cola.append((vecino, nuevo_camino))
        
        return None
    
    def comparar_rutas(self, origen: str, destino: str, 
                       criterio: str = "escalas") -> List[RutaEncontrada]:
        """
        Compara diferentes rutas entre origen y destino según un criterio
        
        Args:
            origen: Aeropuerto de origen
            destino: Aeropuerto de destino
            criterio: "escalas", "tiempo", o "ambos"
            
        Returns:
            Lista de rutas ordenadas según el criterio
        """
        # Encontrar todas las rutas (limitado a 10 para no saturar)
        todas_rutas = self.encontrar_todas_rutas_min_escalas(origen, destino)
        
        if not todas_rutas:
            return []
        
        # Ordenar según criterio
        if criterio == "escalas":
            todas_rutas.sort(key=lambda r: (r.num_escalas, r.tiempo_total_estimado))
        elif criterio == "tiempo":
            todas_rutas.sort(key=lambda r: (r.tiempo_total_estimado, r.num_escalas))
        elif criterio == "ambos":
            todas_rutas.sort(key=lambda r: (r.num_escalas + r.tiempo_total_estimado / 100))
        
        return todas_rutas[:5]  # Top 5 rutas
    
    def mostrar_ruta(self, ruta: RutaEncontrada) -> None:
        """Muestra una ruta de forma formateada"""
        if not ruta:
            print("No se encontró ruta")
            return
        
        print(f"\n{'='*80}")
        print(f"RUTA ENCONTRADA")
        print(f"{'='*80}")
        
        print(f"\n{ruta.descripcion}")
        print(f"\nDETALLES:")
        print(f"   • Origen: {ruta.ruta[0]}")
        print(f"   • Destino: {ruta.ruta[-1]}")
        print(f"   • Número de saltos: {ruta.num_saltos}")
        print(f"   • Número de escalas: {ruta.num_escalas}")
        
        if ruta.aeropuertos_intermedios:
            print(f"   • Aeropuertos intermedios: {', '.join(ruta.aeropuertos_intermedios)}")
        
        print(f"\nRUTA COMPLETA:")
        for i, aeropuerto in enumerate(ruta.ruta):
            if i == 0:
                print(f"   {i+1}. Verde {aeropuerto} (ORIGEN)")
            elif i == len(ruta.ruta) - 1:
                print(f"   {i+1}. Rojo {aeropuerto} (DESTINO)")
            else:
                info = self.aeropuertos_info.get(aeropuerto)
                tipo = info.tipo.value if info else "desconocido"
                print(f"   {i+1}. Rojo {aeropuerto} (Escala - {tipo})")
        
        if ruta.tiempo_total_estimado > 0:
            horas = ruta.tiempo_total_estimado // 60
            minutos = ruta.tiempo_total_estimado % 60
            print(f"\nTIEMPO TOTAL ESTIMADO: {horas}h {minutos}min")
        
        print(f"{'='*80}\n")
    
    def mostrar_todas_rutas(self, rutas: List[RutaEncontrada]) -> None:
        """Muestra múltiples rutas de forma formateada"""
        if not rutas:
            print("No se encontraron rutas")
            return
        
        print(f"\n{'='*80}")
        print(f"RUTAS ENCONTRADAS ({len(rutas)} rutas)")
        print(f"{'='*80}")
        
        for i, ruta in enumerate(rutas, 1):
            print(f"\nRUTA #{i}")
            print(f"   • {ruta.descripcion}")
            print(f"   • Escalas: {ruta.num_escalas}")
            print(f"   • Tiempo estimado: {ruta.tiempo_total_estimado} min")
            print(f"   • Ruta: {' → '.join(ruta.ruta)}")
        
        print(f"{'='*80}\n")


# ============================================================
# EJEMPLOS PRÁCTICOS
# ============================================================

def crear_red_aeroportuaria_ejemplo() -> RedAeroportuaria:
    """Crea una red aeroportuaria de ejemplo"""
    red = RedAeroportuaria()
    
    # Agregar aeropuertos
    aeropuertos = [
        ("MAD", TipoAeropuerto.HUB_PRINCIPAL, "Madrid", "España", 1000),
        ("BCN", TipoAeropuerto.HUB_SECUNDARIO, "Barcelona", "España", 800),
        ("LHR", TipoAeropuerto.HUB_PRINCIPAL, "Londres", "Reino Unido", 1200),
        ("CDG", TipoAeropuerto.HUB_PRINCIPAL, "París", "Francia", 1100),
        ("FRA", TipoAeropuerto.HUB_PRINCIPAL, "Fráncfort", "Alemania", 900),
        ("AMS", TipoAeropuerto.HUB_SECUNDARIO, "Ámsterdam", "Países Bajos", 850),
        ("JFK", TipoAeropuerto.HUB_PRINCIPAL, "Nueva York", "EE.UU.", 1500),
        ("LAX", TipoAeropuerto.HUB_PRINCIPAL, "Los Ángeles", "EE.UU.", 1400),
        ("MEX", TipoAeropuerto.HUB_SECUNDARIO, "Ciudad de México", "México", 700),
        ("BOG", TipoAeropuerto.AEROPUERTO_INTERNACIONAL, "Bogotá", "Colombia", 600),
        ("EZE", TipoAeropuerto.AEROPUERTO_INTERNACIONAL, "Buenos Aires", "Argentina", 500),
        ("GRU", TipoAeropuerto.AEROPUERTO_INTERNACIONAL, "São Paulo", "Brasil", 550),
        ("SYD", TipoAeropuerto.HUB_PRINCIPAL, "Sídney", "Australia", 800),
        ("NRT", TipoAeropuerto.HUB_PRINCIPAL, "Tokio", "Japón", 900),
        ("DXB", TipoAeropuerto.HUB_PRINCIPAL, "Dubái", "EAU", 1300),
        ("IST", TipoAeropuerto.HUB_SECUNDARIO, "Estambul", "Turquía", 750),
        ("DOH", TipoAeropuerto.HUB_SECUNDARIO, "Doha", "Qatar", 700),
        ("SIN", TipoAeropuerto.HUB_PRINCIPAL, "Singapur", "Singapur", 850),
    ]
    
    for nombre, tipo, ciudad, pais, capacidad in aeropuertos:
        red.agregar_aeropuerto(nombre, tipo, ciudad, pais, capacidad)
    
    # Agregar conexiones con tiempos de vuelo (minutos)
    conexiones = [
        # Europa
        ("MAD", "BCN", 60, 45),
        ("MAD", "LHR", 120, 90),
        ("MAD", "CDG", 110, 85),
        ("MAD", "FRA", 130, 100),
        ("BCN", "CDG", 100, 75),
        ("BCN", "AMS", 110, 80),
        ("LHR", "CDG", 60, 45),
        ("LHR", "AMS", 65, 50),
        ("LHR", "FRA", 75, 55),
        ("CDG", "FRA", 65, 50),
        ("CDG", "AMS", 60, 45),
        ("FRA", "AMS", 60, 45),
        ("MAD", "IST", 240, 200),
        ("LHR", "IST", 220, 180),
        ("CDG", "IST", 210, 170),
        ("FRA", "IST", 200, 160),
        
        # Europa - América
        ("MAD", "JFK", 420, 360),
        ("MAD", "MEX", 480, 420),
        ("MAD", "BOG", 520, 460),
        ("LHR", "JFK", 410, 350),
        ("CDG", "JFK", 400, 340),
        ("FRA", "JFK", 430, 370),
        ("MAD", "EZE", 720, 660),
        ("MAD", "GRU", 660, 600),
        
        # América
        ("JFK", "LAX", 300, 240),
        ("JFK", "MEX", 270, 220),
        ("JFK", "BOG", 300, 250),
        ("LAX", "MEX", 230, 180),
        ("MEX", "BOG", 270, 220),
        ("MEX", "EZE", 540, 480),
        ("MEX", "GRU", 500, 440),
        ("BOG", "EZE", 400, 340),
        ("BOG", "GRU", 380, 320),
        ("EZE", "GRU", 210, 170),
        
        # Europa - Asia
        ("IST", "DXB", 270, 220),
        ("IST", "DOH", 280, 230),
        ("IST", "NRT", 700, 640),
        ("DXB", "DOH", 60, 45),
        ("DXB", "NRT", 540, 480),
        ("DXB", "SIN", 420, 360),
        ("DOH", "SIN", 440, 380),
        ("NRT", "SIN", 400, 340),
        ("NRT", "SYD", 560, 500),
        ("SIN", "SYD", 480, 420),
        
        # Europa - Asia (conexiones adicionales)
        ("MAD", "DXB", 420, 360),
        ("LHR", "DXB", 400, 340),
        ("CDG", "DXB", 410, 350),
        ("FRA", "DXB", 380, 320),
    ]
    
    for a1, a2, tiempo, distancia in conexiones:
        red.agregar_conexion(a1, a2, distancia, tiempo)
    
    return red


def demostracion_completa():
    """Demostración completa de todas las funcionalidades"""
    
    print("="*80)
    print("MAPEO DE RUTAS CON MÍNIMO DE ESCALAS")
    print("="*80)
    
    # Crear red
    red = crear_red_aeroportuaria_ejemplo()
    
    # ============================================
    # Prueba 1: Ruta con mínimo de escalas
    # ============================================
    print("\n" + "="*80)
    print("Prueba 1: RUTA CON MÍNIMO DE ESCALAS")
    print("="*80)
    
    ruta = red.encontrar_ruta_min_escalas("MAD", "JFK")
    red.mostrar_ruta(ruta)
    
    # ============================================
    # Prueba 2: Ruta con múltiples escalas
    # ============================================
    print("\n" + "="*80)
    print("Prueba 2: RUTA CON MÚLTIPLES ESCALAS")
    print("="*80)
    
    ruta_larga = red.encontrar_ruta_min_escalas("MAD", "SYD")
    red.mostrar_ruta(ruta_larga)
    
    # ============================================
    # Prueba 3: Todas las rutas con mínimo de escalas
    # ============================================
    print("\n" + "="*80)
    print("Prueba 3: TODAS LAS RUTAS CON MÍNIMO DE ESCALAS")
    print("="*80)
    
    rutas = red.encontrar_todas_rutas_min_escalas("MAD", "JFK")
    red.mostrar_todas_rutas(rutas)
    
    # ============================================
    # Prueba 4: Ruta con restricciones
    # ============================================
    print("\n" + "="*80)
    print("Prueba 4: RUTA CON RESTRICCIONES")
    print("="*80)
    
    ruta_restringida = red.encontrar_ruta_con_restricciones(
        "MAD", "JFK",
        max_escalas=1,
        aeropuertos_prohibidos={"CDG"},
        aeropuertos_requeridos={"LHR"}
    )
    red.mostrar_ruta(ruta_restringida)
    
    # ============================================
    # Prueba 5: Comparación de rutas
    # ============================================
    print("\n" + "="*80)
    print("Prueba 5: COMPARACIÓN DE RUTAS")
    print("="*80)
    
    print("\nRutas ordenadas por número de escalas:")
    rutas_por_escalas = red.comparar_rutas("MAD", "SYD", "escalas")
    red.mostrar_todas_rutas(rutas_por_escalas)
    
    print("\nRutas ordenadas por tiempo total:")
    rutas_por_tiempo = red.comparar_rutas("MAD", "SYD", "tiempo")
    red.mostrar_todas_rutas(rutas_por_tiempo)
    
    # ============================================
    # Prueba 6: Ruta con diferentes escalas
    # ============================================
    print("\n" + "="*80)
    print("Prueba 6: RUTA CON RESTRICCIÓN DE ESCALAS MÁXIMAS")
    print("="*80)
    
    # Intentar ruta con máximo 2 escalas
    ruta_limitada = red.encontrar_ruta_con_restricciones("MAD", "SYD", max_escalas=2)
    if ruta_limitada:
        red.mostrar_ruta(ruta_limitada)
    else:
        print("No se encontró ruta con máximo 2 escalas")
    
    # ============================================
    # Prueba 7: Ruta con aeropuertos requeridos
    # ============================================
    print("\n" + "="*80)
    print("Prueba 7: RUTA CON AEROPUERTOS REQUERIDOS")
    print("="*80)
    
    ruta_requerida = red.encontrar_ruta_con_restricciones(
        "MAD", "SYD",
        aeropuertos_requeridos={"DXB", "SIN"}
    )
    red.mostrar_ruta(ruta_requerida)
    
    # ============================================
    # Prueba 8: Análisis de conectividad
    # ============================================
    print("\n" + "="*80)
    print("Prueba 8: ANÁLISIS DE CONECTIVIDAD")
    print("="*80)
    
    # Verificar conectividad entre pares de aeropuertos
    pares = [("MAD", "JFK"), ("MAD", "SYD"), ("MAD", "EZE"), ("BOG", "NRT")]
    
    for origen, destino in pares:
        ruta = red.encontrar_ruta_min_escalas(origen, destino)
        if ruta:
            print(f"{origen} → {destino}: {ruta.num_escalas} escala(s)")
            print(f"   Ruta: {' → '.join(ruta.ruta)}")
        else:
            print(f"No hay ruta de {origen} a {destino}")


# FUNCIONES ADICIONALES

def visualizar_ruta_ascii(ruta: RutaEncontrada) -> str:
    """Genera una representación ASCII de la ruta"""
    if not ruta:
        return "No hay ruta"
    
    visual = []
    visual.append(" RUTA DE VUELO")
    visual.append("=" * 50)
    
    for i, aeropuerto in enumerate(ruta.ruta):
        if i == 0:
            visual.append(f"Verde {i+1}. {aeropuerto} (ORIGEN)")
        elif i == len(ruta.ruta) - 1:
            visual.append(f"Rojo {i+1}. {aeropuerto} (DESTINO)")
        else:
            visual.append(f"Rojo {i+1}. {aeropuerto} (ESCALA)")
        
        # Conectar con flecha
        if i < len(ruta.ruta) - 1:
            visual.append("   ↓")
    
    visual.append("=" * 50)
    visual.append(f"Escalas: {ruta.num_escalas}")
    visual.append(f"Tiempo estimado: {ruta.tiempo_total_estimado} min")
    
    return "\n".join(visual)


def exportar_rutas_json(rutas: List[RutaEncontrada], archivo: str) -> None:
    """Exporta rutas a un archivo JSON"""
    datos = []
    for ruta in rutas:
        datos.append({
            'ruta': ruta.ruta,
            'num_escalas': ruta.num_escalas,
            'num_saltos': ruta.num_saltos,
            'tiempo_total_estimado': ruta.tiempo_total_estimado,
            'descripcion': ruta.descripcion
        })
    
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    demostracion_completa()
    
    # Ejemplo adicional de visualización ASCII
    print("\n" + "="*80)
    print("VISUALIZACIÓN ASCII DE RUTA")
    print("="*80)
    
    red = crear_red_aeroportuaria_ejemplo()
    ruta = red.encontrar_ruta_min_escalas("MAD", "SYD")
    if ruta:
        print(visualizar_ruta_ascii(ruta))
