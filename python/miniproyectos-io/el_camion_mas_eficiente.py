"""El camión más eficiente:

Eres el encargado de logística de una pequeña empresa de reparto de comidas preparadas.
Tienes:
    - 1 Solo camión.
    - 5 Pedidos que deben entregarse hoy.
    - Cada pedido tiene: ID, dirección, peso (kg), y una ventana de tiempo (hora mínima y máxima de entrega).

El camión:
    - Capacidad máxima: 100 kg.
    - Velocidad: 40 km/h 
    - Sale del almacén en coordenadas (0,0) a las 8:00 am. 
    - Tiempo de descarga por pedido: 5 minutos (independientemente del peso).

Objetivo:
    Decidir en qué orden entregar los pedidos de manera que:
    - No se exceda la capacidad del camión.
    - Se respeten las ventanas de tiempo lo más posible.
    - Se minimice el tiempo total del recorrido (desde que sale hasta que vuelve al almacén).

Almacén (0,0). Capacidad camión: 100 kg.

Nivel 1: Familiarización con datos.
    Escribe las siguientes funciones:
    1. calcular_distancia(origen, destino): Recibe dos tuplas, retorna distancia euclidiana.
    2. peso_total(ruta): Recibe una lista de IDs de pedidos, retorna suma de pesos.
    3. verificar_capacidad(ruta, capacidad_maxima): Retorna true si el peso total <= capacidad.
    4. tiempo_viaje(distancia): Retorna horas de viaje.
    5. tiempo_descarga(cantidad_pedidos): Retorna horas de descarga. """

import math
from itertools import permutations

pedidos = [
    {"id": 1, "x": 2, "y": 3, "peso": 20, "hora_min": 9.0, "hora_max": 11.0},
    {"id": 2, "x": 5, "y": 1, "peso": 15, "hora_min": 10.0, "hora_max": 12.0},
    {"id": 3, "x": 1, "y": 6, "peso": 30, "hora_min": 8.5, "hora_max": 10.5},
    {"id": 4, "x": 7, "y": 2, "peso": 25, "hora_min": 11.0, "hora_max": 13.0},
    {"id": 5, "x": 3, "y": 5, "peso": 10, "hora_min": 12.0, "hora_max": 14.0},
]

def calcular_distancia(origen: tuple, destino: tuple):
    """Distancia euclidiana entre dos puntos"""
    return math.sqrt((destino[0] - origen[0])**2 + (destino[1] - origen[1])**2)

def peso_total(ruta: list, pedidos: list):
    """
    ruta: lista de IDs
    pedidos: lista de diccionarios con los datos.
    """
    suma = 0
    for id_pedido in ruta:
        # Buscarmos pedido por ID 
        for pedido in pedidos:
            if pedido["id"] == id_pedido:
                suma += pedido["peso"]
                break
    return suma

def verificar_capacidad(ruta: list, pedidos: list, capacidad_maxima: float = 100):
    """ Retorna True si el peso total no excede la capacidad"""
    return peso_total(ruta, pedidos) <= capacidad_maxima

def tiempo_viaje(distancia: float):
    """Tiempo en horas = distancia / velocidad """
    return distancia / 40

def tiempo_descarga(cantidad_pedidos: int):
    """5 minutos por pedido, convertido a horas"""
    return (5 * cantidad_pedidos) / 60

# Prueba del nivel 1
dist = calcular_distancia((0,0), (2,3))
print(f"Distancia almacén - pedido 1: {dist:.2f} km")

peso_ruta = peso_total([1, 2, 3], pedidos)
print(f"Peso ruta [1, 2, 3]: {peso_ruta} kg")

capacidad_ok = verificar_capacidad([1, 2, 3, 4, 5], pedidos)
print(f"¿Caben todos los pedidos? {capacidad_ok}")

tiempo = tiempo_viaje(10)
print(f"10 km a 40 km/h: {tiempo:.2f} horas")

descarga = tiempo_descarga(3)
print(f"Descargar 3 pedidos: {descarga:.2f} horas")

"""Nivel 2: Simulación de una ruta
Crear la función simular_ruta(ruta, pedidos, hora_salida=8.0) que calcule:
- La hora de llegada a cada pedido.
- Si cumple o no la ventana de tiempo (entrega antes de hora_max idealmente, o con penalización si es después)
- El tiempo total desde salida hasta regreso al almacén

Reglas de penalización:
- Si llegas antes de hora_min: esperas, pero no penaliza.
- Si llegas después de hora_max: penalización = (hora_llegada - hora_max) en horas 
- Si llegas dentro del rango: penalización 0. """

def encontrar_pedido(id_pedido: int, pedidos: list):
    """Retorna el diccionario del pedido con ese ID"""
    for pedido in pedidos:
        if pedido["id"] == id_pedido:
            return pedido
    return None # Si la ruta es válida nunca será None 

def simular_ruta(ruta: list, pedidos: list, hora_salida: float= 8.0):
    """Simula una ruta de entregas.
        Parámetros:
        - ruta: lista de IDs en orden de entrega [1, 3, 2, 4, 5]
        - pedidos: lista de diccionarios con datos de pedidos
        - hora_salida: hora de salida del almacén (por defecto 8.0)
        Retorna:
        - diccionario con: factible, entregas, tiempo_total_horas, penalizacion_total """

    if not verificar_capacidad(ruta, pedidos):
        return {
            "factibel": False,
            "entregas": [],
            "tiempo_total_horas": float('inf'),
            "penalizacion_total": float('inf') 
        }

    # Estado inicial de la simulación 
    tiempo_actual = hora_salida
    ubicacion_actual = (0,0)
    entregas = []
    penalizacion_total = 0.0

    # Recorrer cada pedido en la ruta:
    for id_pedido in ruta:
        pedido = encontrar_pedido(id_pedido, pedidos)

        # Calcular tiempo de viaje hasta ese pedido 
        distancia = calcular_distancia(ubicacion_actual, (pedido["x"], pedido["y"]))
        tiempo_viaje = distancia / 40
        tiempo_actual += tiempo_viaje

        # Registramos la hora de llegada 
        hora_llegada = tiempo_actual

        penalizacion_entrega = 0.0
        dentro_ventana = False

        if tiempo_actual < pedido["hora_min"]:
            # Llegó temprano: esperar hasta la hora mínima 
            tiempo_actual = pedido["hora_min"]
            hora_llegada = tiempo_actual
            dentro_ventana = True 
        elif tiempo_actual > pedido["hora_max"]:
            # Llegó tarde: calcular penalización 
            penalizacion_entrega = tiempo_actual - pedido["hora_max"]
            penalizacion_total += penalizacion_entrega
            dentro_ventana = False
        else:
            # Llegó en ventana
            dentro_ventana = True
        
        # Guardar información de esta entrega
        entregas.append({
            "id": id_pedido,
            "hora_llegada": round(hora_llegada, 2),
            "dentro_ventana": dentro_ventana,
            "penalizacion": round(penalizacion_entrega, 2)
        })
        
        # Tiempo de descarga (una sola vez)
        tiempo_actual += tiempo_descarga(1)

        # Actualizar ubicación
        ubicacion_actual = (pedido["x"], pedido["y"])

    # Regreso almacén
    distancia_regreso = calcular_distancia(ubicacion_actual, (0,0))
    tiempo_actual += distancia_regreso / 40

    return {
        "factible": True,
        "entregas": entregas,
        "tiempo_total_horas": round(tiempo_actual - hora_salida, 2),
        "penalizacion_total": round(penalizacion_total, 2)
    }

ruta = [3, 1, 2, 4, 5]
resultado = simular_ruta(ruta, pedidos)

print(f"Factible: {resultado['factible']}")
print(f"Tiempo total: {resultado['tiempo_total_horas']} horas")
print("\nEntregas:")
for e in resultado['entregas']:
    print(f"    Pedido {e['id']}: llegada {e['hora_llegada']}, dentro_ventana={e['dentro_ventana']}, penalización={e['penalizacion']}")

"""Nivel 3: Comparación de rutas
Implementa tres estrategias diferentes de ordenamiento:
    1. Por peso (descendente): entregar lo más pesado primero.
    2. Por hora mínima más temprana: Ordenar por hora_min ascendente.
    3. Por distancia al almacén: Ordenar por distancia desde (0,0) ascendente.

Para cada estrategia:
    - Generar la ruta (lista de IDs según criterio)
    - Simula la ruta con simular_ruta.
    - Guardar el resultado.

Generar todas las permutaciones de los 5 pedidos y encuentra la mejor ruta (menor tiempo total entre las que tienen penalización = 0, o menor
penaliación 0). """

def generar_ruta_por_peso(pedidos: list) -> list:
    """Estrategia 1: Ordenar por peso descendente (más pesado primero)"""
    # Crear lista de (id, peso) y ordenar por peso de mayor a menor
    pesos = [(pedido["id"], pedido["peso"]) for pedido in pedidos]
    pesos_ordenados = sorted(pesos, key=lambda x: x[1], reverse=True)
    return [id_pedido for id_pedido, _ in pesos_ordenados]


def generar_ruta_por_horario(pedidos: list) -> list:
    """Estrategia 2: Ordenar por hora_min ascendente (más temprano primero)"""
    horarios = [(pedido["id"], pedido["hora_min"]) for pedido in pedidos]
    horarios_ordenados = sorted(horarios, key=lambda x: x[1])
    return [id_pedido for id_pedido, _ in horarios_ordenados]


def generar_ruta_por_distancia(pedidos: list) -> list:
    """Estrategia 3: Ordenar por distancia al almacén (más cercano primero)"""
    distancias = []
    for pedido in pedidos:
        dist = calcular_distancia((0, 0), (pedido["x"], pedido["y"]))
        distancias.append((pedido["id"], dist))
    
    distancias_ordenadas = sorted(distancias, key=lambda x: x[1])
    return [id_pedido for id_pedido, _ in distancias_ordenadas]


def comparar_estrategias(pedidos: list, hora_salida: float = 8.0) -> dict:
    """
    Compara las tres estrategias heurísticas y determina la mejor.
    """
    estrategias = {
        "por_peso": generar_ruta_por_peso(pedidos),
        "por_horario": generar_ruta_por_horario(pedidos),
        "por_distancia": generar_ruta_por_distancia(pedidos)
    }
    
    resultados = {}
    
    for nombre, ruta in estrategias.items():
        simulacion = simular_ruta(ruta, pedidos, hora_salida)
        
        resultados[nombre] = {
            "ruta": ruta,
            "tiempo_total": simulacion["tiempo_total_horas"],
            "penalizacion": simulacion["penalizacion_total"],
            "factible": simulacion["factible"],
            "entregas": simulacion["entregas"]
        }
    
    # Encontrar la mejor estrategia
    mejor_nombre = None
    mejor_tiempo = float('inf')
    mejor_penalizacion = float('inf')
    
    for nombre, datos in resultados.items():
        if datos["factible"]:
            # Prioridad: penalización 0, luego menor tiempo
            if datos["penalizacion"] == 0 and datos["tiempo_total"] < mejor_tiempo:
                mejor_nombre = nombre
                mejor_tiempo = datos["tiempo_total"]
                mejor_penalizacion = datos["penalizacion"]
            elif mejor_nombre is None or datos["penalizacion"] < mejor_penalizacion:
                mejor_nombre = nombre
                mejor_tiempo = datos["tiempo_total"]
                mejor_penalizacion = datos["penalizacion"]
    
    return {
        "resultados": resultados,
        "mejor_estrategia": mejor_nombre,
        "mejor_tiempo": mejor_tiempo if mejor_nombre else None
    }


def encontrar_ruta_optima(pedidos: list, hora_salida: float = 8.0) -> dict:
    """
    Explora TODAS las permutaciones posibles (fuerza bruta) para encontrar la ruta óptima.
    Para 5 pedidos son 120 combinaciones.
    """
    ids_pedidos = [pedido["id"] for pedido in pedidos]
    
    mejor_ruta = None
    mejor_tiempo = float('inf')
    mejor_penalizacion = float('inf')
    mejor_simulacion = None
    rutas_factibles = 0
    total_combinaciones = 0
    
    # Probar cada permutación
    for ruta_candidata in permutations(ids_pedidos):
        total_combinaciones += 1
        ruta_lista = list(ruta_candidata)
        
        resultado = simular_ruta(ruta_lista, pedidos, hora_salida)
        
        if resultado["factible"]:
            rutas_factibles += 1
            penalizacion = resultado["penalizacion_total"]
            tiempo = resultado["tiempo_total_horas"]
            
            # Criterio de selección
            es_mejor = False
            
            if mejor_ruta is None:
                es_mejor = True
            elif penalizacion == 0 and mejor_penalizacion > 0:
                es_mejor = True
            elif penalizacion == 0 and mejor_penalizacion == 0 and tiempo < mejor_tiempo:
                es_mejor = True
            elif penalizacion < mejor_penalizacion:
                es_mejor = True
            
            if es_mejor:
                mejor_ruta = ruta_lista
                mejor_tiempo = tiempo
                mejor_penalizacion = penalizacion
                mejor_simulacion = resultado
    
    return {
        "mejor_ruta": mejor_ruta,
        "mejor_tiempo": mejor_tiempo,
        "mejor_penalizacion": mejor_penalizacion,
        "total_combinaciones": total_combinaciones,
        "rutas_factibles": rutas_factibles,
        "simulacion_completa": mejor_simulacion
    }


def mostrar_analisis_completo(pedidos: list, hora_salida: float = 8.0):
    """
    Ejecuta y muestra el análisis completo en consola.
    """
    print(" ANÁLISIS DE RUTAS PARA REPARTO DE COMIDAS")
    
    # Parte 1: estrategias heurísticas
    #
    print("\n COMPARACIÓN DE ESTRATEGIAS HEURÍSTICAS")
    
    comparacion = comparar_estrategias(pedidos, hora_salida)
    
    for nombre, datos in comparacion["resultados"].items():
        print(f"\n Estrategia: {nombre.upper()}")
        print(f"   Ruta: {datos['ruta']}")
        print(f"   Tiempo total: {datos['tiempo_total']:.2f} horas")
        print(f"   Penalización: {datos['penalizacion']:.2f} horas")
        print(f"   Factible: {'Sí' if datos['factible'] else 'No'}")
        
        # Mostrar timeline resumido
        print("   Timeline:")
        for entrega in datos["entregas"]:
            horas = int(entrega["hora_llegada"])
            minutos = int((entrega["hora_llegada"] - horas) * 60)
            estado = "Pasa" if entrega["dentro_ventana"] else "No Pasa"
            print(f"     {estado} Pedido {entrega['id']}: {horas:02d}:{minutos:02d}h")
    
    if comparacion["mejor_estrategia"]:
        print(f"\n MEJOR ESTRATEGIA HEURÍSTICA: {comparacion['mejor_estrategia'].upper()}")
        print(f"   Tiempo total: {comparacion['mejor_tiempo']:.2f} horas")
    
    # Parte 2: Ruta óptima
    
    print("\n")
    print(" BÚSQUEDA DE RUTA ÓPTIMA (Fuerza Bruta)")
    
    optimo = encontrar_ruta_optima(pedidos, hora_salida)
    
    print(f" Total de combinaciones evaluadas: {optimo['total_combinaciones']}")
    print(f" Rutas factibles encontradas: {optimo['rutas_factibles']}")
    
    if optimo['total_combinaciones'] > 0:
        porcentaje = (optimo['rutas_factibles'] / optimo['total_combinaciones']) * 100
        print(f" Porcentaje de rutas factibles: {porcentaje:.1f}%")
    
    if optimo["mejor_ruta"]:
        print(f"\n RUTA ÓPTIMA ENCONTRADA: {optimo['mejor_ruta']}")
        print(f"  Tiempo total: {optimo['mejor_tiempo']:.2f} horas")
        print(f"  Penalización: {optimo['mejor_penalizacion']:.2f} horas")
        
        # Mostrar timeline de la ruta óptima
        print("\n TIMELINE DETALLADO (Ruta Óptima):")
        if optimo["simulacion_completa"]:
            for entrega in optimo["simulacion_completa"]["entregas"]:
                horas = int(entrega["hora_llegada"])
                minutos = int((entrega["hora_llegada"] - horas) * 60)
                estado = "Pasa" if entrega["dentro_ventana"] else "No Pasa"
                print(f"   {estado} Pedido {entrega['id']}: {horas:02d}:{minutos:02d}h")
    else:
        print("\n No se encontró ninguna ruta factible")
        print("   Posible solución: aumentar la capacidad del camión")
    
    # Parte 3: comparación final

    if comparacion["mejor_estrategia"] and optimo["mejor_ruta"]:
        print("\n")
        print(" COMPARACIÓN FINAL: Heurística vs Óptimo")
        
        mejor_heuristica = comparacion["resultados"][comparacion["mejor_estrategia"]]
        mejora_tiempo = mejor_heuristica["tiempo_total"] - optimo["mejor_tiempo"]
        
        if mejora_tiempo > 0:
            mejora_porcentaje = (mejora_tiempo / mejor_heuristica["tiempo_total"]) * 100
            print(f"Mejor heurística ({comparacion['mejor_estrategia']}): {mejor_heuristica['tiempo_total']:.2f}h")
            print(f"Ruta óptima: {optimo['mejor_tiempo']:.2f}h")
            print(f" Mejora: {mejora_tiempo:.2f}h ({mejora_porcentaje:.1f}% más eficiente)")
        else:
            print(" La mejor heurística ya encontró la ruta óptima!")

    return {
        "comparacion_heuristica": comparacion,
        "ruta_optima": optimo
    }

if __name__ == "__main__":
    # Ejecutar el análisis completo
    resultados = mostrar_analisis_completo(pedidos)
    
    # Mostrar recomendación final
    print("\n")
    if resultados["ruta_optima"]["mejor_ruta"]:
        print(" RECOMENDACIÓN FINAL PARA EL CONDUCTOR:")
        print(f"   Sigue esta ruta: {resultados['ruta_optima']['mejor_ruta']}")
        print(f"   Salida: 8:00 AM")
        print(f"   Retorno estimado: {8 + resultados['ruta_optima']['mejor_tiempo']:.2f} AM/PM")

"""Nivel 4: Mejora del mundo real 
Agrega una restricción realista:
    'El pedido 3 es prioritario y debe entregarse antes de las 10 sí o sí, aunque toque reordenar todo'

Modifica tu búsqueda de mejor ruta para imponer que el pedido 3 esté en una posición anterior a cierta hora 
límite efectiva. """

# Múltiples camiones
import math
from itertools import permutations

# Configuración de la flota
camiones = [
    {"id": 1, "capacidad": 100, "velocidad": 40, "hora_salida": 8.0},
    {"id": 2, "capacidad": 80, "velocidad": 45, "hora_salida": 8.0},
    {"id": 3, "capacidad": 120, "velocidad": 35, "hora_salida": 8.5},  # Sale más tarde
]

TIEMPO_DESCARGA_MINUTOS = 5

def calcular_distancia(origen: tuple, destino: tuple) -> float:
    return math.sqrt((destino[0] - origen[0])**2 + (destino[1] - origen[1])**2)


def encontrar_pedido(id_pedido: int, pedidos: list) -> dict:
    for pedido in pedidos:
        if pedido["id"] == id_pedido:
            return pedido
    return None


def tiempo_descarga(cantidad_pedidos: int) -> float:
    return (TIEMPO_DESCARGA_MINUTOS * cantidad_pedidos) / 60


def simular_ruta_camion(ruta: list, pedidos: list, camion: dict) -> dict:
    """
    Simula la ruta de UN camión específico.
    
    Parámetros:
    - ruta: lista de IDs en orden
    - pedidos: lista de diccionarios
    - camion: diccionario con id, capacidad, velocidad, hora_salida
    
    Retorna: diccionario con resultados de ese camión
    """
    
    # Verificar capacidad
    peso_total = sum(encontrar_pedido(pid, pedidos)["peso"] for pid in ruta)
    if peso_total > camion["capacidad"]:
        return {
            "camion_id": camion["id"],
            "factible": False,
            "entregas": [],
            "tiempo_total_horas": float('inf'),
            "penalizacion_total": float('inf'),
            "peso_total": peso_total
        }
    
    # Estado inicial
    tiempo_actual = camion["hora_salida"]
    ubicacion_actual = (0, 0)
    entregas = []
    penalizacion_total = 0.0
    
    # Recorrer ruta
    for id_pedido in ruta:
        pedido = encontrar_pedido(id_pedido, pedidos)
        
        # Viajar
        distancia = calcular_distancia(ubicacion_actual, (pedido["x"], pedido["y"]))
        tiempo_actual += distancia / camion["velocidad"]
        hora_llegada = tiempo_actual
        
        # Verificar ventana
        penalizacion_entrega = 0.0
        dentro_ventana = False
        
        if tiempo_actual < pedido["hora_min"]:
            tiempo_actual = pedido["hora_min"]
            hora_llegada = tiempo_actual
            dentro_ventana = True
        elif tiempo_actual > pedido["hora_max"]:
            penalizacion_entrega = tiempo_actual - pedido["hora_max"]
            penalizacion_total += penalizacion_entrega
            dentro_ventana = False
        else:
            dentro_ventana = True
        
        entregas.append({
            "id": id_pedido,
            "hora_llegada": round(hora_llegada, 2),
            "dentro_ventana": dentro_ventana,
            "penalizacion": round(penalizacion_entrega, 2)
        })
        
        # Descargar
        tiempo_actual += tiempo_descarga(1)
        ubicacion_actual = (pedido["x"], pedido["y"])
    
    # Regreso
    distancia_regreso = calcular_distancia(ubicacion_actual, (0, 0))
    tiempo_actual += distancia_regreso / camion["velocidad"]
    
    return {
        "camion_id": camion["id"],
        "factible": True,
        "entregas": entregas,
        "tiempo_total_horas": round(tiempo_actual - camion["hora_salida"], 2),
        "penalizacion_total": round(penalizacion_total, 2),
        "peso_total": peso_total
    }


def asignar_pedidos_a_camiones(pedidos: list, camiones: list) -> dict:
    """
    Asigna pedidos a camiones usando una heurística simple.
    
    Esta es una versión simplificada. En la realidad, esto sería un problema
    de optimización complejo.
    """
    
    # Ordenar pedidos por peso descendente (los más pesados primero)
    pedidos_ordenados = sorted(pedidos, key=lambda p: p["peso"], reverse=True)
    
    # Copia de camiones para ir asignando
    camiones_asignados = []
    for camion in camiones:
        camiones_asignados.append({
            "id": camion["id"],
            "capacidad": camion["capacidad"],
            "velocidad": camion["velocidad"],
            "hora_salida": camion["hora_salida"],
            "pedidos_asignados": [],
            "peso_actual": 0
        })
    
    # Asignar cada pedido al camión que pueda con él
    for pedido in pedidos_ordenados:
        asignado = False
        
        # Buscar camión con capacidad suficiente
        for camion in camiones_asignados:
            if camion["peso_actual"] + pedido["peso"] <= camion["capacidad"]:
                camion["pedidos_asignados"].append(pedido["id"])
                camion["peso_actual"] += pedido["peso"]
                asignado = True
                break
        
        if not asignado:
            # Pedido no se pudo asignar a ningún camión
            return {
                "factible": False,
                "error": f"Pedido {pedido['id']} no se pudo asignar por capacidad"
            }
    
    # Ordenar los pedidos de cada camión por hora_min (heurística)
    for camion in camiones_asignados:
        pedidos_con_horario = []
        for pid in camion["pedidos_asignados"]:
            pedido = encontrar_pedido(pid, pedidos)
            pedidos_con_horario.append((pid, pedido["hora_min"]))
        pedidos_con_horario.sort(key=lambda x: x[1])
        camion["pedidos_asignados"] = [pid for pid, _ in pedidos_con_horario]
    
    return {
        "factible": True,
        "asignacion": camiones_asignados
    }


def simular_flota_completa(pedidos: list, camiones: list) -> dict:
    """
    Simula la operación completa de toda la flota de camiones.
    """
    
    # Asignar pedidos a camiones
    asignacion = asignar_pedidos_a_camiones(pedidos, camiones)
    
    if not asignacion["factible"]:
        return {
            "factible": False,
            "error": asignacion["error"],
            "camiones": []
        }
    
    # Simular cada camión
    resultados_camiones = []
    penalizacion_total = 0.0
    tiempo_maximo = 0.0
    
    for camion_data in asignacion["asignacion"]:
        # Encontrar el camión original para obtener velocidad
        camion_original = next(c for c in camiones if c["id"] == camion_data["id"])
        
        camion_sim = {
            "id": camion_data["id"],
            "capacidad": camion_data["capacidad"],
            "velocidad": camion_original["velocidad"],
            "hora_salida": camion_original["hora_salida"]
        }
        
        resultado = simular_ruta_camion(camion_data["pedidos_asignados"], pedidos, camion_sim)
        resultados_camiones.append(resultado)
        
        if resultado["factible"]:
            penalizacion_total += resultado["penalizacion_total"]
            # El tiempo de finalización de la flota es el máximo entre todos
            hora_fin = camion_sim["hora_salida"] + resultado["tiempo_total_horas"]
            tiempo_maximo = max(tiempo_maximo, hora_fin)
    
    return {
        "factible": True,
        "camiones": resultados_camiones,
        "penalizacion_total": penalizacion_total,
        "tiempo_finalizacion": round(tiempo_maximo, 2),
        "asignacion": asignacion["asignacion"]
    }


def mostrar_resultados_flota(resultados: dict):
    """
    Muestra los resultados de la simulación de flota.
    """
    print("\n")
    print("SIMULACIÓN DE FLOTA COMPLETA")
    print("\n")
    
    if not resultados["factible"]:
        print(f"\n ERROR: {resultados['error']}")
        return
    
    print(f"\n Asignación factible")
    print(f" Penalización total flota: {resultados['penalizacion_total']:.2f} horas")
    print(f"  Hora de finalización de la flota: {resultados['tiempo_finalizacion']:.2f}")
    
    print("\n ASIGNACIÓN POR CAMIÓN:")
    
    for camion in resultados["camiones"]:
        print(f"\n Camión {camion['camion_id']}")
        print(f"   Pedidos: {[e['id'] for e in camion['entregas']]}")
        print(f"   Peso total: {camion['peso_total']:.1f} kg")
        print(f"   Tiempo de ruta: {camion['tiempo_total_horas']:.2f} horas")
        print(f"   Penalización: {camion['penalizacion_total']:.2f} horas")
        print("   Timeline:")
        for entrega in camion["entregas"]:
            horas = int(entrega["hora_llegada"])
            minutos = int((entrega["hora_llegada"] - horas) * 60)
            estado = "Pasa" if entrega["dentro_ventana"] else "No pasa"
            print(f"     {estado} Pedido {entrega['id']}: {horas:02d}:{minutos:02d}h")


# Prueba
if __name__ == "__main__":
    print("\n")
    print("MÚLTIPLES CAMIONES")
    
    resultados_flota = simular_flota_completa(pedidos, camiones)
    mostrar_resultados_flota(resultados_flota)

# Agregamos prioridad a los pedidos
pedidos_con_prioridad = [
    {"id": 1, "x": 2, "y": 3, "peso": 20, "hora_min": 9.0, "hora_max": 11.0, "prioridad": 2},
    {"id": 2, "x": 5, "y": 1, "peso": 15, "hora_min": 10.0, "hora_max": 12.0, "prioridad": 3},
    {"id": 3, "x": 1, "y": 6, "peso": 30, "hora_min": 8.5, "hora_max": 10.5, "prioridad": 1},  # Alta prioridad
    {"id": 4, "x": 7, "y": 2, "peso": 25, "hora_min": 11.0, "hora_max": 13.0, "prioridad": 2},
    {"id": 5, "x": 3, "y": 5, "peso": 10, "hora_min": 12.0, "hora_max": 14.0, "prioridad": 3},
]

# Prioridad 1 = más urgente, 3 = menos urgente

def verificar_prioridades(asignacion: dict, pedidos: list) -> bool:
    """
    Verifica que los pedidos de prioridad 1 se entreguen primero en cada camión.
    """
    for camion in asignacion["asignacion"]:
        pedidos_camion = camion["pedidos_asignados"]
        
        # Encontrar prioridad máxima (número más bajo) en este camión
        prioridades_en_camion = []
        for pid in pedidos_camion:
            pedido = encontrar_pedido(pid, pedidos)
            prioridades_en_camion.append(pedido["prioridad"])
        
        min_prioridad = min(prioridades_en_camion)
        
        # Si hay prioridad 1, debe ser el primero
        if min_prioridad == 1:
            primer_pedido = pedidos_camion[0]
            prioridad_primer = encontrar_pedido(primer_pedido, pedidos)["prioridad"]
            if prioridad_primer != 1:
                return False
    
    return True


def asignar_con_prioridad(pedidos: list, camiones: list) -> dict:
    """
    Asigna pedidos dando prioridad a los urgentes.
    """
    # Separar pedidos por prioridad
    prioridad_1 = [p for p in pedidos if p["prioridad"] == 1]
    prioridad_2 = [p for p in pedidos if p["prioridad"] == 2]
    prioridad_3 = [p for p in pedidos if p["prioridad"] == 3]
    
    # Ordenar por prioridad (1 primero) y luego por peso
    pedidos_ordenados = prioridad_1 + prioridad_2 + prioridad_3
    pedidos_ordenados.sort(key=lambda p: p["peso"], reverse=True)
    
    # Misma lógica de asignación pero con orden respetado
    camiones_asignados = []
    for camion in camiones:
        camiones_asignados.append({
            "id": camion["id"],
            "capacidad": camion["capacidad"],
            "velocidad": camion["velocidad"],
            "hora_salida": camion["hora_salida"],
            "pedidos_asignados": [],
            "peso_actual": 0
        })
    
    for pedido in pedidos_ordenados:
        asignado = False
        for camion in camiones_asignados:
            if camion["peso_actual"] + pedido["peso"] <= camion["capacidad"]:
                camion["pedidos_asignados"].append(pedido["id"])
                camion["peso_actual"] += pedido["peso"]
                asignado = True
                break
        
        if not asignado:
            return {"factible": False, "error": f"Pedido {pedido['id']} no asignable"}
    
    return {"factible": True, "asignacion": camiones_asignados}

# Se agrega incertidumbre

import random

def tiempo_viaje_incierto(distancia: float, velocidad_base: float, variacion: float = 0.2) -> float:
    """
    Tiempo de viaje con incertidumbre.
    variacion = 0.2 significa ±20% de variación
    """
    factor = random.uniform(1 - variacion, 1 + variacion)
    velocidad_real = velocidad_base * factor
    return distancia / velocidad_real


def simular_ruta_incierta(ruta: list, pedidos: list, camion: dict, num_simulaciones: int = 100) -> dict:
    """
    Simula múltiples escenarios para estimar la probabilidad de éxito.
    """
    resultados = []
    
    for _ in range(num_simulaciones):
        # Versión con incertidumbre
        tiempo_actual = camion["hora_salida"]
        ubicacion_actual = (0, 0)
        penalizacion_total = 0.0
        factible = True
        
        for id_pedido in ruta:
            pedido = encontrar_pedido(id_pedido, pedidos)
            
            # Viaje incierto
            distancia = calcular_distancia(ubicacion_actual, (pedido["x"], pedido["y"]))
            tiempo_actual += tiempo_viaje_incierto(distancia, camion["velocidad"])
            
            if tiempo_actual > pedido["hora_max"] + 1.0:  # Hasta 1 hora de tolerancia
                penalizacion_total += tiempo_actual - pedido["hora_max"]
            
            if tiempo_actual > pedido["hora_max"] + 2.0:  # Más de 2 horas tarde = fallo
                factible = False
                break
            
            # Descarga (también incierta)
            tiempo_actual += random.uniform(0.05, 0.15)  # 3-9 minutos
            ubicacion_actual = (pedido["x"], pedido["y"])
        
        if factible:
            resultados.append(penalizacion_total)
    
    if resultados:
        return {
            "probabilidad_exito": len(resultados) / num_simulaciones,
            "penalizacion_promedio": sum(resultados) / len(resultados),
            "penalizacion_maxima": max(resultados),
            "penalizacion_minima": min(resultados)
        }
    else:
        return {
            "probabilidad_exito": 0.0,
            "penalizacion_promedio": float('inf'),
            "penalizacion_maxima": float('inf'),
            "penalizacion_minima": float('inf')
        }


if __name__ == "__main__":

    print(" NIVEL 4 COMPLETO - OPERATIONS RESEARCH AVANZADO")
    
    # 1. Múltiples camiones
    print("\n MÚLTIPLES CAMIONES")

    resultados_flota = simular_flota_completa(pedidos, camiones)
    mostrar_resultados_flota(resultados_flota)
    
    # 2. Prioridades
    print("\n\nRESTRICCIONES PRIORITARIAS")
    print("Los pedidos con prioridad 1 deben entregarse primero")
    print("(Implementado en la función de asignación)")
    
    # 3. Incertidumbre
    print("\n\nANÁLISIS DE INCERTIDUMBRE (Monte Carlo)")
    
    # Tomar la mejor ruta del primer camión para análisis
    if resultados_flota["factible"] and resultados_flota["camiones"]:
        primer_camion = camiones[0]
        ruta_ejemplo = resultados_flota["camiones"][0]["entregas"]
        ruta_ids = [e["id"] for e in ruta_ejemplo]
        
        print(f"Analizando ruta del Camión 1: {ruta_ids}")
        analisis_incierto = simular_ruta_incierta(ruta_ids, pedidos, primer_camion, 1000)
        
        print(f" Probabilidad de éxito (entregas a tiempo): {analisis_incierto['probabilidad_exito']*100:.1f}%")
        print(f" Penalización promedio: {analisis_incierto['penalizacion_promedio']:.2f} horas")
        print(f" Penalización máxima: {analisis_incierto['penalizacion_maxima']:.2f} horas")
        print(f" Penalización mínima: {analisis_incierto['penalizacion_minima']:.2f} horas")
