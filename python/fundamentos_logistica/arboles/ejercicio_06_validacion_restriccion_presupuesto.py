"""Ejercicio 06: Validación de Restricción de Presupuesto (Branching)

En algoritmos tipo Branch and Bound, descartamos ramas enteras si violan una restricción (poda). 
Escribe una función verificar_presupuesto(nodo, presupuesto_maximo, costo_actual=0) que recorra el árbol
y dvuelva una lista con los nombres de los nodos "hoja" cuyos caminos completos desde la raíz no superen
el presupuesto_maximo. Si en algún punto el camino ya supera el presupuesto, no debe seguir explorando
los hijos de ese nodo. """

class Nodo:
    def __init__(self, nombre, costo, hijos=None):
        self.nombre = nombre
        self.costo = costo # Costo de operación de este proceso
        self.hijos = hijos if hijos is not None else []

def verificar_presupuesto(nodo, presupuesto_maximo, costo_actual=0, camino_actual=None):
    """
    Verifica qué rutas completas (hojas) no superan el presupuesto máximo.
    Implementa poda: si el costo actual supera el presupuesto, no explora hijos.

    Args: 
        nodo: Nodo actual del árbol
        presupuesto_maximo: Presupuesto máximo permitido
        costo_actual: Costo acumulado hasta este nodo
        camino_acutal: lista con los nombres de los nodos en el camino actual
    Returns:
        list: Lista de caminos (listas de nombres) que cumplen con el presupuesto
    """
    # Validación de entrada
    if nodo is None:
        return []
    
    # Inicializar camino_actual si es None
    if camino_actual is None:
        camino_actual = []
    
    # Asegurar que camino_actual es una lista
    if not isinstance(camino_actual, list):
        camino_actual = [camino_actual] if camino_actual else []
    
    # Calcular nuevo costo
    nuevo_costo = costo_actual + (nodo.costo if nodo.costo is not None else 0)
    nuevo_camino = camino_actual + [nodo.nombre]
    
    # PODA: Si superamos el presupuesto
    if nuevo_costo > presupuesto_maximo:
        return []
    
    # Si es hoja, retornamos el camino
    if not nodo.hijos:
        return [nuevo_camino]
    
    # Explorar hijos
    caminos_validos = []
    for hijo in nodo.hijos:
        caminos_validos.extend(
            verificar_presupuesto(hijo, presupuesto_maximo, nuevo_costo, nuevo_camino)
        )
    
    return caminos_validos
   
# Construimos el árbol (mismo que antes)
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

horno_electrico = Nodo("Horno Eléctrico", 30000, [maquina_a, maquina_b])
horno_gas = Nodo("Horno Gas", 25000, [maquina_c, maquina_d])
prensa_hidraulica = Nodo("Prensa Hidráulica", 35000, [maquina_e, maquina_f])
martillo_neumatico = Nodo("Martillo Neumático", 20000, [maquina_g, maquina_h])
linea_automatizada = Nodo("Línea Automatizada", 40000, [estacion_1, estacion_2])
linea_manual = Nodo("Línea Manual", 25000, [estacion_3, estacion_4])

fundicion = Nodo("Fundición", 50000, [horno_electrico, horno_gas])
forja = Nodo("Forja", 45000, [prensa_hidraulica, martillo_neumatico])
ensamble = Nodo("Ensamble", 20000, [linea_automatizada, linea_manual])

planta = Nodo("Planta Principal", 0, [fundicion, forja, ensamble])

# Probar con diferentes presupuestos
print("Validación de restricción de presupuesto")

presupuestos = [120000, 100000, 80000, 60000]

for presupuesto in presupuestos:
    print(f"\n--- Presupuesto: ${presupuesto:,.2f} ---")
    caminos_validos = verificar_presupuesto(planta, presupuesto)
    
    if caminos_validos:
        print(f"{len(caminos_validos)} rutas encontradas que cumplen el presupuesto:")
        for i, camino in enumerate(caminos_validos, 1):
            print(f"  {i}. {' → '.join(camino)}")
    else:
        print("No se encontraron rutas que cumplan con el presupuesto")
