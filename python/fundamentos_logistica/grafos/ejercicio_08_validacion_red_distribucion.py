"""Ejercicio 08: Validación de Red de Distribución

Un data scientist nos entrega una matriz de adyacencia de N x N que representa los costos de 
transporte de un centro de distribución a varios clientes. Escribe una función que convierta
esa Matriz de Adyacencia en una Lista de Adyacencia (usando diccionarios de Python) para
alimentar un algoritmo de rutas. Debes omitis las conexiones inexistentes (representadas con costo 0 o inf). """

def matriz_a_lista_adyacencia(matriz, etiquetas=None):
    """
    Convierte una matriz de adyacencia N x N en una lista de adyacencia 
    usando diccionarios de Python.
    
    Args:
        matriz (list): Matriz de adyacencia N x N con costos de transporte
        etiquetas (list, optional): Lista de etiquetas para los nodos.
                                   Si es None, usa índices numéricos.
    
    Returns:
        dict: Diccionario donde cada clave es un nodo y su valor es otro
              diccionario {nodo_destino: costo} con las conexiones existentes
    """
    n = len(matriz)
    
    # Si no se proporcionan etiquetas, usar índices numéricos
    if etiquetas is None:
        etiquetas = list(range(n))
    elif len(etiquetas) != n:
        raise ValueError("El número de etiquetas debe coincidir con el tamaño de la matriz")
    
    # Inicializar diccionario vacío para cada nodo
    lista_adyacencia = {etiqueta: {} for etiqueta in etiquetas}
    
    # Recorrer la matriz
    for i in range(n):
        for j in range(n):
            costo = matriz[i][j]
            
            # Omitir conexiones inexistentes (0, inf o None)
            if costo is not None and costo != 0 and costo != float('inf'):
                origen = etiquetas[i]
                destino = etiquetas[j]
                lista_adyacencia[origen][destino] = costo
    
    return lista_adyacencia


# EJEMPLO DE USO
if __name__ == "__main__":
    # Matriz de adyacencia 4x4 con costos de transporte
    # Filas: origen, Columnas: destino
    # 0 = sin conexión, inf = sin conexión
    matriz_ejemplo = [
        [0, 10, 0, 30],      # Nodo 0 -> 1 (10), 3 (30)
        [10, 0, 20, 0],      # Nodo 1 -> 0 (10), 2 (20)
        [0, 20, 0, 15],      # Nodo 2 -> 1 (20), 3 (15)
        [30, 0, 15, 0]       # Nodo 3 -> 0 (30), 2 (15)
    ]
    
    # Con etiquetas personalizadas (centros/clientes)
    nodos = ["Centro", "ClienteA", "ClienteB", "ClienteC"]
    
    lista = matriz_a_lista_adyacencia(matriz_ejemplo, nodos)
    
    print("Lista de Adyacencia:")
    for origen, destinos in lista.items():
        print(f"  {origen} -> {destinos}")
    
    print("\n")
    
    # Con etiquetas numéricas por defecto
    lista_numerica = matriz_a_lista_adyacencia(matriz_ejemplo)
    print("Lista de Adyacencia (índices numéricos):")
    for origen, destinos in lista_numerica.items():
        print(f"  {origen} -> {destinos}")
