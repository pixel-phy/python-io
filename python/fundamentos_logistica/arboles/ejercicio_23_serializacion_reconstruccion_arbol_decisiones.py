"""Ejercicio 23: Serialización y Reconstrucción de un Árbol de decisiones (MRP)

Para guardar un árbol de planeación de producción en una base de datos de texto plano (serialización), es común almacenar 
su recorrido Pre-order y su recorrido In-order. Escribe una función reconstruir_arbol(preorder, inorder) que reciba estas dos
listas de nombres y reconstruya físicamente el árbol binario original devolviendo el nodo raíz. """

class Nodo:
    def __init__(self, valor, izquierdo=None, derecho=None):
        self.valor = valor
        self.izquierdo = izquierdo
        self.derecho = derecho

def reconstruccion_arbol(preorder, inorder):
    """
    Reconstruye un árbol binario a partir de sus recorridos Pro-order e In-order.

    Args:
        preorder: Lista con el recorrido Pro-order
        Inorder: Lista con el recorrido In-order

    Returns:
        Nodo raíz del árbol reconstruido
    """

    # Validación: si las listas están vacías, no hay árbol
    if not preorder or not inorder:
        return None

    # Paso 1: El primer elemento de Pre-order es la raíz
    valor_raiz = preorder[0]
    nodo_raiz = Nodo(valor_raiz)

    # Paso 2: Encontramos la raíz en In-order
    indice_raiz = inorder.index(valor_raiz)

    # Paso 3: Separamos los subárboles en In-order
    # Elemento a la izquierda de la raíz = subárbol izquierdo
    inorder_izquierdo = inorder[:indice_raiz]

    # Elemento a la derecha de la raíz = subárbol derecho
    inorder_derecho = inorder[indice_raiz + 1:]

    # Paso 4: Separamos los subárboles en Pre-order
    # La cantidad de elementos en inorder_izquierdo nos dice cuántos elementos corresponden
    # al subárbol izquierdo en Pre-order
    preorder_izquierdo = preorder[1:1 + len(inorder_izquierdo)]
    preorder_derecho = preorder[1 + len(inorder_izquierdo):]

    # Paso 5: Reconstruimos rescursivamente
    nodo_raiz.izquierdo = reconstruccion_arbol(preorder_izquierdo, inorder_izquierdo)
    nodo_raiz.derecho = reconstruccion_arbol(preorder_derecho, inorder_derecho)

    return nodo_raiz

# Prueba:
# Recorridos de un árbol de decisionies MRP
preorder = ["PLANIFICACION", "PRODUCCION", "MATERIAS_PRIMAS", "COMPRAS", "ENSAMBLE", "LOGISTICA"]
inorder = ["MATERIAS_PRIMAS", "PRODUCCION", "COMPRAS", "PLANIFICACION", "ENSAMBLE", "LOGISTICA"]

# Reconstruimos el árbol
arbol = reconstruccion_arbol(preorder, inorder)

# Verificamos los recorridos
def obtener_preorder(nodo):
    if nodo is None:
        return []
    return [nodo.valor] + obtener_preorder(nodo.izquierdo) + obtener_preorder(nodo.derecho)

def obtener_inorder(nodo):
    if nodo is None:
        return []
    return obtener_inorder(nodo.izquierdo) + [nodo.valor] + obtener_inorder(nodo.derecho)

print("Original Pre-order:", preorder)
print("Reconstruido Pre-order:", obtener_preorder(arbol))
print("\nOriginal In-order:", inorder)
print("Reconstruido In-order:", obtener_inorder(arbol))

# Visualizamos el árbol
def imprimir_arbol(nodo, nivel=0, prefijo="Raíz: "):
    if nodo is None:
        return 
    print(" " * nivel + prefijo + nodo.valor)
    imprimir_arbol(nodo.izquierdo, nivel + 1, "I: ")
    imprimir_arbol(nodo.derecho, nivel + 1, "D: ")

print("\nÁrbol reconstruido:")
imprimir_arbol(arbol)
