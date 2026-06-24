"""Ejercicio 12: Inversión de Prioridades Operativas (Mirroring)

A veces, en simulación de operaciones, necesitamos evaluar el escenario espejo 
(por ejemplo, cambiar la prioridad de "costo mínimo" a "costo máximo", o invertir rutas 
de ida y vuelta). Escribe una función invertir_arbol_operaciones(nodo) que transforme el árbol
binario modificándolo de tal manera que el hijo izquierdo y el hijo derecho de todos los nodos 
se intercambien entre sí. La función debe modificar el árbol original o devolver la raíz del 
árbol invertido. """

class Nodo:
    def __init__(self, valor, izquierdo=None, derecho=None):
        self.valor = valor
        self.izquierdo = izquierdo
        self.derecho = derecho

def invertir_arbol_operaciones(nodo):
    # Caso base: si el nodo es None, retornamos None
    if nodo is None:
        return None

    # Intercambiamos los hijos del nodo actual
    nodo.izquierdo, nodo.derecho = nodo.derecho, nodo.izquierdo

    # Invertimos recursivamente los subárboles (ahora intercambiados)
    invertir_arbol_operaciones(nodo.izquierdo)
    invertir_arbol_operaciones(nodo.derecho)

    # Retornamos la raíz del árbol invertido
    return nodo

# Pruebas:

def imprimir_arbol(nodo):
    if nodo is None:
        return "Árbol vacío"

    from collections import deque
    resultado = []
    cola = deque([nodo])

    while cola:
        nivel = []
        for _ in range(len(cola)):
            actual = cola.popleft()
            nivel.append(str(actual.valor) if actual else "None")
            if actual:
                cola.append(actual.izquierdo)
                cola.append(actual.derecho)
        resultado.append(" ".join(nivel))

    return "\n".join(resultado)

print("Árbol original")
raiz = Nodo(1, Nodo(2, Nodo(4), Nodo(5)), Nodo(3))
print(imprimir_arbol(raiz))

print("\nÁrbol Invertido")
raiz_invertida = invertir_arbol_operaciones(raiz)
print(imprimir_arbol(raiz_invertida))

print("\nÁrbol asimétrico original")
raiz2 = Nodo(1, 
             Nodo(2, Nodo(4, Nodo(6)), None),
             Nodo(3, None, Nodo(5)))
print(imprimir_arbol(raiz2))

print("\nArbol asimétrico invertido")
raiz2_invertida = invertir_arbol_operaciones(raiz2)
print(imprimir_arbol(raiz2_invertida))

print("\nÁrbol vacío")
print(invertir_arbol_operaciones(None))
