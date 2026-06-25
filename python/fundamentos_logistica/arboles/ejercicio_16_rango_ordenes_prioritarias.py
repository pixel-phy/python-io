""" Ejercicio 16: Rango de órdenes prioritarias (Filtro logístico)

Tu supervisor de almacén te pide una lista de todos los SKUs cuyos IDs se encuentren en un Rango
específico (por ejemplo, entre el ID 30 y el 60). Escribe una función
obtener_skus_en_rango(nodo, limite_inferior, limite_superior) que recorra el BST y devuelva
una lista con las descripciones de los nodos que entran en el rango inclusivo, aprovechando 
la estructura para no visitar ramas que queden fuera del rango. """

class Nodo:
    def __init__(self, id_sku, descripcion):
        self.id = id_sku
        self.descripcion = descripcion
        self.izquierdo = None
        self.derecho = None

def obtener_skus_en_rango(nodo, limite_inferior, limite_superior):
    """
        Retorna una lista con las descripciones de los SKUs cuyos IDs están en el rango 
        [limite_inferior, limite_superior] (inclusivo).
    """
    # Caso base: nodo vacío
    if nodo is None:
        return []

    resultado = []

    # 1. Verificar si el nodo actual está en el rango
    if limite_inferior <= nodo.id <= limite_superior:
        resultado.append(nodo.descripcion)

    # 2. Explorar subárbol izquierdo solo si puede contener valores >= limite inferior
    if nodo.id > limite_inferior:
        resultado.extend(obtener_skus_en_rango(nodo.izquierdo, limite_inferior, limite_superior))

    # 3. Explorar subárbol derecho solo si puede contener valores <= limite superior
    if nodo.id < limite_superior:
        resultado.extend(obtener_skus_en_rango(nodo.derecho, limite_inferior, limite_superior))

    return resultado

# Pruebas:

raiz = Nodo(50, "SKU-50")
raiz.izquierdo = Nodo(30, "SKU-30")
raiz.derecho = Nodo(70, "SKU-70")
raiz.izquierdo.izquierdo = Nodo(20, "SKU-20")
raiz.izquierdo.derecho = Nodo(40, "SKU-40")
raiz.derecho.izquierdo = Nodo(60, "SKU-60")
raiz.derecho.derecho = Nodo(80, "SKU-80")

resultado = obtener_skus_en_rango(raiz, 30, 60)
print(resultado)
