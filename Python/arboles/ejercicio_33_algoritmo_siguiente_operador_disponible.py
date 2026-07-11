"""Ejercicio 33: El algoritmo del "Siguiente Operador Disponible" 

En un sistema de asignación de tareas en tiempo real, cada operador tiene un ID. Las tareas deben 
asignarse al operador que tenga el ID inmediatamente superior al operador que acaba de terminar (es decir
Sucesor In-order). Escribe una función obtener_siguiente_operador(raiz, id_actual) que, dado el ID de un
operador, devuelva el nodo del operador que debe seguir en la secuencia de la línea de producción de forma
eficiente (O(log N)). """

class Nodo:
    def __init__(self, id_operador, nombre_operador, izquierdo=None, derecho=None, padre=None):
        self.id_operador = id_operador
        self.nombre_operador = nombre_operador
        self.izquierdo = izquierdo
        self.derecho = derecho
        self.padre = padre                      # Referenciamos al padre para facilitar búsqueda

def obtener_siguiente_operador(raiz, id_actual):
    """
    Encuentra el sucesor in-order del operador con ID = id_actual.
    Retorna el nodo del Siguiente operador o None si no existe.
    """

    # Paso 1: Buscar el nodo con el ID actual
    nodo_actual = buscar_nodo(raiz, id_actual)

    if nodo_actual is None:
        return None # El ID no existe en el árbol

    # Paso 2: Encontrar el sucesor
    return encontrar_sucesor(nodo_actual)

def buscar_nodo(raiz, id_operador):
    """
    Busca un nodo por su ID en el BST.
    Retorna el nodo o None si no existe.
    """
    actual = raiz
    while actual is not None:
        if id_operador == actual.id_operador:
            return actual
        elif id_operador < actual.id_operador:
            actual = actual.izquierdo
        else:
            actual = actual.derecho
    return None

def encontrar_sucesor(nodo):
    """
    Encuentra el sucesor in-order de un nodo dado.
    Asume que el nodo existe en el árbol.
    """
    # Caso 1: El nodo tiene hijo derecho
    # El sucesor es el mínimo del subárbol derecho
    if nodo.derecho is not None:
        return encontrar_minimo(nodo.derecho)

    # Caso 2: El nodo NO tiene hijo derecho
    # Subir hasta encontrar un ancestro donde el nodo actual esté en el subárbol izquierdo

    actual = nodo
    while actual.padre is not None and actual == actual.padre.derecho:
        actual = actual.padre

    # Si llegamos a la raiz y aún no encontramos, retornamos None
    # (el nodo actual es el último en in-order)
    return actual.padre

def encontrar_minimo(nodo):
    """
    Encuentra el nodo más a la izquierda (mínimo) de un subárbol.
    """
    while nodo.izquierdo is not None:
        nodo = nodo.izquierdo
    return nodo

# Prueba:

raiz = Nodo(50, "Ana")
raiz.izquierdo = Nodo(30, "Luis", padre=raiz)
raiz.derecho = Nodo(70, "Carlos", padre=raiz)

raiz.izquierdo.izquierdo = Nodo(20, "María", padre=raiz.izquierdo)
raiz.izquierdo.derecho = Nodo(40, "Juan", padre=raiz.izquierdo)

raiz.derecho.izquierdo = Nodo(60, "Elena", padre=raiz.derecho)
raiz.derecho.derecho = Nodo(80, "Pedro", padre=raiz.derecho)

raiz.izquierdo.izquierdo.izquierdo = Nodo(10, "Sofía", padre=raiz.izquierdo.izquierdo)
raiz.izquierdo.izquierdo.derecho = Nodo(25, "Diego", padre=raiz.izquierdo.izquierdo)

# Test de sucesores
test_cases = [10, 20, 25, 30, 40, 50, 60, 70, 80, 99]

for id_test in test_cases:
    sucesor = obtener_siguiente_operador(raiz, id_test)
    if sucesor:
        print(f"Sucesor de {id_test}: {sucesor.id_operador} ({sucesor.nombre_operador})")
    else:
        print(f"Sucesor de {id_test}: No existe")
