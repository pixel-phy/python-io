"""Ejercicio 26: Validación de Redes de Proyectos (CPM)

En la gestión de proyectos mediante el Método de la Ruta crítica (CPM), las actividades tienen que ser 
secuenciales y no pueden contener ciclos (no puedes empezar a techar si no has hecho los cimientos, 
y los cimientos no pueden depender del techo).
    - Modifica el método de detección de ciclos que, en lugar de solo devolver True o False, devuelva
    la lista exacta de nodos que forman el primer bucle cerrado (ciclo) detectado en la secuencia de 
    producción para poder alertar al ingeniero de planta. """

def detectar_ciclo_cpm(grafo):
    """
    Detecta el primer ciclo en un grafo dirigido (red CPM).
    
    Args:
        grafo: Diccionario {nodo: [lista_de_vecinos]}
    
    Returns:
        Lista de nodos que forman el ciclo, o lista vacía si no hay ciclo.
    """
    # Estados: 0 = no visitado, 1 = en proceso, 2 = completado
    estado = {nodo: 0 for nodo in grafo}
    camino_actual = []  # Para rastrear el camino DFS actual
    
    def dfs(nodo):
        # Marcar como en proceso
        estado[nodo] = 1
        camino_actual.append(nodo)
        
        # Explorar vecinos
        for vecino in grafo.get(nodo, []):
            if estado[vecino] == 0:
                # Si encontramos ciclo en la recursión, lo propagamos
                resultado = dfs(vecino)
                if resultado:
                    return resultado
            elif estado[vecino] == 1:
                # ¡Ciclo detectado! vecino está en el camino actual
                # Extraer el ciclo desde vecino hasta el final del camino
                indice = camino_actual.index(vecino)
                ciclo = camino_actual[indice:] + [vecino]  # Cerramos el ciclo
                return ciclo
        
        # Marcar como completado y salir del camino
        estado[nodo] = 2
        camino_actual.pop()
        return None
    
    # Probar todos los nodos (por si el grafo no es conexo)
    for nodo in grafo:
        if estado[nodo] == 0:
            resultado = dfs(nodo)
            if resultado:
                return resultado
    
    return []  # No hay ciclo

# Ejemplo de uso con un grafo que tiene ciclo
grafo_con_ciclo = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': ['D'],
    'D': ['E'],
    'E': ['B']  # Este arco crea el ciclo B-D-E-B
}

grafo_sin_ciclo = {
    'Cimientos': ['Paredes'],
    'Paredes': ['Tejado'],
    'Tejado': ['Pintura'],
    'Pintura': []
}

print("=== Prueba 1: Grafo con ciclo ===")
ciclo = detectar_ciclo_cpm(grafo_con_ciclo)
if ciclo:
    print(f"Ciclo detectado: {' -> '.join(ciclo)}")
else:
    print("No se detectaron ciclos")

print("\n=== Prueba 2: Grafo sin ciclo (CPM válido) ===")
ciclo = detectar_ciclo_cpm(grafo_sin_ciclo)
if ciclo:
    print(f"Ciclo detectado: {' -> '.join(ciclo)}")
else:
    print("No se detectaron ciclos - Red CPM válida")
