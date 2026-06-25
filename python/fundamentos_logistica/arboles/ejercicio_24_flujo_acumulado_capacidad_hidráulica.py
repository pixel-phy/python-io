"""Ejercicio 24: Flujo acumulado de capacidad hidráulica / Red de gas de abajo hacia arriba

Imagina una red de tuberías binaria de distribución de gas. Cada nodo hoja inyecta un flujo constante
(nodo.valor). Los nodos intermedios no inyectan gas, pero su capacidad final debe ser la suma de los 
flujos de todo su subárbol. Escribe una función 
calcular_flujos_red(nodo) que recorra el árbol en Post-order y actualice el atributo nodo.valor de cada nodo interno
con la suma total del flujo que pasa a través de él. """

class Nodo:
    def __init__(self, valor, izquierdo=None, derecho=None):
        self.valor = valor  #Flujo inyectado (hojas) o capacidad (internos)
        self.izquierdo = izquierdo
        self.derecho = derecho

def calcular_flujos_red(nodo):
    """
        Calcula el flujo acumulado en cada nodo usando Post-order.

        Args:
            nodo: Nodo raíz de la red de tuberías
        Returns:
            int: Lfujo total que pasa por este nodo (suma de su subárbol)
    """
    # Caso base: nodo vacío
    if nodo is None:
        return 0

    # Paso 1: Procesaamos el subárbol izquierdo (Post-order)
    flujo_izquierdo = calcular_flujos_red(nodo.izquierdo)

    # Paso 2: Procesamos el subárbol derecho (Post-order)
    flujo_derecho = calcular_flujos_red(nodo.derecho)

    # Paso 3: Calculamos el flujo total que pasa por este nodo
    # Si es hoja, su valor se manteien (es el flujo que inyecta)
    # Si es interno, actualizamos su valor con la suma de sus hijos
    if nodo.izquierdo is None and nodo.derecho is None:
    # Es una hoja: su valor es el flujo que inyecta
        flujo_total = nodo.valor
    else:
    # Es un nodo interno: Su valor es la suma de sus subárboles
        flujo_total = flujo_izquierdo + flujo_derecho
        nodo.valor = flujo_total # Actualizamos el nodo

    return flujo_total

# Prueba:
red = Nodo(0)           # Nodo_A(Capacidad inicial 0)
red.izquierdo = Nodo(0) # Nodo_B
red.derecho = Nodo(0)   # Nodo_C
red.izquierdo.izquierdo = Nodo(5)   # Hoja: flujo 5
red.izquierdo.derecho = Nodo(3)     # Hoja: flujo 3
red.derecho.izquierdo = Nodo(7)     # Hoja: flujo 7
red.derecho.derecho = Nodo(2)       # Hoja: flujo 2

# Calculamos los flujos
flujo_total = calcular_flujos_red(red)

print(f"Flujo total en la red: {flujo_total}\n")

# Mostramos los valores actualizados
def mostrar_red(nodo, nivel=0, prefijo="Raíz: "):
    if nodo is None:
        return
    print(" " * nivel + prefijo + f"{nodo.valor}")
    mostrar_red(nodo.izquierdo, nivel + 1, "I: ")
    mostrar_red(nodo.derecho, nivel + 1, "D: ")

print("Red después de calcular flujos:")
mostrar_red(red)
