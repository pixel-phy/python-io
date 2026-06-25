"""Ejercicio 21: Desensamble y liquidación de Activos (Post-order)

Al cerrar una planta de manufactura, las estaciones deben desmantelarse de abajo hacia arriba 
(primero las herramientas de las hojas, luego los soportes intermedios y al final la infraestructura raíz).
Escribe una función generar_plan_desmantelamiento(nodo) que devuelva una lista con los nombres de los nodos en 
el orden exacto en que deben ser desactivados usando Post_order. """

class Nodo:
    def __init__(self, valor, izquierdo=None, derecho=None):
        self.valor = valor
        self.izquierdo = izquierdo
        self.derecho = derecho

def generar_plan_desmantelamiento(nodo):
    """
    Genera una lista con el orden de desmantelamiento usando Post-order.

    Args:
        nodo: Nodo raíz de la estructura a desmantelar

    Returns:
        Lista con los nombres de los nodos en orden Post-order
    """

    # Lista que almacenará el plan de desmantelamiento
    plan = []

    # Función recursiva interna
    def post_order(nodo_actual):
        if nodo_actual is None:
            return

        # paso 1: Procesamos el subárbol izquierdo
        post_order(nodo_actual.izquierdo)

        # Paso 2: Procesamos el subárbol derecho
        post_order(nodo_actual.derecho)

        # Paso 3: Procesamos la raíz (desmantelamos el nodo actual)
        plan.append(nodo_actual.valor)

    # Iniciamos el recorrido
    post_order(nodo)

    return plan

# Prueba
planta = Nodo("Planta")
planta.izquierdo = Nodo("Taller_A")
planta.derecho = Nodo("Taller_B")
planta.izquierdo.izquierdo = Nodo("Hoja1")
planta.izquierdo.derecho = Nodo("Hoja2")
planta.derecho.izquierdo = Nodo("Hoja3")
planta.izquierdo.izquierdo.izquierdo = Nodo("T1")
planta.izquierdo.izquierdo.derecho = Nodo("T2")

# Generamos el plan de desmantelamiento
plan = generar_plan_desmantelamiento(planta)

print("Plan de desmantelamiento (Post-order):")
for i, elemento in enumerate(plan, 1):
    print(f"{i}. {elemento}")
