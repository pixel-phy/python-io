"""Ejercicio 03: Análisis de Densidad de una Red Logística

Crea una función que reciba una Lista de Adyacencia de una infraestructura de transporte y calcule
su densidad de red (D).

    D = E / (V(v-1)) Para grafos dirigidos

Donde E es el número de arcos y V el número de nodos. Si la densidad es menor al 15%, 
    la función debe emitir una recomendación explícita indicando que para futuros algoritmos se debe 
priorizar la Lista de Adyacencia sobre la matriz por eficiencia de memoria. """

def analizar_densidad_red(lista_adyacencia, es_dirigido=True, umbral=0.15):
    """
    Analiza la densidad de una red logística representada como lista de adyacencia.
    
    Args:
        lista_adyacencia (dict): Diccionario con origen -> [(destino, costo), ...]
        es_dirigido (bool): True para grafos dirigidos, False para no dirigidos
        umbral (float): Porcentaje mínimo de densidad para recomendar matriz (0.0 a 1.0)
    
    Returns:
        dict: Diccionario con métricas y recomendaciones:
            - V: Número de nodos
            - E: Número de arcos (conexiones)
            - E_posibles: Número máximo de arcos posibles
            - densidad: Densidad de la red (0.0 a 1.0)
            - porcentaje: Densidad en porcentaje
            - recomendacion: Mensaje con recomendación explícita
            - estructura_recomendada: 'matriz' o 'lista_adyacencia'
    """
    
    # Calcular número de nodos (V)
    V = len(lista_adyacencia)
    
    if V == 0:
        return {
            'V': 0,
            'E': 0,
            'E_posibles': 0,
            'densidad': 0.0,
            'porcentaje': '0.00%',
            'recomendacion': 'La red está vacía. No hay nodos para analizar.',
            'estructura_recomendada': 'lista_adyacencia'
        }
    
    # Contar arcos (E) - considerando que puede haber duplicados
    E = 0
    arcos_unicos = set()  # Para evitar contar arcos duplicados
    
    for origen, destinos in lista_adyacencia.items():
        for destino, _ in destinos:
            arco = (origen, destino)
            if arco not in arcos_unicos:
                arcos_unicos.add(arco)
                E += 1
    
    # Calcular el número máximo de arcos posibles
    # Para grafos dirigidos: V*(V-1)
    # Para grafos no dirigidos: V*(V-1)/2
    if es_dirigido:
        E_posibles = V * (V - 1)
        tipo_grafo = "dirigido"
    else:
        E_posibles = V * (V - 1) // 2
        tipo_grafo = "no dirigido"
    
    # Calcular densidad
    densidad = E / E_posibles if E_posibles > 0 else 0.0
    porcentaje = densidad * 100
    
    # Generar recomendación
    if densidad < umbral:
        recomendacion = (
            f" RECOMENDACIÓN: La densidad de la red es del {porcentaje:.2f}%, "
            f"menor al {umbral*100:.0f}% recomendado. "
            f"Para futuros algoritmos, PRIORIZA LA LISTA DE ADYACENCIA sobre la matriz "
            f"por eficiencia de memoria, ya que la red es dispersa "
            f"(solo {E} de {E_posibles} conexiones posibles)."
        )
        estructura_recomendada = 'lista_adyacencia'
    else:
        recomendacion = (
            f"La red tiene una densidad del {porcentaje:.2f}%, "
            f"mayor o igual al {umbral*100:.0f}% de umbral. "
            f"La matriz de adyacencia puede ser una opción viable "
            f"para algoritmos que requieran acceso rápido a las conexiones."
        )
        estructura_recomendada = 'matriz'
    
    return {
        'V': V,
        'E': E,
        'E_posibles': E_posibles,
        'densidad': densidad,
        'porcentaje': f"{porcentaje:.2f}%",
        'tipo_grafo': tipo_grafo,
        'recomendacion': recomendacion,
        'estructura_recomendada': estructura_recomendada
    }


# FUNCIÓN PARA GENERAR LISTAS DE ADYACENCIA DE EJEMPLO
def generar_red_ejemplo(tipo='dispersa', num_nodos=10):
    """Genera redes de ejemplo para probar la función."""
    import random
    
    if tipo == 'dispersa':
        # Red con ~10% de densidad
        lista = {i: [] for i in range(num_nodos)}
        for i in range(num_nodos):
            # Cada nodo se conecta a 1 o 2 nodos aleatorios
            num_conexiones = random.randint(1, 2)
            destinos = random.sample([j for j in range(num_nodos) if j != i], 
                                    min(num_conexiones, num_nodos - 1))
            for j in destinos:
                lista[i].append((j, random.randint(1, 100)))
        return lista
    
    elif tipo == 'densa':
        # Red con ~80% de densidad
        lista = {i: [] for i in range(num_nodos)}
        for i in range(num_nodos):
            for j in range(num_nodos):
                if i != j and random.random() < 0.8:
                    lista[i].append((j, random.randint(1, 100)))
        return lista
    
    elif tipo == 'completa':
        # Red completamente conectada (100% densidad)
        lista = {i: [(j, random.randint(1, 100)) 
                    for j in range(num_nodos) if j != i] 
                for i in range(num_nodos)}
        return lista
    
    else:
        raise ValueError(f"Tipo '{tipo}' no válido. Use 'dispersa', 'densa' o 'completa'")


def imprimir_analisis(resultado):
    """Imprime el análisis de densidad de forma legible."""
    
    print("ANÁLISIS DE DENSIDAD DE RED LOGÍSTICA")

    print(f"  Tipo de grafo: {resultado['tipo_grafo'].capitalize()}")
    print(f"  Número de nodos (V): {resultado['V']}")
    print(f"  Número de arcos (E): {resultado['E']}")
    print(f"  Arcos máximos posibles: {resultado['E_posibles']}")
    print(f"  Densidad: {resultado['porcentaje']} ({resultado['densidad']:.4f})")

    print(f"  {resultado['recomendacion']}")
    print(f"  Estructura recomendada: {resultado['estructura_recomendada'].upper()}")

# Prueba
if __name__ == "__main__":
    import random
    
    print("=== Caso 1: RED DISPERSA (<15% de densidad) ===\n")
    red_dispersa = generar_red_ejemplo('dispersa', 8)
    # Mostramos algunas conexiones
    print("Lista de adyacencia (muestra):")
    for i in range(min(3, len(red_dispersa))):
        print(f"  {i}: {red_dispersa[i]}")
    print("  ...")
    print()
    
    resultado1 = analizar_densidad_red(red_dispersa)
    imprimir_analisis(resultado1)
    
    print("\n\n")
    
    print("=== Caso 2: RED DENSA (>15% de densidad) ===\n")
    red_densa = generar_red_ejemplo('densa', 6)
    print("Lista de adyacencia (muestra):")
    for i in range(min(3, len(red_densa))):
        print(f"  {i}: {red_densa[i]}")
    print("  ...")
    print()
    
    resultado2 = analizar_densidad_red(red_densa, umbral=0.15)
    imprimir_analisis(resultado2)
    
    print("\n\n")
    
    print("=== acceso 3: RED COMPLETA (100% de densidad) ===\n")
    red_completa = generar_red_ejemplo('completa', 4)
    for i in range(len(red_completa)):
        print(f"  {i}: {red_completa[i]}")
    print()
    
    resultado3 = analizar_densidad_red(red_completa, umbral=0.15)
    imprimir_analisis(resultado3)
    
    print("\n\n")
    
    print("=== Caso 4: RED CON ETIQUETAS PERSONALIZADAS ===\n")
    red_logistica = {
        'CD_Madrid': [('Barcelona', 320), ('Valencia', 180)],
        'Barcelona': [('Madrid', 320), ('Valencia', 210), ('Zaragoza', 150)],
        'Valencia': [('Madrid', 180), ('Barcelona', 210)],
        'Zaragoza': [('Barcelona', 150), ('Madrid', 200)],
        'Sevilla': [('Madrid', 280)]  # Sevilla solo conecta a Madrid
    }
    
    resultado4 = analizar_densidad_red(red_logistica, es_dirigido=False, umbral=0.15)
    imprimir_analisis(resultado4)
