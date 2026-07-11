"""Ejercicio 13: Árbol binario de Búsqueda (BST)

Un árbol binario de Búsqueda (BST) es un árbol binario que impone una restricción de 
    orden estricta en sus nodos. Para cualquier nodo dado (que llamaremos "Nodo Raíz Local"):
    1. Todos los nodos en su subárbol izquierdoo deben tener un valor menor que el valor del nodo 
    actual.
    2. Todos los nodos en su subárbol derecho deben tener un valor mayor que el valor del nodo actual.
    3. No se permiten valores duplicados (en la versión estándar de IO, o se manejan con contadores).

    ¿Por qué es importante en Investigación de Operaciones?

    En IO, necesitamos consultar catálogos de inventario, índices de pallets en almacenes o IDs de 
    órdenes de producción de forma masiva.
    - Si usamos una lista desordenada, buscar un elemento toma un tiempo lineal O(n) (se debe revisar uno por uno).
    - Si el árbol está balanceado como un BST, buscar un elemento toma un tiempo logarítmico de O(log n).

Impacto real: En un inventario de 1.000.000 de SKUs, una lista requiere hasta 1.000.000 de operaciones 
para encontrar un producto. Un BST balanceado lo encuentra en máximo 20 operaciones!. """

# Implementación en Python
class NodoBST:
    def __init__(self, sku_id, descripcion=""):
        self.id = sku_id                # Clave numérica para ordenar.
        self.descripcion = descripcion  # Datos del recurso
        self.izquierdo = None           # Aquí irán los IDs menores
        self.derecho = None             # Aquí irán los IDs mayores

# Ejemplo: Indexación eficiente de SKUs en bodega.
# Insertamos el primer SKU (ID 50). Se convierte en la raíz del almacén. 
raiz_bodega = NodoBST(50, "Pallet Cemento")

# Llega el SKU 30. Como 30 < 50, se va a la izquierda.
raiz_bodega.izquierdo = NodoBST(30, "Caja tornillos")

# Llega el SKU 70. Como 70 > 50, se va a la derecha.
raiz_bodega.derecho = NodoBST(70, "Contenedor Pintura")

#Llega el SKU 35.
raiz_bodega.izquierdo.derecho = NodoBST(35, "Herramientas Manuales")

# Función de búsqueda en el BST
def buscar_sku(nodo, id_buscar):
    if nodo is None:
        return None # No encontrado en bodega

    if id_buscar == nodo.id:
        return nodo.descripcion # Encontrado

    # Si lo que busco es menor, descarto toda la derecha y voy a la izquierda
    if id_buscar < nodo.id:
        return buscar_sku(nodo.izquierdo, id_buscar)

    # Si es mayor, descarto la izquierda y voy a la derecha
    return buscar_sku(nodo.derecho, id_buscar)

# Prueba de búsqueda ultra veloz
print(f"Buscando SKU 35: {buscar_sku(raiz_bodega, 35)}")
