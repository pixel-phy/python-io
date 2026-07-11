"""Ejercicio 03: Análisis de Costos Acumulados de Ruta

Imagina un árbol que representa las fases de un proyecto de ensamble (BOM). Cada nodo tiene un costo asociado.
Escribe una función calcular_costo_total(nodo) que sume recursivamente el costo del nodo actual y el de todos
sus descendientes para saber el costo total del sistema. """

class Nodo:
    def __init__(self, nombre, costo, hijos=None):
        self.nombre = nombre
        self.costo = costo # Costo del componente acutal
        self.hijos = hijos if hijos is not None else []

def calcular_costo_total(nodo):
    """
    Calcula el costo total acumulado de un nodo y todos sus descendientes.

    Args:
        nodo: Nodo del árbol BOM

    Returns: 
        float/int: Costo total incluyendo el nodo y todos sus subcomponentes
    """

    # Si no iene hijos, el costo total es su propio costo
    return nodo.costo + sum(calcular_costo_total(hijo) for hijo in nodo.hijos)

# Se construye el árbol de costos
# Nivel de hojas (ciudades)
ciudad_medellin = Nodo("Medellin", 8000)
ciudad_bogota = Nodo("Bogotá", 6000)
ciudad_pereira = Nodo("Pereira", 10000)
ciudad_manizales = Nodo("Manizales", 12000)
ciudad_barranquilla = Nodo("Barranquilla", 9000)
ciudad_armenia = Nodo("Armenia", 15000)
ciudad_cartagena = Nodo("Cartagena", 5000)

# Nivel de rutas de transporte
ruta_a = Nodo("Ruta A - Camión", 15000, [ciudad_medellin, ciudad_bogota])
ruta_b = Nodo("Ruta B - Tren", 20000, [ciudad_pereira])
ruta_c = Nodo("Ruta C - Barco", 25000, [ciudad_barranquilla, ciudad_manizales])
ruta_d = Nodo("Ruta D - Avión", 35000, [ciudad_armenia])
ruta_e = Nodo("Ruta E - Camión", 10000, [ciudad_cartagena])

# Nivel de centro de distribución
centro_norte = Nodo("Centro Norte", 50000, [ruta_a, ruta_b])
centro_sur = Nodo("Centro Sur", 45000, [ruta_c, ruta_d])
centro_este = Nodo("Centro Este", 30000, [ruta_e])

# Raíz del árbol
centro_principal = Nodo("Centro Principal", 100000, [centro_norte, centro_sur, centro_este])

# Calculo del costo
costo_total_sistema = calcular_costo_total(centro_principal)
print(f"Costo total del sistema de distribución: ${costo_total_sistema:,.2f}")
