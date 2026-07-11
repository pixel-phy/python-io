"""Ejercicio 29: Ventanas de Tiempo en Distribución

En problemas de optimización de rutas (VRPTW), cada nodo (cliente) tiene una ventana de tiempo de atención
[Ei, Li] donde Ei es la hora de apertura más temprana y Li la hora de cierre más tardía. Cada arista tiene un
'tiempo de viaje'. Si llegas antes de Ei, debes esperar. Si llegas después de Li, la ruta es inviable.
    - Implementar una variante de Dijkstra que encuentre el camino más rápido entre un centro de distribución
    y un cliente final, respetando las ventanas de tiempo de los nodos intermedios. Si violas una ventana Li,
    ese camino se vuelve inmediatamente inválido. """

import heapq

def encontrar_ruta_con_time_windows(grafo, tiempos_viaje, time_windows, origen, destino, hora_salida=0):
    """
    Encuentra la ruta más rápida respetando ventanas de tiempo.
    
    Args:
        grafo: Diccionario {nodo: [lista_vecinos]}
        tiempos_viaje: Diccionario {(origen, destino): tiempo}
        time_windows: Diccionario {nodo: (E_i, L_i)}
        origen: Nodo de inicio
        destino: Nodo final
        hora_salida: Hora de salida del origen
    
    Returns:
        Tupla (tiempo_total, [ruta], tiempos_llegada)
    """
    # Estado: (tiempo_llegada, nodo)
    # Usamos tiempo_llegada como distancia principal (minimizar)
    
    # Inicializar estructuras
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[origen] = hora_salida
    padres = {origen: None}
    tiempos_llegada_dict = {origen: hora_salida}
    cola_prioridad = [(hora_salida, origen)]
    visitados = set()
    
    # Validar ventana del origen
    E_origen, L_origen = time_windows[origen]
    if not (E_origen <= hora_salida <= L_origen):
        print(f"Error: Hora de salida {hora_salida} fuera de ventana [{E_origen}, {L_origen}]")
        return float('inf'), [], {}
    
    while cola_prioridad:
        tiempo_actual, nodo_actual = heapq.heappop(cola_prioridad)
        
        if nodo_actual in visitados:
            continue
        
        visitados.add(nodo_actual)
        
        # Si llegamos al destino, podemos parar (Dijkstra garantiza óptimo)
        if nodo_actual == destino:
            break
        
        # Explorar vecinos
        for vecino in grafo.get(nodo_actual, []):
            if vecino in visitados:
                continue
            
            # Calcular tiempo de llegada al vecino
            clave_viaje = (nodo_actual, vecino)
            if clave_viaje not in tiempos_viaje:
                continue
            
            tiempo_viaje = tiempos_viaje[clave_viaje]
            tiempo_llegada = tiempo_actual + tiempo_viaje
            
            # Verificar ventana de tiempo del vecino
            E_vecino, L_vecino = time_windows[vecino]
            
            # Si llegamos antes de E, esperamos hasta la apertura
            if tiempo_llegada < E_vecino:
                tiempo_llegada = E_vecino
            # Si llegamos después de L, ruta inválida
            elif tiempo_llegada > L_vecino:
                continue
            
            # Actualizar si encontramos mejor tiempo
            if tiempo_llegada < distancias[vecino]:
                distancias[vecino] = tiempo_llegada
                padres[vecino] = nodo_actual
                tiempos_llegada_dict[vecino] = tiempo_llegada
                heapq.heappush(cola_prioridad, (tiempo_llegada, vecino))
    
    # Verificar si hay ruta
    if distancias[destino] == float('inf'):
        return float('inf'), [], {}
    
    # Reconstruir ruta
    ruta = []
    tiempos_llegada_ruta = {}
    nodo = destino
    while nodo is not None:
        ruta.append(nodo)
        if nodo in tiempos_llegada_dict:
            tiempos_llegada_ruta[nodo] = tiempos_llegada_dict[nodo]
        nodo = padres.get(nodo)
    ruta.reverse()
    
    # Reconstruir tiempos en orden correcto
    tiempos_ordenados = [tiempos_llegada_ruta[nodo] for nodo in ruta]
    
    return distancias[destino], ruta, tiempos_ordenados

def mostrar_ruta_time_windows(ruta, tiempos_llegada, time_windows, tiempo_total):
    """Muestra la ruta con detalles de ventanas de tiempo."""
    if not ruta:
        print("No se encontró ruta válida")
        return
    
    print(f"\nRuta encontrada (tiempo total: {tiempo_total} unidades)")
    print(f"Ruta: {' -> '.join(ruta)}")
    print("\nDetalle de paradas:")
    
    for i, nodo in enumerate(ruta):
        E, L = time_windows[nodo]
        llegada = tiempos_llegada[i] if i < len(tiempos_llegada) else "N/A"
        
        if isinstance(llegada, (int, float)):
            espera = max(0, E - llegada) if i > 0 else 0
            if i == 0:
                print(f"  {i}. {nodo}: Ventana [{E}, {L}], Salida: {llegada}")
            else:
                estado = "OK" if E <= llegada <= L else "INVÁLIDA"
                print(f"  {i}. {nodo}: Ventana [{E}, {L}], Llegada: {llegada}, Espera: {espera}, Estado: {estado}")
        else:
            print(f"  {i}. {nodo}: Ventana [{E}, {L}]")

# ===== EJEMPLO DE USO =====

# Definir la red de distribución
# Grafo: conexiones entre nodos
grafo_distribucion = {
    'Deposito': ['Cliente1', 'Cliente2'],
    'Cliente1': ['Deposito', 'Cliente2', 'Cliente3'],
    'Cliente2': ['Deposito', 'Cliente1', 'Cliente3', 'Cliente4'],
    'Cliente3': ['Cliente1', 'Cliente2', 'Cliente4'],
    'Cliente4': ['Cliente2', 'Cliente3', 'Cliente5'],
    'Cliente5': ['Cliente4']
}

# Tiempos de viaje entre nodos (en minutos)
tiempos_viaje = {
    ('Deposito', 'Cliente1'): 15,
    ('Deposito', 'Cliente2'): 20,
    ('Cliente1', 'Deposito'): 15,
    ('Cliente1', 'Cliente2'): 10,
    ('Cliente1', 'Cliente3'): 25,
    ('Cliente2', 'Deposito'): 20,
    ('Cliente2', 'Cliente1'): 10,
    ('Cliente2', 'Cliente3'): 12,
    ('Cliente2', 'Cliente4'): 30,
    ('Cliente3', 'Cliente1'): 25,
    ('Cliente3', 'Cliente2'): 12,
    ('Cliente3', 'Cliente4'): 18,
    ('Cliente4', 'Cliente2'): 30,
    ('Cliente4', 'Cliente3'): 18,
    ('Cliente4', 'Cliente5'): 20,
    ('Cliente5', 'Cliente4'): 20
}

# Ventanas de tiempo [E_i, L_i] en minutos desde la salida
time_windows = {
    'Deposito': (0, 10),      # El depósito solo puede salir entre 0 y 10
    'Cliente1': (10, 30),
    'Cliente2': (15, 45),
    'Cliente3': (20, 50),
    'Cliente4': (35, 65),
    'Cliente5': (50, 80)
}

print("=" * 80)
print("RUTEO CON VENTANAS DE TIEMPO (TIME WINDOWS)")
print("=" * 80)

# Caso 1: Ruta válida con esperas
print("\nCaso 1: Ruta con esperas necesarias")
print("-" * 50)
tiempo_total, ruta, tiempos = encontrar_ruta_con_time_windows(
    grafo_distribucion, tiempos_viaje, time_windows, 
    'Deposito', 'Cliente5', 0
)
mostrar_ruta_time_windows(ruta, tiempos, time_windows, tiempo_total)

# Caso 2: Ruta inválida por violación de ventana
print("\nCaso 2: Intentando llegar demasiado tarde")
print("-" * 50)
# Forzar una salida tardía para mostrar violación de ventana
tiempo_total, ruta, tiempos = encontrar_ruta_con_time_windows(
    grafo_distribucion, tiempos_viaje, time_windows, 
    'Deposito', 'Cliente5', 10  # Salir en el límite de la ventana del depósito
)
mostrar_ruta_time_windows(ruta, tiempos, time_windows, tiempo_total)

# Caso 3: Demostración de diferentes rutas
print("\nCaso 3: Comparación de rutas alternativas")
print("-" * 50)
print("Ruta 1: Deposito -> Cliente1 -> Cliente2 -> Cliente4 -> Cliente5")
print("Ruta 2: Deposito -> Cliente2 -> Cliente3 -> Cliente4 -> Cliente5")

print("\nAnálisis de viabilidad de Ruta 1:")
tiempo = 0
for tramo in [('Deposito', 'Cliente1'), ('Cliente1', 'Cliente2'), 
              ('Cliente2', 'Cliente4'), ('Cliente4', 'Cliente5')]:
    tiempo += tiempos_viaje[tramo]
    destino = tramo[1]
    E, L = time_windows[destino]
    if tiempo < E:
        print(f"  Llegada a {destino} a tiempo {tiempo} - Esperar hasta {E}")
        tiempo = E
    elif tiempo <= L:
        print(f"  Llegada a {destino} a tiempo {tiempo} - OK")
    else:
        print(f"  Llegada a {destino} a tiempo {tiempo} - VIOLACIÓN (L={L})")
        break

print("\nAnálisis de viabilidad de Ruta 2:")
tiempo = 0
for tramo in [('Deposito', 'Cliente2'), ('Cliente2', 'Cliente3'), 
              ('Cliente3', 'Cliente4'), ('Cliente4', 'Cliente5')]:
    tiempo += tiempos_viaje[tramo]
    destino = tramo[1]
    E, L = time_windows[destino]
    if tiempo < E:
        print(f"  Llegada a {destino} a tiempo {tiempo} - Esperar hasta {E}")
        tiempo = E
    elif tiempo <= L:
        print(f"  Llegada a {destino} a tiempo {tiempo} - OK")
    else:
        print(f"  Llegada a {destino} a tiempo {tiempo} - VIOLACIÓN (L={L})")
        break

# Caso 4: Escenario con múltiples clientes
print("\nCaso 4: Encontrando ruta óptima a Cliente3")
print("-" * 50)
tiempo_total, ruta, tiempos = encontrar_ruta_con_time_windows(
    grafo_distribucion, tiempos_viaje, time_windows, 
    'Deposito', 'Cliente3', 0
)
mostrar_ruta_time_windows(ruta, tiempos, time_windows, tiempo_total)
