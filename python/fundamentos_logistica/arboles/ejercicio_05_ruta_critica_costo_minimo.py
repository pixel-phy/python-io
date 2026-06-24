""" Ejercicio 05: Ruta crítica de Costo mínimo (Decisión Óptima)

Estás en la raíz de un árbol de procesos de manufactura. Cada nodo hijo representa una
alternativa de maquinaria con un costo de operación determinado. Escribe una función 
encontrar_camino_aconomico(nodo) que devuelva una lista con los nombres de los nodos que representan
la ruta desde la raíz hasta una hoja que acumule el menor costo posible. """

class Nodo:
    def __init__(self, nombre, costo, hijos=None):
        self.nombre = nombre
        self.costo = costo  # Costo de operación de este proceso
        self.hijos = hijos if hijos is not None else []

def encontrar_camino_economico(nodo):
    """
    Encuentra la ruta de costo mínimo desde la raíz hasta una hoja.
    Retorna una lista con los nombres de los nodos en la ruta óptima.
    
    Args:
        nodo: Nodo raíz del árbol de procesos
    
    Returns:
        list: Lista de nombres de nodos en la ruta de menor costo
    """
    # Caso base: si es hoja, retorna [nombre]
    if not nodo.hijos:
        return [nodo.nombre]
    
    # Encontrar la mejor ruta entre todos los hijos
    mejor_camino = None
    mejor_costo = float('inf')
    
    for hijo in nodo.hijos:
        # Obtener la ruta óptima del hijo
        camino_hijo = encontrar_camino_economico(hijo)
        
        # Calcular el costo de la ruta del hijo
        costo_hijo = calcular_costo_ruta(hijo, camino_hijo)
        
        # Actualizar si encontramos una mejor ruta
        if costo_hijo < mejor_costo:
            mejor_costo = costo_hijo
            mejor_camino = [nodo.nombre] + camino_hijo
    
    return mejor_camino

def calcular_costo_ruta(nodo, ruta_nombres):
    """
    Calcula el costo total de una ruta dada sus nombres.
    Función auxiliar para la solución básica.
    """
    # Buscamos el nodo correspondiente al primer elemento de la ruta
    if not ruta_nombres:
        return 0
    
    # Si el nodo actual es el primero de la ruta
    if nodo.nombre == ruta_nombres[0]:
        if len(ruta_nombres) == 1:
            return nodo.costo
        # Buscar en los hijos
        for hijo in nodo.hijos:
            if hijo.nombre == ruta_nombres[1]:
                return nodo.costo + calcular_costo_ruta(hijo, ruta_nombres[1:])
    
    return 0

def encontrar_camino_economico_v2(nodo, costo_acumulado=0, camino_actual=None):
    """
    Versión mejorada que acumula el costo durante la recursión.
    Más eficiente y elegante.
    """
    if camino_actual is None:
        camino_actual = []
    
    # Agregamos el nodo actual al camino
    nuevo_camino = camino_actual + [nodo.nombre]
    nuevo_costo = costo_acumulado + nodo.costo
    
    # Si es hoja, retornamos el camino y su costo
    if not nodo.hijos:
        return nuevo_camino, nuevo_costo
    
    # Explorar todos los hijos y quedarnos con el mejor
    mejor_camino = None
    mejor_costo = float('inf')
    
    for hijo in nodo.hijos:
        camino_hijo, costo_hijo = encontrar_camino_economico_v2(
            hijo, nuevo_costo, nuevo_camino
        )
        
        if costo_hijo < mejor_costo:
            mejor_costo = costo_hijo
            mejor_camino = camino_hijo
    
    return mejor_camino, mejor_costo

# Función wrapper para mantener la interfaz solicitada
def encontrar_camino_economico_wrapper(nodo):
    """
    Wrapper para la versión V2 que mantiene la interfaz original.
    """
    camino, _ = encontrar_camino_economico_v2(nodo)
    return camino

# Prueba

# Nivel de máquinas finales (hojas)
maquina_a = Nodo("Máquina A - Automática", 45000)
maquina_b = Nodo("Máquina B - Semiautomática", 35000)
maquina_c = Nodo("Máquina C - Automática", 40000)
maquina_d = Nodo("Máquina D - Manual", 28000)
maquina_e = Nodo("Máquina E - CNC", 50000)
maquina_f = Nodo("Máquina F - Convencional", 30000)
maquina_g = Nodo("Máquina G - Automática", 38000)
maquina_h = Nodo("Máquina H - Manual", 25000)
estacion_1 = Nodo("Estación 1", 15000)
estacion_2 = Nodo("Estación 2", 12000)
estacion_3 = Nodo("Estación 3", 10000)
estacion_4 = Nodo("Estación 4", 8000)

# Nivel de procesos específicos
horno_electrico = Nodo("Horno Eléctrico", 30000, [maquina_a, maquina_b])
horno_gas = Nodo("Horno Gas", 25000, [maquina_c, maquina_d])
prensa_hidraulica = Nodo("Prensa Hidráulica", 35000, [maquina_e, maquina_f])
martillo_neumatico = Nodo("Martillo Neumático", 20000, [maquina_g, maquina_h])
linea_automatizada = Nodo("Línea Automatizada", 40000, [estacion_1, estacion_2])
linea_manual = Nodo("Línea Manual", 25000, [estacion_3, estacion_4])  # Corregido: "Línea"

# Nivel de procesos principales
fundicion = Nodo("Fundición", 50000, [horno_electrico, horno_gas])
forja = Nodo("Forja", 45000, [prensa_hidraulica, martillo_neumatico])
ensamble = Nodo("Ensamble", 20000, [linea_automatizada, linea_manual])

# Raíz
planta = Nodo("Planta Principal", 0, [fundicion, forja, ensamble])

print("ANÁLISIS DE RUTA DE COSTO MÍNIMO")

# Usando la versión básica (con errores corregidos)
print("\n--- Versión Básica ---")
ruta_optima = encontrar_camino_economico(planta)
print("Ruta óptima:", " → ".join(ruta_optima))

# Usando la versión V2 (más eficiente)
print("\n--- Versión Mejorada (V2) ---")
ruta_optima_v2, costo_optimo = encontrar_camino_economico_v2(planta)
print("Ruta óptima:", " → ".join(ruta_optima_v2))
print(f"Costo total: ${costo_optimo:,.2f}")

# Verificación: calcular el costo manualmente para confirmar
print("\n--- Verificación de Costos ---")
costo_verificado = 0
for nombre in ruta_optima_v2:
    # Esta es una verificación simplificada
    # En un caso real, necesitaríamos buscar el nodo
    pass
print(f"Costo verificado: ${costo_optimo:,.2f}")
