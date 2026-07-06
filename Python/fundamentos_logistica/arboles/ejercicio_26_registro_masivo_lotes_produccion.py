""" Ejercicio 26: Registro Masivo de Lotes de Producción

En un sistema MRP, los lotes llegan en ráfagas. Escribe una función 
registrar_lotes_masivos(raiz, lista_lotes) que reciba la raíz de un BST y una lista de tuplas [(id_sku, "descripción"), ...] 
e inserte todos los elementos en el árbol de forma secuencial, devolviendo la raiz actualizada. """

class Nodo:
    def __init__(self, id_sku, descripcion):
        self.id_sku = id_sku
        self.descripcion = descripcion
        self.izquierdo = None
        self.derecho = None

def insertar_nodo(raiz, id_sku, descripcion):
    """Inserta un nuevo nodo en el BST de forma recursiva"""
    if raiz is None:
        return Nodo(id_sku, descripcion)

    if id_sku < raiz.id_sku:
        raiz.izquierdo = insertar_nodo(raiz.izquierdo, id_sku, descripcion)
    elif id_sku > raiz.id_sku:
        raiz.derecho = insertar_nodo(raiz.derecho, id_sku, descripcion)
    else:
        # Si el ID ya existe, actualizamos la descripcion (opcional)
        raiz.descripcion = descripcion

    return raiz

def registrar_lotes_masivos(raiz, lista_lotes):
    """
    Inserta múltiples lotes en el BST de forma secuencial.

    Args:
        - raiz: raíz del BST (puede ser None si está vacío)
        - lista_lotes: lista de tuplas [(id_sku, descripcion), ...]
    Returns:
        -raiz actualizada del BST
    """
    for id_sku, descripcion in lista_lotes:
        raiz = insertar_nodo(raiz, id_sku, descripcion)

    return raiz

# Prueba:
if __name__ == '__main__':
    # creamos un árbol vacío
    raiz = None

    # Lista de lotes a registrar
    lotes = [
        (101, "Componente A - Lote 1"),
        (50, "Componente B - Lote 2"),
        (200, "Componente C - Lote 3"),
        (75, "Componente D - Lote 4"),
        (150, "Componente E - Lote 5"),
        (25, "Componente F - Lote 6"),
    ]

    # Registrar todos los lotes
    raiz = registrar_lotes_masivos(raiz, lotes)

    # Función auxiliar para imprimir el árbol en orden (para verificar)
    def inorder(nodo):
        if nodo:
            inorder(nodo.izquierdo)
            print(f"ID: {nodo.id_sku}, Descripción: {nodo.descripcion}")
            inorder(nodo.derecho)

    print("Árbol BST después de registrar los lotes:")
    inorder(raiz)
