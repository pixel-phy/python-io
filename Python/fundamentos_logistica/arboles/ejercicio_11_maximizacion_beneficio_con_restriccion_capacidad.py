"""Ejercicio 11: Maximización de Beneficio con Restricción de Capacidad

Imagina que el árbol binario representa un árbol de decisiones de carga de camiones (Mochila
0-1). El nodo izquierdo añade un paquete (suma peso a un contador y beneficio a otro) y el derecho
lo descarta. Escribe una función mejor_combinacion_carga(nodo, capacidad_maxima, peso_actual=0, 
beneficio_actual=0) que recorra el árbol y devuelva el máximo beneficio posible sin que el peso 
acumulado supere la capacidad_maxima. """

class Nodo:
    def __init__(self, peso, beneficio, izquierdo=None, derecho=None):
        self.peso = peso
        self.beneficio = beneficio
        self.izquierdo = izquierdo # Incluir paquete
        self.derecho = derecho # No incluir el paquete

def mejor_combinacion_carga(nodo, capacidad_maxima, peso_actual=0, beneficio_actual=0):
# Caso base: si llegamos al final del árbol
    if nodo is None:
        return beneficio_actual

    #Opción 1: Incluir el paquete (ir por la izquierda)
    beneficio_incluir = float('-inf')
    nuevo_peso = peso_actual + nodo.peso
    if nuevo_peso <= capacidad_maxima:
        beneficio_incluir = mejor_combinacion_carga(
            nodo.izquierdo,
            capacidad_maxima,
            nuevo_peso,
            beneficio_actual + nodo.beneficio
        )

    #Opción 2: No incluir el paquete (ir por la derecha)
    beneficio_no_incluir = mejor_combinacion_carga(
        nodo.derecho,
        capacidad_maxima,
        peso_actual,
        beneficio_actual
    )

    # Retornamos el máximo beneficio entre ambas opciones
    return max(beneficio_incluir, beneficio_no_incluir)

# Casos de prueba:
paquete2 = Nodo(2, 3)
paquete1 = Nodo(3, 5, paquete2, paquete2)

capacidad = 4
print(mejor_combinacion_carga(paquete1, capacidad))

paq3 = Nodo(1, 5)
paq2 = Nodo(3, 15, paq3, None)
paq1 = Nodo(2, 10, paq2, paq2)
capacidad = 5
print(mejor_combinacion_carga(paq1, capacidad))

capacidad = 3
print(mejor_combinacion_carga(paq1, capacidad))
