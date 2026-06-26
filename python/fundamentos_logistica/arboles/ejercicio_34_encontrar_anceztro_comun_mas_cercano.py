"""Ejercicio 34: Encontrar el "Anceztro común más cercano" (LCA) en la cadena de mando

En una estrucutra organizacional o en un árbol de dependencias de subensambles MRP, dos componentes A y B 
reportan o se alimentan de un componente supervisor común. Escribe una función
encontrar_supervisor_comun(raiz, id_A, id_B) que encuentre el ancestro común más bajo entre dos nodos 
en un BST. Aprovecha las propiedades del BST para resolverlo en tiempo O(log N) sin usar memoria extra. """

class Nodo:
    def __init__(self, id_empleado, nombre, izquierdo=None, derecho=None):
        self.id_empleado = id_empleado
        self.nombre = nombre
        self.izquierdo = izquierdo
        self.derecho = derecho

def encontrar_supervisor_comun(raiz, id_A, id_B):
    """
    Encuentra el Anceztro común más cercano (LCA) de dos nodos en un BST.

    Args:
        raiz: Raíz del árbol organizacional
        id_A: ID del primer empleado/componente
        id_B: ID del segundo empleado/componente

    Returns:
        Nodo del LCA o None si no existe
    """

    # Caso base: árbol vacío
    if raiz is None:
        return None

    # Si ambas IDs son menores que la raíz, el LCA está en el subárbol izquierdo
    if id_A < raiz.id_empleado and id_B < raiz.id_empleado:
        return encontrar_supervisor_comun(raiz.izquierdo, id_A, id_B)

    # Si ambos IDs son mayores que la raíz, el LCA está en el subárbol derecho
    if id_A > raiz.id_empleado and id_B > raiz.id_empleado:
        return encontrar_supervisor_comun(raiz.derecho, id_A, id_B)

    # Si llegamos hasta aquí significa:
    # - Un ID está a la izquierda y el otro a la derecha.
    # - Uno de los IDs es igual a la raíz
    # Por tal motivo, la raiz actual es el LCA
    return raiz

# Prueba:

raiz = Nodo(50, "CEO - Ana")
raiz.izquierdo = Nodo(30, "Director - Luis")
raiz.derecho = Nodo(70, "VP - Carlos")

raiz.izquierdo.izquierdo = Nodo(20, "Gerente - María")
raiz.izquierdo.derecho = Nodo(40, "Gerente - Juan")

raiz.derecho.izquierdo = Nodo(60, "Gerente - Elena")
raiz.derecho.derecho = Nodo(80, "Gerente - Pedro")

raiz.izquierdo.izquierdo.izquierdo = Nodo(10, "Analista - Sofía")
raiz.izquierdo.izquierdo.derecho = Nodo(25, "Analista - Diego")
raiz.derecho.derecho.derecho = Nodo(90, "Analista - Laura")

# Test cases
test_cases = [
    (10, 25),  # Mismo padre directo
    (10, 40),  # Diferentes ramas bajo el mismo director
    (10, 90),  # Ramas completamente diferentes
    (25, 60),  # Ramas diferentes
    (50, 30),  # Uno es ancestro del otro
    (30, 50),  # Orden inverso
    (10, 10),  # Mismo nodo
    (99, 100), # IDs inexistentes
]

for id_A, id_B in test_cases:
    print(f"\n")
    print(f"Buscando LCA de ID {id_A} y ID {id_B}")
    resultado = encontrar_supervisor_comun(raiz, id_A, id_B)
    if resultado:
        print(f"LCA: {resultado.nombre} (ID: {resultado.id_empleado})")
