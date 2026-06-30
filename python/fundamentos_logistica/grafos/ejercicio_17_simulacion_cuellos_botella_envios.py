"""Ejercicio 17: Simulación de Cuellos de Botella por Envíos en Batch/Oleadas

En una cadena de suministro, los despachos se hacen por "Oleadas diarias". En el día 0, el CD despacha.
En el día 1, reciben sus clientes directos. En el día 2, los sub-clientes, etc. Escribe una función 
que agrupe los nodos de la red por su "Día de llegada". La salida debe ser un diccionario o lista
de listas: {Día 0: [CD], Día 1: [clienteA, ClienteB], Día 2: [...]}. Esto servirá para calcular 
el inventario en tránsito esperado por día. """

from typing import Dict, List, Set, Tuple, Optional, Any, Union
from collections import deque, defaultdict
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import math

class TipoNodo(Enum):
    """Clasificación de nodos en la cadena de suministro"""
    CENTRO_DISTRIBUCION = "centro_distribucion"
    ALMACEN_REGIONAL = "almacen_regional"
    CLIENTE_MAYORISTA = "cliente_mayorista"
    CLIENTE_MINORISTA = "cliente_minorista"
    PUNTO_VENTA = "punto_venta"
    CENTRO_LOGISTICO = "centro_logistico"

class EstadoEnvio(Enum):
    """Estado de un envío en la cadena"""
    PENDIENTE = "pendiente"
    EN_TRANSITO = "en_transito"
    ENTREGADO = "entregado"
    RETRASADO = "retrasado"
    PERDIDO = "perdido"

@dataclass
class NodoCadena:
    """Información de un nodo en la cadena de suministro"""
    nombre: str
    tipo: TipoNodo
    ubicacion: str
    capacidad_diaria: float = 0.0
    inventario_actual: float = 0.0
    demanda_diaria: float = 0.0
    tiempo_procesamiento: int = 0  # días
    
@dataclass
class Envio:
    """Representa un envío en la cadena"""
    id: str
    origen: str
    destino: str
    cantidad: float
    dia_envio: int
    dia_llegada_estimado: int
    estado: EstadoEnvio = EstadoEnvio.PENDIENTE
    dia_llegada_real: Optional[int] = None

@dataclass
class OleadaDiaria:
    """Representa una oleada de envíos en un día específico"""
    dia: int
    nodos_que_reciben: List[str]
    cantidad_total: float
    envios: List[Envio]
    detalle_por_nodo: Dict[str, float]

class CadenaSuministroOleadas:
    """
    Simulación de cadena de suministro con envíos por oleadas diarias.
    
    Características:
    - Agrupación de nodos por día de llegada
    - Simulación de oleadas de envíos
    - Cálculo de inventario en tránsito
    - Análisis de cuellos de botella
    - Proyección de demanda
    - Estadísticas de entregas
    """
    
    def __init__(self, nombre: str = "Cadena de Suministro"):
        """
        Inicializa la cadena de suministro
        
        Args:
            nombre: Nombre identificativo de la cadena
        """
        self.nombre = nombre
        self.adyacencia: Dict[str, Set[str]] = defaultdict(set)
        self.nodos_info: Dict[str, NodoCadena] = {}
        self.total_nodos = 0
        self.total_conexiones = 0
        
        # Datos de envíos
        self.envios: List[Envio] = []
        self.historial_envios: Dict[int, List[Envio]] = defaultdict(list)
        
        # Capacidades y tiempos de tránsito
        self.tiempos_transito: Dict[Tuple[str, str], int] = {}
        self.capacidades_ruta: Dict[Tuple[str, str], float] = {}
        
        # Cache de resultados de oleadas
        self.cache_oleadas: Dict[Tuple[str, int], List[OleadaDiaria]] = {}
        
        # Estadísticas
        self.total_enviado = 0.0
        self.total_entregado = 0.0
        self.dia_actual = 0
    
    def agregar_nodo(self, nombre: str, tipo: TipoNodo = TipoNodo.CLIENTE_MINORISTA,
                     ubicacion: str = "", capacidad_diaria: float = 0.0,
                     inventario_actual: float = 0.0, demanda_diaria: float = 0.0,
                     tiempo_procesamiento: int = 0) -> None:
        """
        Agrega un nodo a la cadena de suministro
        
        Args:
            nombre: Identificador del nodo
            tipo: Tipo de nodo
            ubicacion: Ubicación geográfica
            capacidad_diaria: Capacidad de procesamiento por día
            inventario_actual: Inventario disponible
            demanda_diaria: Demanda diaria del nodo
            tiempo_procesamiento: Días que tarda en procesar
        """
        if nombre in self.nodos_info:
            raise ValueError(f"El nodo '{nombre}' ya existe en la cadena")
        
        self.nodos_info[nombre] = NodoCadena(
            nombre=nombre,
            tipo=tipo,
            ubicacion=ubicacion,
            capacidad_diaria=capacidad_diaria,
            inventario_actual=inventario_actual,
            demanda_diaria=demanda_diaria,
            tiempo_procesamiento=tiempo_procesamiento
        )
        self.total_nodos += 1
    
    def agregar_conexion(self, nodo1: str, nodo2: str, 
                        tiempo_transito: int = 1,
                        capacidad: float = float('inf')) -> None:
        """
        Agrega una conexión bidireccional entre nodos
        
        Args:
            nodo1: Primer nodo
            nodo2: Segundo nodo
            tiempo_transito: Días que tarda el envío
            capacidad: Capacidad máxima de la ruta (toneladas/día)
        """
        if nodo1 not in self.nodos_info:
            raise ValueError(f"El nodo '{nodo1}' no existe")
        if nodo2 not in self.nodos_info:
            raise ValueError(f"El nodo '{nodo2}' no existe")
        if nodo1 == nodo2:
            raise ValueError("No se puede conectar un nodo consigo mismo")
        
        self.adyacencia[nodo1].add(nodo2)
        self.adyacencia[nodo2].add(nodo1)
        self.total_conexiones += 1
        
        # Guardar tiempo de tránsito (mismo en ambas direcciones)
        self.tiempos_transito[(nodo1, nodo2)] = tiempo_transito
        self.tiempos_transito[(nodo2, nodo1)] = tiempo_transito
        
        # Guardar capacidad de ruta
        self.capacidades_ruta[(nodo1, nodo2)] = capacidad
        self.capacidades_ruta[(nodo2, nodo1)] = capacidad
    
    def calcular_oleadas(self, cd_principal: str, 
                        dias_simulacion: int = 30,
                        incluir_detalles: bool = True) -> List[OleadaDiaria]:
        """
        Calcula las oleadas de envíos desde el CD principal
        
        Args:
            cd_principal: Centro de Distribución principal
            dias_simulacion: Número de días a simular
            incluir_detalles: Si incluye detalles de envíos
            
        Returns:
            Lista de OleadaDiaria por día
        """
        if cd_principal not in self.nodos_info:
            raise ValueError(f"El CD '{cd_principal}' no existe")
        
        # Verificar cache
        cache_key = (cd_principal, dias_simulacion)
        if cache_key in self.cache_oleadas:
            return self.cache_oleadas[cache_key]
        
        # BFS para calcular días de llegada
        cola: deque = deque()
        cola.append((cd_principal, 0))  # (nodo, dia)
        
        visitados: Set[str] = {cd_principal}
        dias_llegada: Dict[str, int] = {cd_principal: 0}
        padres: Dict[str, str] = {}
        
        # Para rastrear la ruta más corta en días
        while cola:
            nodo_actual, dia_actual = cola.popleft()
            
            for vecino in self.adyacencia.get(nodo_actual, set()):
                if vecino not in visitados:
                    # Calcular día de llegada considerando tiempo de tránsito
                    tiempo_transito = self.tiempos_transito.get((nodo_actual, vecino), 1)
                    dia_llegada = dia_actual + tiempo_transito
                    
                    if dia_llegada <= dias_simulacion:
                        visitados.add(vecino)
                        dias_llegada[vecino] = dia_llegada
                        padres[vecino] = nodo_actual
                        cola.append((vecino, dia_llegada))
        
        # Agrupar nodos por día de llegada
        nodos_por_dia: Dict[int, List[str]] = defaultdict(list)
        for nodo, dia in dias_llegada.items():
            if dia <= dias_simulacion:
                nodos_por_dia[dia].append(nodo)
        
        # Crear oleadas diarias
        oleadas = []
        envios_por_dia: Dict[int, List[Envio]] = defaultdict(list)
        
        for dia in range(dias_simulacion + 1):
            nodos_dia = nodos_por_dia.get(dia, [])
            
            if not nodos_dia and dia > 0:
                # Si no hay nodos en este día, crear oleada vacía
                oleada = OleadaDiaria(
                    dia=dia,
                    nodos_que_reciben=[],
                    cantidad_total=0.0,
                    envios=[],
                    detalle_por_nodo={}
                )
                oleadas.append(oleada)
                continue
            
            # Calcular envíos para este día
            envios_dia = []
            cantidad_total = 0.0
            detalle_por_nodo = {}
            
            for nodo in nodos_dia:
                if nodo == cd_principal:
                    continue  # El CD no recibe envíos
                
                # Calcular cantidad a enviar (basado en demanda)
                info_nodo = self.nodos_info.get(nodo)
                if not info_nodo:
                    continue
                
                # Demanda del nodo * días desde último envío
                demanda = info_nodo.demanda_diaria
                cantidad = demanda * 1.2  # 20% extra para seguridad
                
                # Verificar capacidad de la ruta
                padre = padres.get(nodo)
                if padre:
                    capacidad_ruta = self.capacidades_ruta.get((padre, nodo), float('inf'))
                    cantidad = min(cantidad, capacidad_ruta)
                
                # Crear envío
                envio_id = f"E{dia}-{nodo}-{len(self.envios)}"
                envio = Envio(
                    id=envio_id,
                    origen=padre if padre else cd_principal,
                    destino=nodo,
                    cantidad=cantidad,
                    dia_envio=dia - self.tiempos_transito.get((padre, nodo), 1) if padre else 0,
                    dia_llegada_estimado=dia,
                    estado=EstadoEnvio.EN_TRANSITO if dia > 0 else EstadoEnvio.ENTREGADO
                )
                
                envios_dia.append(envio)
                cantidad_total += cantidad
                detalle_por_nodo[nodo] = cantidad
                
                # Guardar en historial
                self.envios.append(envio)
                envios_por_dia[dia].append(envio)
            
            # Crear oleada
            oleada = OleadaDiaria(
                dia=dia,
                nodos_que_reciben=nodos_dia,
                cantidad_total=cantidad_total,
                envios=envios_dia if incluir_detalles else [],
                detalle_por_nodo=detalle_por_nodo
            )
            oleadas.append(oleada)
        
        # Guardar en cache
        self.cache_oleadas[cache_key] = oleadas
        
        # Actualizar estadísticas
        self._actualizar_estadisticas(oleadas)
        
        return oleadas
    
    def _actualizar_estadisticas(self, oleadas: List[OleadaDiaria]) -> None:
        """Actualiza estadísticas globales"""
        total_enviado = 0.0
        total_entregado = 0.0
        
        for oleada in oleadas:
            total_enviado += oleada.cantidad_total
            for envio in oleada.envios:
                if envio.estado == EstadoEnvio.ENTREGADO:
                    total_entregado += envio.cantidad
        
        self.total_enviado = total_enviado
        self.total_entregado = total_entregado
    
    def calcular_inventario_transito(self, oleadas: List[OleadaDiaria]) -> Dict[int, float]:
        """
        Calcula el inventario en tránsito por día
        
        Args:
            oleadas: Lista de oleadas diarias
            
        Returns:
            Dict con inventario en tránsito por día
        """
        inventario_transito = defaultdict(float)
        
        for oleada in oleadas:
            for envio in oleada.envios:
                if envio.estado == EstadoEnvio.EN_TRANSITO:
                    # El envío está en tránsito desde su día de envío hasta su llegada
                    for dia in range(envio.dia_envio, envio.dia_llegada_estimado):
                        inventario_transito[dia] += envio.cantidad
        
        return dict(inventario_transito)
    
    def calcular_inventario_total(self, oleadas: List[OleadaDiaria]) -> Dict[int, float]:
        """
        Calcula el inventario total por día (en tránsito + en nodos)
        
        Args:
            oleadas: Lista de oleadas diarias
            
        Returns:
            Dict con inventario total por día
        """
        inventario_total = defaultdict(float)
        
        # Inventario en tránsito
        inventario_transito = self.calcular_inventario_transito(oleadas)
        for dia, cantidad in inventario_transito.items():
            inventario_total[dia] += cantidad
        
        # Inventario en nodos
        for nodo, info in self.nodos_info.items():
            # Asumir que el inventario se consume diariamente
            for dia in range(len(oleadas)):
                if dia == 0:
                    inventario_total[dia] += info.inventario_actual
                else:
                    # Consumo diario
                    consumo = info.demanda_diaria
                    inventario_total[dia] = max(0, inventario_total.get(dia, 0) - consumo)
        
        return dict(inventario_total)
    
    def identificar_cuellos_botella(self, oleadas: List[OleadaDiaria], 
                                   umbral: float = 0.8) -> List[Dict[str, Any]]:
        """
        Identifica posibles cuellos de botella en la cadena
        
        Args:
            oleadas: Lista de oleadas diarias
            umbral: Porcentaje de capacidad para considerar cuello de botella
            
        Returns:
            Lista de cuellos de botella identificados
        """
        cuellos_botella = []
        
        # Analizar cada nodo
        for nodo, info in self.nodos_info.items():
            if info.capacidad_diaria <= 0:
                continue
            
            # Calcular flujo promedio que pasa por el nodo
            flujo_total = 0.0
            dias_con_flujo = 0
            
            for oleada in oleadas:
                if nodo in oleada.nodos_que_reciben:
                    cantidad = oleada.detalle_por_nodo.get(nodo, 0)
                    flujo_total += cantidad
                    dias_con_flujo += 1
            
            if dias_con_flujo > 0:
                flujo_promedio = flujo_total / dias_con_flujo
                utilizacion = flujo_promedio / info.capacidad_diaria
                
                if utilizacion >= umbral:
                    cuellos_botella.append({
                        'nodo': nodo,
                        'tipo': info.tipo.value,
                        'capacidad': info.capacidad_diaria,
                        'flujo_promedio': flujo_promedio,
                        'utilizacion': utilizacion,
                        'nivel': f"{utilizacion*100:.1f}%",
                        'recomendacion': self._generar_recomendacion(utilizacion, info)
                    })
        
        # Ordenar por nivel de utilización (descendente)
        cuellos_botella.sort(key=lambda x: x['utilizacion'], reverse=True)
        
        return cuellos_botella
    
    def _generar_recomendacion(self, utilizacion: float, info: NodoCadena) -> str:
        """Genera recomendación basada en la utilización"""
        if utilizacion >= 0.95:
            return f"CRÍTICO: Aumentar capacidad de {info.nombre} urgentemente"
        elif utilizacion >= 0.85:
            return f"ALTO: Considerar expansión de {info.nombre}"
        elif utilizacion >= 0.75:
            return f"MEDIO: Monitorear {info.nombre} de cerca"
        else:
            return f"ACEPTABLE: {info.nombre} operando normalmente"
    
    def proyectar_demanda(self, cd_principal: str, 
                          dias_proyeccion: int = 30) -> Dict[int, float]:
        """
        Proyecta la demanda futura basada en patrones históricos
        
        Args:
            cd_principal: Centro de Distribución principal
            dias_proyeccion: Días a proyectar
            
        Returns:
            Dict con proyección de demanda por día
        """
        # Obtener oleadas históricas
        oleadas = self.calcular_oleadas(cd_principal, dias_proyeccion)
        
        # Calcular demanda por día
        demanda_diaria = defaultdict(float)
        
        for oleada in oleadas:
            for nodo, cantidad in oleada.detalle_por_nodo.items():
                info = self.nodos_info.get(nodo)
                if info:
                    demanda_diaria[oleada.dia] += info.demanda_diaria
        
        # Suavizar con promedio móvil
        proyeccion = {}
        ventana = 7  # Promedio de 7 días
        
        for dia in range(dias_proyeccion + 1):
            if dia < len(oleadas):
                proyeccion[dia] = demanda_diaria[dia]
            else:
                # Usar promedio de días anteriores
                dias_anteriores = [d for d in range(max(0, dia-ventana), dia) if d in demanda_diaria]
                if dias_anteriores:
                    promedio = sum(demanda_diaria[d] for d in dias_anteriores) / len(dias_anteriores)
                    proyeccion[dia] = promedio * 1.05  # 5% de crecimiento estimado
                else:
                    proyeccion[dia] = 0
        
        return dict(proyeccion)
    
    def mostrar_oleadas(self, cd_principal: str, 
                        dias_simulacion: int = 10,
                        mostrar_detalles: bool = True) -> None:
        """
        Muestra de forma formateada las oleadas diarias
        
        Args:
            cd_principal: Centro de Distribución principal
            dias_simulacion: Días a simular
            mostrar_detalles: Si muestra detalles de envíos
        """
        print(f"\n{'='*80}")
        print(f"SIMULACIÓN DE OLEADAS DIARIAS")
        print(f"   Cadena: {self.nombre}")
        print(f"   CD Principal: {cd_principal}")
        print(f"   Días de simulación: {dias_simulacion}")
        print(f"{'='*80}")
        
        # Calcular oleadas
        oleadas = self.calcular_oleadas(cd_principal, dias_simulacion, mostrar_detalles)
        
        # Mostrar resumen por día
        print(f"\nRESUMEN POR DÍA:")
        print(f"{'Día':>4} | {'Nodos que reciben':<30} | {'Cantidad':>10} | {'Envíos':>6}")
        print("-" * 80)
        
        for oleada in oleadas[:dias_simulacion + 1]:
            nodos_str = ', '.join(oleada.nodos_que_reciben) if oleada.nodos_que_reciben else "(ninguno)"
            if len(nodos_str) > 28:
                nodos_str = nodos_str[:25] + "..."
            
            print(f"{oleada.dia:>4} | {nodos_str:<30} | {oleada.cantidad_total:>10.1f} | {len(oleada.envios):>6}")
        
        # Mostrar detalles de envíos si se solicita
        if mostrar_detalles:
            print(f"\nDETALLE DE ENVÍOS POR DÍA:")
            for oleada in oleadas[:dias_simulacion + 1]:
                if oleada.envios:
                    print(f"\n  Día {oleada.dia}:")
                    for envio in oleada.envios[:5]:  # Mostrar primeros 5
                        estado_icono = "BIEN" if envio.estado == EstadoEnvio.ENTREGADO else "EN CAMINO"
                        print(f"    {estado_icono} {envio.origen} → {envio.destino}: {envio.cantidad:.1f} ton")
                    if len(oleada.envios) > 5:
                        print(f"    ... y {len(oleada.envios) - 5} envíos más")
        
        # Mostrar inventario en tránsito
        inventario_transito = self.calcular_inventario_transito(oleadas)
        if inventario_transito:
            print(f"\nINVENTARIO EN TRÁNSITO POR DÍA:")
            for dia in sorted(inventario_transito.keys())[:dias_simulacion + 1]:
                print(f"  Día {dia}: {inventario_transito[dia]:.1f} toneladas")
        
        # Mostrar cuellos de botella
        cuellos = self.identificar_cuellos_botella(oleadas)
        if cuellos:
            print(f"\nCUELLOS DE BOTELLA IDENTIFICADOS:")
            for i, cuello in enumerate(cuellos[:5], 1):
                print(f"  {i}. {cuello['nodo']} - {cuello['nivel']} de capacidad")
                print(f"     {cuello['recomendacion']}")
        
        print(f"{'='*80}\n")
    
    def mostrar_analisis_completo(self, cd_principal: str, 
                                 dias_simulacion: int = 15) -> None:
        """
        Muestra un análisis completo de la cadena de suministro
        
        Args:
            cd_principal: Centro de Distribución principal
            dias_simulacion: Días a simular
        """
        print(f"\n{'='*80}")
        print(f"ANÁLISIS COMPLETO DE CADENA DE SUMINISTRO")
        print(f"   {self.nombre}")
        print(f"{'='*80}")
        
        # Calcular oleadas
        oleadas = self.calcular_oleadas(cd_principal, dias_simulacion)
        
        # Estadísticas generales
        print(f"\nESTADÍSTICAS GENERALES:")
        print(f"   • Total de nodos: {self.total_nodos}")
        print(f"   • Total de conexiones: {self.total_conexiones}")
        print(f"   • Total enviado: {self.total_enviado:.1f} toneladas")
        print(f"   • Total entregado: {self.total_entregado:.1f} toneladas")
        print(f"   • Tasa de entrega: {(self.total_entregado/self.total_enviado*100) if self.total_enviado > 0 else 0:.1f}%")
        
        # Distribución de nodos por tipo
        distribucion = defaultdict(int)
        for info in self.nodos_info.values():
            distribucion[info.tipo.value] += 1
        
        print(f"\nDISTRIBUCIÓN POR TIPO:")
        for tipo, cantidad in distribucion.items():
            print(f"   • {tipo}: {cantidad}")
        
        # Proyección de demanda
        proyeccion = self.proyectar_demanda(cd_principal, dias_simulacion)
        if proyeccion:
            print(f"\nPROYECCIÓN DE DEMANDA (próximos {dias_simulacion} días):")
            for dia in sorted(proyeccion.keys())[:10]:
                print(f"   Día {dia}: {proyeccion[dia]:.1f} toneladas")
            if len(proyeccion) > 10:
                print(f"   ... y {len(proyeccion) - 10} días más")
        
        # Cuellos de botella detallados
        cuellos = self.identificar_cuellos_botella(oleadas)
        if cuellos:
            print(f"\nCUELLOS DE BOTELLA DETALLADOS:")
            for cuello in cuellos[:3]:
                print(f"\n{cuello['nodo']} ({cuello['tipo']})")
                print(f"     • Capacidad: {cuello['capacidad']:.1f} ton/día")
                print(f"     • Flujo promedio: {cuello['flujo_promedio']:.1f} ton/día")
                print(f"     • Utilización: {cuello['nivel']}")
                print(f"     • {cuello['recomendacion']}")
        
        print(f"{'='*80}\n")


# ============================================================
# EJEMPLOS PRÁCTICOS
# ============================================================

def crear_cadena_suministro_ejemplo() -> CadenaSuministroOleadas:
    """Crea una cadena de suministro de ejemplo"""
    cadena = CadenaSuministroOleadas("Cadena Logística Nacional")
    
    # Agregar nodos
    nodos = [
        # Centro de Distribución
        ("CD", TipoNodo.CENTRO_DISTRIBUCION, "Madrid", 5000, 10000, 0, 0),
        
        # Almacenes Regionales
        ("AR_Norte", TipoNodo.ALMACEN_REGIONAL, "Burgos", 2000, 1000, 800, 1),
        ("AR_Sur", TipoNodo.ALMACEN_REGIONAL, "Sevilla", 1800, 800, 700, 1),
        ("AR_Este", TipoNodo.ALMACEN_REGIONAL, "Valencia", 1600, 600, 600, 1),
        ("AR_Oeste", TipoNodo.ALMACEN_REGIONAL, "Salamanca", 1400, 400, 500, 1),
        
        # Clientes Mayoristas
        ("CM_Barcelona", TipoNodo.CLIENTE_MAYORISTA, "Barcelona", 800, 300, 400, 1),
        ("CM_Bilbao", TipoNodo.CLIENTE_MAYORISTA, "Bilbao", 700, 200, 350, 1),
        ("CM_Alicante", TipoNodo.CLIENTE_MAYORISTA, "Alicante", 600, 200, 300, 1),
        ("CM_Malaga", TipoNodo.CLIENTE_MAYORISTA, "Málaga", 650, 150, 320, 1),
        ("CM_Zaragoza", TipoNodo.CLIENTE_MAYORISTA, "Zaragoza", 750, 250, 380, 1),
        
        # Clientes Minoristas
        ("Tienda1", TipoNodo.CLIENTE_MINORISTA, "Madrid-Centro", 200, 100, 150, 0),
        ("Tienda2", TipoNodo.CLIENTE_MINORISTA, "Madrid-Norte", 180, 80, 130, 0),
        ("Tienda3", TipoNodo.CLIENTE_MINORISTA, "Madrid-Sur", 160, 60, 120, 0),
        ("Tienda4", TipoNodo.CLIENTE_MINORISTA, "Barcelona-Centro", 200, 80, 150, 0),
        ("Tienda5", TipoNodo.CLIENTE_MINORISTA, "Valencia-Centro", 150, 50, 100, 0),
        ("Tienda6", TipoNodo.CLIENTE_MINORISTA, "Sevilla-Centro", 150, 50, 100, 0),
        
        # Puntos de Venta
        ("PV1", TipoNodo.PUNTO_VENTA, "Madrid-Usera", 50, 20, 30, 0),
        ("PV2", TipoNodo.PUNTO_VENTA, "Madrid-Carabanchel", 50, 15, 25, 0),
        ("PV3", TipoNodo.PUNTO_VENTA, "Barcelona-Gracia", 40, 15, 20, 0),
        ("PV4", TipoNodo.PUNTO_VENTA, "Valencia-Ruzafa", 40, 10, 20, 0),
    ]
    
    for nombre, tipo, ubicacion, capacidad, inventario, demanda, tiempo in nodos:
        cadena.agregar_nodo(nombre, tipo, ubicacion, capacidad, inventario, demanda, tiempo)
    
    # Agregar conexiones (origen, destino, tiempo_transito, capacidad)
    conexiones = [
        # CD -> Almacenes Regionales
        ("CD", "AR_Norte", 1, 3000),
        ("CD", "AR_Sur", 2, 2500),
        ("CD", "AR_Este", 1, 2500),
        ("CD", "AR_Oeste", 1, 2000),
        
        # Almacenes Regionales -> Clientes Mayoristas
        ("AR_Norte", "CM_Bilbao", 1, 1500),
        ("AR_Norte", "CM_Zaragoza", 1, 1500),
        ("AR_Este", "CM_Barcelona", 1, 1800),
        ("AR_Este", "CM_Alicante", 1, 1200),
        ("AR_Sur", "CM_Malaga", 1, 1300),
        ("AR_Oeste", "CM_Zaragoza", 1, 1200),
        
        # Clientes Mayoristas -> Clientes Minoristas
        ("CM_Barcelona", "Tienda4", 1, 600),
        ("CM_Barcelona", "Tienda5", 1, 500),
        ("CM_Bilbao", "Tienda6", 1, 400),
        ("CM_Alicante", "Tienda5", 1, 400),
        ("CM_Malaga", "Tienda6", 1, 400),
        ("CM_Zaragoza", "Tienda1", 1, 500),
        ("CM_Zaragoza", "Tienda2", 1, 400),
        ("CM_Zaragoza", "Tienda3", 1, 400),
        
        # Clientes Minoristas -> Puntos de Venta
        ("Tienda1", "PV1", 1, 100),
        ("Tienda1", "PV2", 1, 100),
        ("Tienda4", "PV3", 1, 80),
        ("Tienda5", "PV4", 1, 80),
        
        # Conexiones entre Almacenes Regionales (redundancia)
        ("AR_Norte", "AR_Este", 2, 1000),
        ("AR_Norte", "AR_Oeste", 2, 1000),
        ("AR_Este", "AR_Sur", 3, 1000),
        ("AR_Sur", "AR_Oeste", 2, 1000),
        
        # Conexiones entre Mayoristas
        ("CM_Barcelona", "CM_Zaragoza", 2, 800),
        ("CM_Bilbao", "CM_Zaragoza", 1, 800),
        ("CM_Alicante", "CM_Malaga", 2, 800),
    ]
    
    for n1, n2, tiempo, capacidad in conexiones:
        cadena.agregar_conexion(n1, n2, tiempo, capacidad)
    
    return cadena


def crear_cadena_simple() -> CadenaSuministroOleadas:
    """Crea una cadena simple para demostración"""
    cadena = CadenaSuministroOleadas("Cadena Simple")
    
    # Nodos
    cadena.agregar_nodo("CD", TipoNodo.CENTRO_DISTRIBUCION, "Central", 1000, 5000, 0, 0)
    cadena.agregar_nodo("A", TipoNodo.ALMACEN_REGIONAL, "Región A", 500, 200, 300, 1)
    cadena.agregar_nodo("B", TipoNodo.ALMACEN_REGIONAL, "Región B", 500, 200, 300, 1)
    cadena.agregar_nodo("C", TipoNodo.ALMACEN_REGIONAL, "Región C", 500, 200, 300, 1)
    cadena.agregar_nodo("D", TipoNodo.CLIENTE_MAYORISTA, "Mayorista D", 300, 100, 150, 1)
    cadena.agregar_nodo("E", TipoNodo.CLIENTE_MAYORISTA, "Mayorista E", 300, 100, 150, 1)
    cadena.agregar_nodo("F", TipoNodo.CLIENTE_MINORISTA, "Tienda F", 100, 50, 80, 0)
    cadena.agregar_nodo("G", TipoNodo.CLIENTE_MINORISTA, "Tienda G", 100, 50, 80, 0)
    cadena.agregar_nodo("H", TipoNodo.PUNTO_VENTA, "PV H", 50, 20, 30, 0)
    cadena.agregar_nodo("I", TipoNodo.PUNTO_VENTA, "PV I", 50, 20, 30, 0)
    
    # Conexiones
    conexiones = [
        ("CD", "A", 1, 600),
        ("CD", "B", 1, 600),
        ("CD", "C", 1, 600),
        ("A", "D", 1, 400),
        ("A", "E", 1, 400),
        ("B", "D", 1, 400),
        ("B", "F", 1, 200),
        ("C", "E", 1, 400),
        ("C", "G", 1, 200),
        ("D", "H", 1, 150),
        ("E", "I", 1, 150),
        ("D", "E", 1, 200),
        ("F", "G", 1, 100),
    ]
    
    for n1, n2, tiempo, capacidad in conexiones:
        cadena.agregar_conexion(n1, n2, tiempo, capacidad)
    
    return cadena


def demostracion_completa():
    """Demostración completa de todas las funcionalidades"""
    
    print("="*80)
    print("SIMULACIÓN DE CUELLOS DE BOTELLA POR ENVÍOS EN OLEADAS")
    print("="*80)
    
    # Crear cadena
    cadena = crear_cadena_suministro_ejemplo()
    
    # ============================================
    # EJEMPLO 1: Oleadas básicas
    # ============================================
    print("\n" + "="*80)
    print("EJEMPLO 1: OLEADAS BÁSICAS (7 días)")
    print("="*80)
    
    cadena.mostrar_oleadas("CD", 7, mostrar_detalles=True)
    
    # ============================================
    # EJEMPLO 2: Análisis completo
    # ============================================
    print("\n" + "="*80)
    print("EJEMPLO 2: ANÁLISIS COMPLETO")
    print("="*80)
    
    cadena.mostrar_analisis_completo("CD", 10)
    
    # ============================================
    # EJEMPLO 3: Inventario en tránsito
    # ============================================
    print("\n" + "="*80)
    print("EJEMPLO 3: INVENTARIO EN TRÁNSITO")
    print("="*80)
    
    oleadas = cadena.calcular_oleadas("CD", 10)
    inventario_transito = cadena.calcular_inventario_transito(oleadas)
    
    print("Inventario en tránsito por día:")
    for dia in sorted(inventario_transito.keys())[:10]:
        print(f"  Día {dia}: {inventario_transito[dia]:.1f} toneladas")
    
    # ============================================
    # EJEMPLO 4: Proyección de demanda
    # ============================================
    print("\n" + "="*80)
    print("EJEMPLO 4: PROYECCIÓN DE DEMANDA")
    print("="*80)
    
    proyeccion = cadena.proyectar_demanda("CD", 15)
    print("Proyección de demanda:")
    for dia in sorted(proyeccion.keys())[:10]:
        print(f"  Día {dia}: {proyeccion[dia]:.1f} toneladas")
    
    # ============================================
    # EJEMPLO 5: Red simple para comparación
    # ============================================
    print("\n" + "="*80)
    print("EJEMPLO 5: RED SIMPLE")
    print("="*80)
    
    cadena_simple = crear_cadena_simple()
    cadena_simple.mostrar_oleadas("CD", 5, mostrar_detalles=True)
    
    # ============================================
    # EJEMPLO 6: Comparación de escenarios
    # ============================================
    print("\n" + "="*80)
    print("EJEMPLO 6: COMPARACIÓN DE ESCENARIOS")
    print("="*80)
    
    # Escenario 1: Capacidad normal
    print("\nEscenario 1: Capacidad normal")
    oleadas1 = cadena.calcular_oleadas("CD", 5)
    total1 = sum(o.cantidad_total for o in oleadas1)
    print(f"  Total enviado en 5 días: {total1:.1f} toneladas")
    
    # Escenario 2: Aumento de demanda
    print("\nEscenario 2: Aumento de demanda (simulado)")
    # Modificar demanda de algunos nodos
    cadena.nodos_info["CM_Barcelona"].demanda_diaria = 600  # +50%
    cadena.nodos_info["CM_Bilbao"].demanda_diaria = 525    # +50%
    
    oleadas2 = cadena.calcular_oleadas("CD", 5)
    total2 = sum(o.cantidad_total for o in oleadas2)
    print(f"  Total enviado en 5 días: {total2:.1f} toneladas")
    print(f"  Incremento: {((total2-total1)/total1*100):.1f}%")
    
    # Identificar nuevos cuellos de botella
    cuellos = cadena.identificar_cuellos_botella(oleadas2)
    if cuellos:
        print(f"\n  Nuevos cuellos de botella detectados:")
        for cuello in cuellos[:3]:
            print(f"    • {cuello['nodo']}: {cuello['nivel']} de capacidad")


# ============================================================
# FUNCIONES ADICIONALES ÚTILES
# ============================================================

def exportar_oleadas_csv(oleadas: List[OleadaDiaria], archivo: str) -> None:
    """
    Exporta las oleadas a un archivo CSV
    
    Args:
        oleadas: Lista de oleadas diarias
        archivo: Nombre del archivo de salida
    """
    import csv
    
    with open(archivo, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Dia', 'Nodo', 'Cantidad', 'Origen', 'Estado'])
        
        for oleada in oleadas:
            for envio in oleada.envios:
                writer.writerow([
                    oleada.dia,
                    envio.destino,
                    envio.cantidad,
                    envio.origen,
                    envio.estado.value
                ])


def generar_reporte_oleadas(cadena: CadenaSuministroOleadas, 
                           cd_principal: str,
                           dias: int = 10) -> str:
    """
    Genera un reporte en texto de las oleadas
    
    Args:
        cadena: Cadena de suministro
        cd_principal: Centro de Distribución principal
        dias: Días a simular
        
    Returns:
        String con el reporte
    """
    oleadas = cadena.calcular_oleadas(cd_principal, dias)
    
    reporte = []
    reporte.append("=" * 60)
    reporte.append(f"REPORTE DE OLEADAS - {cadena.nombre}")
    reporte.append("=" * 60)
    reporte.append(f"CD Principal: {cd_principal}")
    reporte.append(f"Días simulados: {dias}")
    reporte.append("=" * 60)
    reporte.append("")
    
    # Resumen por día
    reporte.append("RESUMEN DIARIO:")
    reporte.append(f"{'Día':>4} | {'Nodos':<20} | {'Cantidad':>10} | {'Envíos':>6}")
    reporte.append("-" * 60)
    
    for oleada in oleadas:
        nodos_str = ', '.join(oleada.nodos_que_reciben[:3])
        if len(oleada.nodos_que_reciben) > 3:
            nodos_str += f" +{len(oleada.nodos_que_reciben)-3}"
        reporte.append(f"{oleada.dia:>4} | {nodos_str:<20} | {oleada.cantidad_total:>10.1f} | {len(oleada.envios):>6}")
    
    reporte.append("")
    reporte.append("ESTADÍSTICAS:")
    
    # Calcular estadísticas
    total_envios = sum(len(o.envios) for o in oleadas)
    total_cantidad = sum(o.cantidad_total for o in oleadas)
    promedio_diario = total_cantidad / dias if dias > 0 else 0
    
    reporte.append(f"  Total envíos: {total_envios}")
    reporte.append(f"  Total cantidad: {total_cantidad:.1f} toneladas")
    reporte.append(f"  Promedio diario: {promedio_diario:.1f} toneladas")
    
    # Inventario en tránsito
    inventario = cadena.calcular_inventario_transito(oleadas)
    if inventario:
        promedio_transito = sum(inventario.values()) / len(inventario)
        reporte.append(f"  Inventario en tránsito promedio: {promedio_transito:.1f} toneladas")
    
    reporte.append("")
    reporte.append("=" * 60)
    
    return "\n".join(reporte)


if __name__ == "__main__":
    demostracion_completa()
    
    # Ejemplo de reporte
    print("\n" + "="*80)
    print("GENERACIÓN DE REPORTE")
    print("="*80)
    
    cadena_reporte = crear_cadena_suministro_ejemplo()
    reporte = generar_reporte_oleadas(cadena_reporte, "CD", 7)
    print(reporte)
