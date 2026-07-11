""" Recorridos en Áboles
Recorrer un árbol significa visitar cada uno de sus nodos exactamente una vez en un orden sistemático. Mientras que en una lista 
lineal solo se puede ir hacia adelante o hacia atrás, en las estructuras jerárquicas tenemos dos grandes familiar de recorridos:

1. Recorridos en profundidad (DFS - Depth-first Searh)

Exploran una rama por completo hacia el fondo antes de retroceder. Dependiendo del momento en que se procese el nodo raíz 
con respecto a sus hijos, se dividen en tres:
- In-order (Izquierda -> Raíz -> Derecha): En un BST, este recorrido extrae los elementos en orden ascendente.
- Pro-order (Raíz -> Izquierda -> Derecha): Excelente para duplicar o clonar estructuras de red, ya que creas el nodo 
padre antes de intentar crear a sus hijos.
- Post-order (Izquierda -> Derecha -> Raíz): Ideal para cálculos acumulativos de abajo hacia arriba. En IO, se usa para 
calcular el costo total de un producto ensamblado (BOM), asegurando que sumas el costo de los tornillos y piezas antes
de calcular el costo del subensamble final. 

2. Recorrido en amplitud / Por niveles (BFS - Breadth-first Search)

Visita los nodos nivel por nivel, de izquierda a derecha (la raíz, luego todos sus hijos, luego todos sus nietos).
- Aplicación en IO: Es la base para simulaciones de procesos concurrentes y para encontrar la ruta con el menor 
número de escalas oo transbordos en una red de distribución. """

# Implementación en Python

class Nodo:
    def __init__(self, nombre, valor=0):
        self.nombre = nombre
        self.valor = valor
        self.izquierdo = None
        self.dereche = None

def recorrido_preorder(nodo):
    if nodo:
        print(f"-> {nodo.nombre}", end=" ") # Procesar raíz
        recorrido_preorder(nodo.izquierdo)  # Ir a Izquierda
        recorrido_preorder(nodo.derecho)    # Ir a Derecha

def recorrido_inorder(nodo):
    if nodo:
        recorrido_inorder(nodo.izquierdo)   # Ir a izquierda
        print(f"-> {nodo.nombre}", end= " ") # Procesar Raíz
        recorrido_inorder(nodo.derecho)     # Ir a derecha

def recorrido_postorder(nodo):
    if nodo:
        recorrido_postorder(nodo.izquierdo) # Ir a izquierda
        recorrido_postorder(nodo.derecho)   # Ir a derecha
        print(f"-> {nodo.nombre}", end=" ") # Procesar Raíz


