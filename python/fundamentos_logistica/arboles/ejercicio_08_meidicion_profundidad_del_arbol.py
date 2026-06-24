"""Ejercicio 08: Meidición de la Profundidad del árbol (Complejidad de Decisiones)

En la planeación estratégica, la altura o profundidad de un árbol binario representa el número máximo
de decisiones secuenciales que se deben tomoar en el peor de los escenarios. Escribe una función 
calcular_profundidad(nodo) que devuelva la altura máxima del árbol (la raíz sola cuenta como profundidad 1;
                                                                      si no hay nodo devuelve 0). """

class Nodo:
    def __init__(self, valor, izquierdo=None, derecho=None):
        self.valor = valor
        self.izquierdo = izquierdo
        self.derecho = derecho

def calcular_profundidad(nodo):
    # Caso base: si no hay nodo, la profundidad es 0
    if nodo is None:
        return 0

    # Calculamos la profundidad de cada subárbol
    prof_izq = calcular_profundidad(nodo.izquierdo)
    prof_der = calcular_profundidad(nodo.derecho)

    # La profundidad del nodo actual es 1 + la máxima profundidad de sus hijos
    return 1 + max(prof_izq, prof_der)

# Prueba:
raiz = Nodo(1)
print("Caso 1: ", calcular_profundidad(raiz))

raiz = Nodo(1, Nodo(2, Nodo(4)), Nodo(3))
print("\nCaso 2: ", calcular_profundidad(raiz))

print("\nCaso 3: ", calcular_profundidad(None)) # Árbol vacío
