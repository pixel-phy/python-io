""" Ejercicio 02: Evaluación del Valor esperado (Árbol de decisión con Incertidumbre)

En un árbol binario de decisión, el nodo actual se ramifica en dos escenarios climáticos:
Escenario A (izquierdo) y Escenario B (Derecho). Cada nodo hijo tiene un valor (ingreso financiero).
Escribe una función calcular_valor_esperado_maximo(nodo) que recorra el árbol binario y devuelva cuál
es el máximo valor individual registrado en cualquiera de las hojas terminales para mapear el escenario
más optimista. """

class Nodo:
    def __init__(self, valor, izquierdo=None, derecho=None):
        self.valor = valor
        self.izquierdo = izquierdo
        self.derecho = derecho

def calcular_valor_esperado_maximo(nodo):
    # Caso base: si el nodo es None retornamos el valor más bajo posible
    if nodo is None:
        return float('-inf')

    # Si es una hoja (no tiene hijos), retornamos su valor
    if nodo.izquierdo is None and nodo.derecho is None:
        return nodo.valor

    # Recorremos ambos subárboles y obtenemos sus máximos
    max_izq = calcular_valor_esperado_maximo(nodo.izquierdo)
    max_der = calcular_valor_esperado_maximo(nodo.derecho)

    # Retornamos el máximo entre ambos
    return max(max_izq, max_der)

# Pruebas:
# Árbol simple
raiz = Nodo(5,
            Nodo(3, Nodo(1), Nodo(4)),
            Nodo(8))
print(calcular_valor_esperado_maximo(raiz))

# Árbol con números negativos
raiz = Nodo(-2,
            Nodo(-5, Nodo(-10), Nodo(-3)),
            Nodo(-1))
print(calcular_valor_esperado_maximo(raiz))

# Árbol de una sola hoja
raiz = Nodo(42)
print(calcular_valor_esperado_maximo(raiz))

# Árbol vacío
print(calcular_valor_esperado_maximo(None))
