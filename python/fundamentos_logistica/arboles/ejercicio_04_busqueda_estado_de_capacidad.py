"""Ejercicio 04: Búsqueda de un Estado de Capacidad

Tienes un árbol que representa la jerarquía de una red de distribución (País -> Regiones -> Centros de distribución). 
Escribe una función buscar_centro(nodo, nombre_destino) que busque un nodo por su nombre y devuelva su valor (que 
representa la capacidad de almacenamiento en toneladas). Si no lo encuentra, debe devolver None. """

class Nodo:
    def __init__(self, nombre, capacidad, hijos=None):
        self.nombre = nombre
        self.capacidad = capacidad # Capacidad en toneladas
        self.hijos = hijos if hijos is not None else []

def buscar_centro(nodo, nombre_destino):
    """
    Busca un nodo por su nombre en el árbol de distribución
    Retorna la capacidad (valor) del nodo si lo encuentra, None en caso contrario.
    
    Args: 
        nodo: Nodo raíz del árbol
        nombre_destino: Nombre del centro a buscar

    Returns: 
        int/float: Capacidad del centro, o None si no existe
    """
    # Caso base: si el nodo acutal es el que buscamos
    if nodo.nombre == nombre_destino:
        return nodo.capacidad

    # Búsqueda recursiva
    for hijo in nodo.hijos:
        resultado = buscar_centro(hijo, nombre_destino)
        if resultado is not None:
            return resultado

    return None

# Nicel de centros de distribución
cd_pereira = Nodo("CD Pereira", 2000)
cd_neiva = Nodo("CD Neiva", 1200)
cd_cali = Nodo("CD Cali", 1000)
cd_barranquilla = Nodo("CD Barranquilla", 1600)
cd_girardota = Nodo("CD Girardota", 2500)
cd_cota = Nodo("CD Cota", 1600)
cd_gapala = Nodo("CD Galapa", 1000)
cd_choco = Nodo("CD Chocó", 800)
cd_oeste = Nodo("CD Oeste", 1400)

# Nivel de regiones
region_norte = Nodo("Región Norte", 3000, [cd_gapala, cd_cota, cd_oeste])
region_centro = Nodo("Región Occidente", 4500, [cd_pereira, cd_cali, cd_neiva])
region_antioquia = Nodo("Región Antioquia", 2500, [cd_girardota, cd_choco, cd_barranquilla])

# Raíz - País
pais = Nodo("Pais", 10000, [region_norte, region_centro, region_antioquia])

# Prueba de búsqueda
print("--- Búsqueda de centro de distribución ---")

# Existentes
centro_buscar = "CD Pereira"
capacidad = buscar_centro(pais, centro_buscar)
if capacidad is not None:
    print(f"Centro '{centro_buscar}' encontrado. Capacidad: {capacidad} toneladas")
else:
    print(f"Centro '{centro_buscar}' no encontrado")

centro_buscar = "CD Cota"
capacidad = buscar_centro(pais, centro_buscar)
if capacidad is not None:
    print(f"Centro '{centro_buscar}' encontrado. Capacidad: {capacidad} toneladas")
else:
    print(f"Centro '{centro_buscar}' no encontrado")

# No existente
centro_buscar = "CD Tunja"
capacidad = buscar_centro(pais, centro_buscar)
if capacidad is not None:
    print(f"Centro '{centro_buscar}' encontrado. Capacidad: {capacidad} toneladas")
else:
    print(f"Centro '{centro_buscar}' no encontrado")
