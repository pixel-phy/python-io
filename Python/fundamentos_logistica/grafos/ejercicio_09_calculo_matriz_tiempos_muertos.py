"""Ejercicio 09: Cálculo de Matriz de Tiempos Muertos

En una planta de manufactura flexible, pasar de producir el producto i al producto j 
requiere un tiempo de configuración (setup time). Se te da la estructura como una Lista de 
Adyacencia: Origen: [(Destino, Tiempo)]. Construye la Matriz de Adyacencia correspondiente.
Si no hay transición directa entre dos productos, el tiempo de configuración debe ser infinito
(float('inf')). """

def lista_a_matriz_adyacencia(lista_adyacencia, num_productos=None, etiquetas=None):
    """
    Convierte una Lista de Adyacencia en una Matriz de Adyacencia N x N.
    
    Args:
        lista_adyacencia (dict): Diccionario donde cada clave es un producto origen,
                                 y su valor es una lista de tuplas (destino, tiempo_setup)
        num_productos (int, optional): Número total de productos (N). 
                                       Si es None, se infiere de las claves.
        etiquetas (list, optional): Lista de etiquetas para ordenar los productos.
                                    Si es None, usa sorted() de las claves.
    
    Returns:
        list: Matriz N x N donde matriz[i][j] = tiempo de setup de i a j,
              o float('inf') si no hay transición directa.
    
    Raises:
        ValueError: Si hay inconsistencias en los datos
    """
    # Si no se especifican etiquetas, usar las claves del diccionario ordenadas
    if etiquetas is None:
        etiquetas = sorted(lista_adyacencia.keys())
    
    n = len(etiquetas)
    
    # Verificar que el número de productos coincide
    if num_productos is not None and num_productos != n:
        raise ValueError(f"num_productos ({num_productos}) no coincide con las etiquetas ({n})")
    
    # Crear mapa de etiqueta -> índice
    indice = {etiqueta: i for i, etiqueta in enumerate(etiquetas)}
    
    # Inicializar matriz con infinito (sin conexión)
    matriz = [[float('inf')] * n for _ in range(n)]
    
    # Llenar la diagonal con 0 (transición de un producto a sí mismo)
    # Nota: Generalmente el tiempo de setup de i a i es 0
    for i in range(n):
        matriz[i][i] = 0
    
    # Procesar cada nodo origen
    for origen, destinos in lista_adyacencia.items():
        if origen not in indice:
            raise ValueError(f"El origen '{origen}' no está en la lista de etiquetas")
        
        i = indice[origen]
        
        # Procesar cada conexión
        for destino, tiempo in destinos:
            if destino not in indice:
                raise ValueError(f"El destino '{destino}' no está en la lista de etiquetas")
            
            j = indice[destino]
            
            # Validar que el tiempo sea positivo
            if tiempo < 0:
                raise ValueError(f"Tiempo de setup negativo: {tiempo} para {origen}->{destino}")
            
            matriz[i][j] = tiempo
    
    return matriz


# Función de ayuda para visualizar la matriz

def imprimir_matriz(matriz, etiquetas=None, decimales=2):
    """Imprime la matriz de forma legible."""
    n = len(matriz)
    
    if etiquetas is None:
        etiquetas = [f"P{i}" for i in range(n)]
    
    # Encabezado
    print("      " + "  ".join(f"{et:>8}" for et in etiquetas))
    print("-" * (9 + 10 * n))
    
    for i, fila in enumerate(matriz):
        # Mostrar los valores
        valores = []
        for val in fila:
            if val == float('inf'):
                valores.append("    ∞")
            else:
                valores.append(f"{val:>8.2f}" if isinstance(val, float) else f"{val:>8}")
        
        print(f"{etiquetas[i]:>4} |" + "  ".join(valores))


# Prueba
if __name__ == "__main__":
    # Lista de adyacencia: tiempos de setup entre productos
    # Formato: Origen: [(Destino, Tiempo_setup)]
    lista_ejemplo = {
        'A': [('B', 5.0), ('C', 3.0)],          # De A a B tarda 5, a C tarda 3
        'B': [('A', 4.0), ('C', 2.0), ('D', 7.0)],
        'C': [('A', 6.0), ('D', 1.5)],
        'D': [('A', 2.0), ('B', 3.0)]           # No tiene conexión directa a C
    }
    
    # Convertir a matriz
    print("--- CONVERSIÓN A MATRIZ DE ADYACENCIA ---\n")
    matriz = lista_a_matriz_adyacencia(lista_ejemplo)
    imprimir_matriz(matriz, etiquetas=['A', 'B', 'C', 'D'])
    
    print("\n")
    
    # Acceso directo a la matriz
    print("Acceso a valores específicos:")
    print(f"  A -> B: {matriz[0][1]}  (índices 0->1)")
    print(f"  C -> D: {matriz[2][3]}  (índices 2->3)")
    print(f"  D -> C: {matriz[3][2]}  (infinito, no hay conexión)")
    
    print("\n")
    
    # Otro ejemplo con productos numéricos
    lista_numerica = {
        0: [(1, 10), (2, 15)],
        1: [(0, 12), (2, 8)],
        2: [(0, 5)]
    }
    
    matriz_num = lista_a_matriz_adyacencia(lista_numerica)
    print("Matriz con productos numéricos:")
    imprimir_matriz(matriz_num, etiquetas=[0, 1, 2])
