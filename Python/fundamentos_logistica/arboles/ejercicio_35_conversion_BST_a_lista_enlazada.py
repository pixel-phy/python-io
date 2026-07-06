""" Ejercicio 35: Conversión de BST a Lista doblemente Enlazada de Despacho (In-place)

Para un sistema de secuenciación de tareas en el piso de producción, el jefe de planta necesita tomar todos los 
elementos ordenados del BST y transformarlos en una Lista Doblemente Enlazada circular o lineal para que el 
operario pueda avanzar y retroceder entre tareas usando botones de Siguiente (derecho) y Anterior (izquierdo).
Escribe una función bst_a_lista_enlazada(raiz) que relice esta conversión in-place (modificando únicamente los
punteros existentes del árbol, sin crear nuevos nodos). """

class Nodo:
    def __init__(self, id_tarea, descripcion, izquierdo=None, derecho=None):
        self.id_tarea = id_tarea
        self.descripcion = descripcion
        self.izquierdo = izquierdo
        self.derecho = derecho

def bst_a_lista_enlazada(raiz):
    """
        Convierte un BST en una lista doblemente enlazada lineal in-place.
        Retorna la cabeza de la lista enlazada.
    """
    if raiz is None:
        return None

    # Variable para mantener el nodo anterior en el recorrido
    # Usamos una lista para poder modificarla dentro de la función recursiva
    prev = [None]

    def convertir(nodo):
        """Función recursiva auxiliar que realiza la conversión."""

        if nodo is None:
            return

        # 1. Recorrer el subárbol izquierdo
        convertir(nodo.izquierdo)

        # 2. Procesar el nodo actual
        # El 'izquierdo' del nodo actual apunta al anterior
        nodo.izquierdo = prev[0]

        if prev[0] is not None:
            # El 'derecho' del anterior apunta al nodo actual
            prev[0].derecho = nodo

        # Actualizar el anterior
        prev[0] = nodo

        # 3. Recorrer el subárbol derecho
        convertir(nodo.derecho)

    # Iniciar conversión desde la raíz
    convertir(raiz)

    # Encontrar la cabeza de la lista (el nodo más a la izquierda)
    cabeza = raiz
    while cabeza and cabeza.izquierdo is not None:
        cabeza = cabeza.izquierdo

    # Asegurar que el último nodo apunte a None
    # El último nodo es 'prev[0' después de la conversión
    if prev[0] is not None:
        prev[0].derecho = None

    return cabeza

# Prueba:
raiz = Nodo(50, "Tarea Principal")
raiz.izquierdo = Nodo(30, "Subtarea A")
raiz.derecho = Nodo(70, "Subtarea B")
raiz.izquierdo.izquierdo = Nodo(20, "Subtarea A1")
raiz.izquierdo.derecho = Nodo(40, "Subtarea A2")
raiz.derecho.izquierdo = Nodo(60, "Subtarea B1")
raiz.derecho.derecho = Nodo(80, "Subtarea B2")
raiz.izquierdo.izquierdo.izquierdo = Nodo(10, "Subtarea A1a")
raiz.izquierdo.izquierdo.derecho = Nodo(25, "Subtarea A1b")

# Convertir a lista
cabeza = bst_a_lista_enlazada(raiz)

def imprimir_lista(cabeza):
        if cabeza is None:
            print("Lista vacía")
            return
        
        print("\nLista enlazada (orden in-order):")
        
        actual = cabeza
        posicion = 1
        
        while actual is not None:
            # Mostrar información del nodo
            anterior = actual.izquierdo.id_tarea if actual.izquierdo else "None"
            siguiente = actual.derecho.id_tarea if actual.derecho else "None"
            
            print(f"Nodo {posicion}:")
            print(f"  ID: {actual.id_tarea}")
            print(f"  Descripción: {actual.descripcion}")
            print(f"  Anterior: {anterior}")
            print(f"  Siguiente: {siguiente}")
            print()
            
            actual = actual.derecho
            posicion += 1
    
imprimir_lista(cabeza)
