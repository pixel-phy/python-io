"""Ejercicio 22: Auditoría de Despacho por Niveles de Urgencia (BFS)

En un almacén cross-docking, los camiones en la raíz se descargan primero, luego las plataformas del nivel 1,
luego las bahías del nivel 2. Escribe una función recorrido_por_niveles(nodo) que devuelva una lista de listas,
donde cada sublista contenga los nombres de los nodos de ese nivel específico (utiliza una cola con collections.deque). """

from collections import deque

class Nodo:
    def __init__(self, valor, izquierdo=None, derecho=None):
        self.valor = valor
        self.izquierdo = izquierdo
        self.derecho = derecho

def recorrido_por_niveles(nodo):
    """
    Recorre el árbol por niveles usando BFS con una cola.

    Args:
        nodo: Nodo raíz del árbol
    Returns:
        Lista de listas, donde cada sublista contiene los nodos de ese nivel
    """

    if nodo is None:
        return []

    # Resultado final: lista de niveles
    resultado = []

    # Cola para BFS (almacena tuplas: (nodo, nivel))
    cola = deque()
    cola.append((nodo, 0)) # (nodo_raíz, nivel_0)

    while cola:
        # Extraemos el primer elemento de la cola (FIFO)
        nodo_actual, nivel = cola.popleft()

        # Si es un nuevo nivel, creamos una nueva sublista
        if nivel == len(resultado):
            resultado.append([])

        # Agregamos el valor al nivel correspondiente
        resultado[nivel].append(nodo_actual.valor)

        # Agregamos los hijos a la cola (con su nivel correspondiente)
        if nodo_actual.izquierdo:
            cola.append((nodo_actual.izquierdo, nivel + 1))
        if nodo_actual.derecho:
            cola.append((nodo_actual.derecho, nivel + 1))

    return resultado

almacen = Nodo("Camiones")
almacen.izquierdo = Nodo("Plataforma_A")
almacen.derecho = Nodo("Plataforma_B")
almacen.izquierdo.izquierdo = Nodo("Bahía1")
almacen.izquierdo.derecho = Nodo("Bahía2")
almacen.derecho.izquierdo = Nodo("Bahía3")
almacen.derecho.derecho = Nodo("Bahía4")
almacen.izquierdo.izquierdo.izquierdo = Nodo("C1")
almacen.izquierdo.izquierdo.derecho = Nodo("C2")

# Realizamos recorrido por niveles
niveles = recorrido_por_niveles(almacen)

# Mostramos resultados
print("Auditoría de Despacho por Niveles:")
for i, nivel in enumerate(niveles):
    print(f"Nivel {i}: {nivel}")
