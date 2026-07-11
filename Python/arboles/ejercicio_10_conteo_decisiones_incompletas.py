"""Ejercicio 10: Conteo de Decisiones Incompletas

En la configuración de un modelo de manufactura automátizada, un árbol debe estar perfectamente
balanceado (árbol lleno). Queremos auditar el sistema. Escribe una función contar_nodos_un_hijo(nodo)
que cuente cuántos nodos del árbol tienen exactamente un solo hijo (lo que en producción significaría
un proceso mal configurado o una decisión sin alternativa). """

class Nodo:
    def __init__(self, valor, izquierdo=None, derecho=None):
        self.valor = valor
        self.izquierdo = izquierdo
        self.derecho = derecho

def contar_nodos_un_hijo(nodo):
    # Caso base: si el nodo es None, no hay nada que contar
    if nodo is None:
        return 0

    # Contamos en los subárboles
    cont_izq = contar_nodos_un_hijo(nodo.izquierdo)
    cont_der = contar_nodos_un_hijo(nodo.derecho)

    # Verificamos si el nodo actual tiene exactamente un hijo
    tiene_izq = nodo.izquierdo is not None
    tiene_der = nodo.derecho is not None

    # Si tiene exactamente un hijo (uno es None y el otro no)
    if tiene_izq != tiene_der:
        return 1 + cont_izq + cont_der

    else:
        return cont_izq + cont_der

# Prueba:
raiz = Nodo(1,
            Nodo(2, Nodo(4, Nodo(6)), None),
            Nodo(3, None, Nodo(5)))
print(contar_nodos_un_hijo(raiz))

raiz = Nodo(1, 
            Nodo(2, Nodo(4), Nodo(5)),
            Nodo(3, Nodo(6), Nodo(7)))
print(contar_nodos_un_hijo(raiz))

raiz = Nodo(1, Nodo(2, Nodo(3), Nodo(4)), None)
print(contar_nodos_un_hijo(raiz))

print(contar_nodos_un_hijo(None))
