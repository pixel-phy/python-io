"""Ejercicio 20: Clonación de una Red Logística (Pre-order)

Una empresa aliada quiere replicar exactamente nuestra estructura jerárquica de centros de distribución.
Escribe una función clonar_red(nodo) que utilice un recorrido Pre-order para crear y devolver un árbol
completamente nuevo (nuevas instancias de Nodo) idéntico al original """

class Nodo:
    def __init__(self, valor, izquierdo=None, derecho=None):
        self.valor = valor
        self.izquierdo = izquierdo
        self.derecho = derecho

def clonar_red(nodo):
    """
    Clona un árbol usando recorrido Pre-order.

    Args:
        nodo: Nodo raíz del árbol a clonar. 

    Returns:
        Nuevo Nodo (copia) o None si el nodo original es None
    """
    # Caso base: si el nodo es None, retornamos None
    if nodo is None:
        return None

    # Paso 1: Clonamos la raíz (pre-order: visitamos la raíz primero)
    nuevo_nodo = Nodo(nodo.valor)

    # Paso 2: Clonamos el subárbol izquierdo (recursivamente)
    nuevo_nodo.izquierdo = clonar_red(nodo.izquierdo)

    # Paso 3: Clonamos el subárbol derecho (recursivamente)
    nuevo_nodo.derecho = clonar_red(nodo.derecho)

    # Retornamos el nuevo nodo clonado
    return nuevo_nodo

# Pruebas:
red_original = Nodo("Central")
red_original.izquierdo = Nodo("Norte")
red_original.derecho = Nodo("Sur")
red_original.izquierdo.izquierdo = Nodo("Este")
red_original.izquierdo.derecho = Nodo("Oeste")
red_original.derecho.derecho = Nodo("Suroeste")

# Clonamos red
red_clonada = clonar_red(red_original)

# Verificamos que son independientes
print("Son la misma red: ", red_original is red_clonada)
print("Comparten el mismo valor: ",red_original.valor == red_clonada.valor)

# Modificamos el original y vemos que el clon no cambia
red_original.valor = "Central_modificada"
print(red_clonada.valor)
