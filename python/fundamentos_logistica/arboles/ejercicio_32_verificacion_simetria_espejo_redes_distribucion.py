""" Ejercicio 32: Verificación de Simetría en Espejo de Redes de Distribución

En logística de distribución gemela (Cross-Docking con muelles de entrada y salida idénticos), necesitamos
verificar si dos centros de distribución tienen estructuras exactamente simétricas (una es el reflejo en 
espejo de la otra). Diseña una función son_espejo(raiz_centro_A, raiz_centro_B) que devuelva True si los 
árboles son copias reflejadas (el hijo izquierdo de A es idéntico en estructura y valor al hijo 
derecho de B, y viceversa). """

class Nodo:
    def __init__(self, id_centro, capacidad, izquierdo=None, derecho=None):
        self.id_centro = id_centro
        self.capacidad = capacidad
        self.izquierdo = izquierdo
        self.derecho = derecho

def son_espejo(raiz_centro_A, raiz_centro_B):
    """
        Verifica si dos árboles binarios son reflejos especulares. 
        Retorna Tru si son espejo, False en caso contrario.
        
        Args:
            - raiz_centro_A: raiz del primer centro de distribución.
            - raiz_centro_B: raiz del segundo centro de distribución.
    """

    # Caso base 1: ambos nodos son None -> son espejo
    if raiz_centro_A is None and raiz_centro_B is None:
        return True

    # Caso base 2: uno es None y el otro no -> no son espejo
    if raiz_centro_A is None or raiz_centro_B is None:
        return False

    # Verificamos:
    # 1. Valores de los nodos actuales coninciden
    # 2. El subárbol izquierdo de A es espejo del subárbol derehco de B
    # 3. El subárbol derecho de A es espejo del subárbol izquierdo de B
    return (raiz_centro_A.id_centro == raiz_centro_B.id_centro and
            raiz_centro_A.capacidad == raiz_centro_B.capacidad and
            son_espejo(raiz_centro_A.izquierdo, raiz_centro_B.derecho) and
            son_espejo(raiz_centro_A.derecho, raiz_centro_B.izquierdo))

# Prueba:
# Son espejo
centro_A = Nodo(10, 100)
centro_A.izquierdo = Nodo(5, 50)
centro_A.derecho = Nodo(15, 150)
centro_A.izquierdo.izquierdo = Nodo(3, 30)
centro_A.izquierdo.derecho = Nodo(7, 70)
centro_A.derecho.izquierdo = Nodo(12, 120)
centro_A.derecho.derecho = Nodo(20, 200)

centro_B = Nodo(10, 100)
centro_B.izquierdo = Nodo(15, 150)
centro_B.derecho = Nodo(5, 50)
centro_B.izquierdo.izquierdo = Nodo(20, 200)
centro_B.izquierdo.derecho = Nodo(12, 120)
centro_B.derecho.izquierdo = Nodo(7, 70)
centro_B.derecho.derecho = Nodo(3, 30)

print(son_espejo(centro_A, centro_B))

# No son espejo:
centro_C = Nodo(10, 100)
centro_C.izquierdo = Nodo(5, 50)
centro_C.derecho = Nodo(15, 150)
centro_C.izquierdo.izquierdo = Nodo(3, 30)
centro_C.izquierdo.derecho = Nodo(7, 70)
centro_C.derecho.izquierdo = Nodo(12, 120)
centro_C.derecho.derecho = Nodo(20, 999)  # Capacidad diferente

print(son_espejo(centro_A, centro_C))
