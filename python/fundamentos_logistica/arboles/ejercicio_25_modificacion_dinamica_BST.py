"""Modificación dinámica de un BST

1. Inserción en un BST
Insertar es relativamente sencillo porque toda nueva inserción siempre se convierte en una hoja.

    - El algoritmo busca el ID en el árbol.
    - Si es menor, va a la izquierda; si es mayor, va a la derecha.
    - Cuando llega a un puntero None (un espacio vacío), ahí engancha el nuevo nodo.

2. Eliminación en un BST

Dar de baja un recurso o una orden de producción es más complejo porque no podemos dejar "huecos" 
ni desconectar las ramas hijas. Cuando queremos eliminar un nodo, nos enfrentamos a 3 escenarios posibles:

- Caso 1: El nodo es una hoja (0 hijos). Es el más fácil. Simplemente lo borramos rompiendo el puntero de su padre (se vuelve None).
- Caso 2: El nodo tiene un solo hijo. El abuelo adopta directamente al nieto. El nodo a 
eliminar se borra y su único hijo toma su lugar.
- Caso 3: El nodo tiene dos hijos. No podemos subir a ambos. Para mantener el orden del BST, debemos buscar un sustituto ideal.
        Este sustituto puede ser:
    1. El sucesor In-order (el valor más pequeño del subárbol derecho).
    2. El Antecesor In-order (el valor más grande del subárbol izquierdo)
        - El valor del sustituto reemplaza al del nodo que queremos eliminar, y luego eliminamos físicamente
        el nodo sustituto original (que por definición caerá en el Caso 1 o Caso 2). """

# Implementación en Python
class NodoBST:
    def __init__(self, sku_id, descripcion =""):
        self.id = sku_id
        self.descripcion = descripcion
        self.izquierdo = None
        self.derecho = None

def insertar_sku(nodo, sku_id, descripcion=""):
    if nodo is None:
        return NodoBST(sku_id, descripcion)
    
    if sku_id < nodo.id:
        nodo.izquierdo = insertar_sku(nodo.izquierdo, sku_id, descripcion)
    elif sku_id > nodo.id:
        nodo.derecho = insertar_sku(nodo.derecho, sku_id, descripcion)

    return nodo

def encontrar_minimo(nodo):
    actual = nodo
    while actual.izquierdo is not None:
        actual = actual.izquierdo

    return actual

def eliminar_sku(nodo, sku_id):
    if nodo is None:
        return None

    # 1. Buscar el nodo a eliminar
    if sku_id < nodo.id:
        nodo.izquierdo = eliminar_sku(nodo.izquierdo, sku_id)
    elif sku_id > nodo.id:
        nodo.derecho = eliminar_sku(nodo.derecho, sku_id)
    else:
    # Nodo encontrado. Se aplican los 3 casos:
    # Casi 1 y 2: 0 o 1 hijo
        if nodo.izquierdo is None:
            return nodo.derecho
        elif nodo.derecho is None:
            return nodo.izquierdo

        # Caso 3: Dos hijos (buscaremos el sucesor in-order)
        sucesor = encontrar_minimo(nodo.derecho)
        nodo.id = sucesor.id
        nodo.descripcion = sucesor.descripcion

        # Eliminar el sucesor en el subárbol derecho
        nodo.derecho = eliminar_sku(nodo.derecho, sucesor.id)

    return nodo

