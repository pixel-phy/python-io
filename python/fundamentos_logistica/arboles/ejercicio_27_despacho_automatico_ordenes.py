"""Ejercicio 27: Despacho automático de órdenes (eliminación de mínimo)

En una cola de prioridades logísticas gestionada en un BST, la orden con menor ID representa el pedido
más urgente y antiguo. Escribe una función despachar_orden_urgente(raiz) que localice la orden con el menor ID,
imprima un mensaje confirmando su despacho, la elimine del árbol y devuelva la nueva raíz del BST optimizado. """

class Nodo:
    def __init__(self, id_orden, descripcion=""):
        self.id_orden = id_orden
        self.descripcion = descripcion
        self.izquierdo = None
        self.derecho = None

def encontrar_minimo(nodo):
    """Encuentra el nodo con el menor ID (el más a la izquierda)"""
    actual = nodo
    while actual.izquierdo is not None:
        actual = actual.izquierdo
    return actual

def eliminar_nodo(raiz, id_orden):
    """Elimina un nodo específico del BST"""
    if raiz is None:
        return raiz

    # Buscar el nodo a eliminar
    if id_orden < raiz.id_orden:
        raiz.izquierdo = eliminar_nodo(raiz.izquierdo, id_orden)
    elif id_orden > raiz.id_orden:
        raiz.derecho = eliminar_nodo(raiz.derecho, id_orden)
    else:
        # Nodo encontrado
        # Caso 1: Nodo sin hijos o con un solo hijo
        if raiz.izquierdo is None:
            return raiz.derecho
        elif raiz.derecho is None:
            return raiz.izquierdo

        # Caso 2: Nodo con dos hijos
        # Encontrar el sucesor inorden (mínimo del subárbol derecho)
        sucesor = encontrar_minimo(raiz.derecho)

        # Copiar los datos del sucesor al nodo actual
        raiz.id_orden = sucesor.id_orden
        raiz.descripcion = sucesor.descripcion

        # Eliminar el sucesor (que ahora está duplicado)
        raiz.derecho = eliminar_nodo(raiz.derecho, sucesor.id_orden)

    return raiz

def despachar_orden_urgente(raiz):
    """
        Localiza la orden con el menor ID (más urgente), la elimina del BST
        y devuelve la nueva raiz.

        Args:
        - raiz: raiz del BST de órdenes

        Returns:
        - nueva raiz del BST después de eliminar la orden urgente
    """
    # Validar que el árbol no esté vacío
    if raiz is None:
        print("No hay órdenes pendientes para despachar.")
        return None

    # Econtrar el nodo con el menor ID (el más a la izquierda)
    nodo_minimo = encontrar_minimo(raiz)
    id_despachado = nodo_minimo.id_orden
    descripcion_despachado = nodo_minimo.descripcion

    # Mensaje de confirmación de despacho
    print(f"Orde despachada: ID {id_despachado}")
    if descripcion_despachado:
        print(f"descripcion: {descripcion_despachado}")
    print(f"La orden ha sido enviada a producción.")

    # Eliminar el nodo del árbol
    nueva_raiz = eliminar_nodo(raiz, id_despachado)

    return nueva_raiz

# Función auxiliar para mostrar el árbol
def inorder(nodo, nivel=0):
    """Muestra el árbol en orden para verificación"""
    if nodo:
        inorder(nodo.izquierdo, nivel + 1)
        print(f"{'  ' * nivel}ID: {nodo.id_orden}, Desc: {nodo.descripcion}")
        inorder(nodo.derecho, nivel + 1)

def insertar_nodo(raiz, id_orden, descripcion):
    """Inserta un nuevo nodo en el BST de forma recursiva"""
    if raiz is None:
        return Nodo(id_orden, descripcion)

    if id_orden < raiz.id_orden:
        raiz.izquierdo = insertar_nodo(raiz.izquierdo, id_orden, descripcion)
    elif id_orden > raiz.id_orden:
        raiz.derecho = insertar_nodo(raiz.derecho, id_orden, descripcion)
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
    for id_orden, descripcion in lista_lotes:
        raiz = insertar_nodo(raiz, id_orden, descripcion)

    return raiz

def contar_nodos(raiz):
    """Cuenta el número de nodos en el árbol (auxiliar)"""
    if raiz is None:
        return 0
    return 1 + contar_nodos(raiz.izquierdo) + contar_nodos(raiz.derecho)

# Prueba:
if __name__ == "__main__":
    
    # Crear un árbol con órdenes de prueba
    raiz = None

    # Lista de órdenes (ID, descripción)
    ordenes = [
        (50, "Pedido urgente - cliente VIP"),
        (30, "Pedido estándar"),
        (70, "Pedido internacional"),
        (20, "Pedido express - Prioridad alta"),
        (60, "Pedido local"),
        (40, "Pedido corporativo"),
    ]

    print("Registro de órdenes inicial")
    for id_orden, desc in ordenes:
        raiz = insertar_nodo(raiz, id_orden, desc)

    print("\n Árbol de órdenes (inorden):")
    inorder(raiz)

    # Despachar la orden más urgente (menor ID)
    print("\n")
    raiz = despachar_orden_urgente(raiz)

    print("\n Árbol después del despacho:")
    inorder(raiz)

    # Despachar otra orden para demostración
    print("\n")
    raiz = despachar_orden_urgente(raiz)
    
    print("\n Árbol después del segundo despacho:")
    inorder(raiz)
    
    # Simular que se despachan todas las órdenes
    print("\n")
    print("Despachando órdenes restantes:")
    while raiz is not None:
        raiz = despachar_orden_urgente(raiz)
        if raiz:
            print(f"    Quedan {contar_nodos(raiz)} órdenes pendientes")
    
    # Verificar que el árbol está vacío
    print("\n")
    raiz = despachar_orden_urgente(raiz)  # Esto mostrará el mensaje de "no hay órdenes"

def contar_nodos(raiz):
    """Cuenta el número de nodos en el árbol (auxiliar)"""
    if raiz is None:
        return 0
    return 1 + contar_nodos(raiz.izquierdo) + contar_nodos(raiz.derecho)
