"""Ejercicio 15: Búsqueda del SKU de Menor costo o identificador

En una cola de prioridades de órdenes de despacho guardadas en un BST, el nodo de la extrema 
izquierda siempre contiene la prioridad mínima. Escribe una función encontrar_minimo_sku(nodo)
que devuelva los datos (id y descripción) del nodo con el menor ID del árbol sin explorar nodos innecesarios. """

class NodoBST:
    def __init__(self, sku_id, descripcion=""):
        self.id = sku_id
        self.descripcion = descripcion
        self.izquierdo = None
        self.derecho = None

class InventarioBST:
    def __init__(self):
        self.raiz = None
        self.tamaño = 0
    
    def insertar(self, sku_id, descripcion=""):
        if self.raiz is None:
            self.raiz = NodoBST(sku_id, descripcion)
        else:
            self._insertar_recursivo(self.raiz, sku_id, descripcion)
        self.tamaño += 1
    
    def _insertar_recursivo(self, nodo, sku_id, descripcion):
        if sku_id < nodo.id:
            if nodo.izquierdo is None:
                nodo.izquierdo = NodoBST(sku_id, descripcion)
            else:
                self._insertar_recursivo(nodo.izquierdo, sku_id, descripcion)
        elif sku_id > nodo.id:
            if nodo.derecho is None:
                nodo.derecho = NodoBST(sku_id, descripcion)
            else:
                self._insertar_recursivo(nodo.derecho, sku_id, descripcion)
        else:
            nodo.descripcion = descripcion
            self.tamaño -= 1
    
    def recorrido_inorden(self):
        resultado = []
        self._inorden_recursivo(self.raiz, resultado)
        return resultado
    
    def _inorden_recursivo(self, nodo, resultado):
        if nodo:
            self._inorden_recursivo(nodo.izquierdo, resultado)
            resultado.append((nodo.id, nodo.descripcion))
            self._inorden_recursivo(nodo.derecho, resultado)

def encontrar_minimo_sku(nodo):
    """
        Encuentra el SKU con el menor ID en el árbol BST.
        El mínimo siempre está en el nodo más a la izquierda.

        Args:
            nodo: Nodo raíz del árbol o subárbol

        Returns:
            tuple: (id, descripcion) del SKU mínimo, o None si el árbol está vacío
    """

    # Caso: Árbol vacío
    if nodo is None:
        return None

    # Bajar por la izquierda hasta encontrar el último nodo
    while nodo.izquierdo is not None:
        nodo = nodo.izquierdo

    # Hemos llegado al nodo más a la izquierda (el mínimo)
    return (nodo.id, nodo.descripcion)

# Pruebas:

print("Caso 1: ")
inventario = InventarioBST()
productos = [
    (50, "Pallet Cemento"),
    (30, "Caja tornillos"),
    (70, "Contenedor Pintura"),
    (20, "Cinta Aislante"),
    (40, "Herramientas Manuales"),
    (60, "Láminas Metalicas"),
    (80, "Equipo Seguridad"),
    (10, "Baterías"),
    (35, "Llaves")
]

for sku, desc in productos:
    inventario.insertar(sku, desc)

minimo = encontrar_minimo_sku(inventario.raiz)
print(f"SKU mínimo: {minimo}")

print("\nCaso 2: ")
inventario_vacio = InventarioBST()
minimo_vacio = encontrar_minimo_sku(inventario_vacio.raiz)
print(f"SKU mínimo en árbol vacío: {minimo_vacio}")

print("\nCaso 3")
inventario_una_raiz = InventarioBST()
inventario_una_raiz.insertar(100, "Producto Único")
minimo_raiz = encontrar_minimo_sku(inventario_una_raiz.raiz)
print(f"SKU mínimo (solo raíz): {minimo_raiz}")

print("\nCaso 4: ")
inventario_derecha = InventarioBST()
for i in [10, 20, 30, 40, 50]:
    inventario_derecha.insertar(i, f"Producto {i}")

minimo_derecha = encontrar_minimo_sku(inventario_derecha.raiz)
print(f"SKU mínimo: {minimo_derecha}")
print(f"Recorrido completo: {inventario_derecha.recorrido_inorden()}")

print("\nCaso 5: ")
inventario_izquierda = InventarioBST()
for i in [50, 40, 30, 20, 10]:
    inventario_izquierda.insertar(i, f"Producto {i}")

minimo_izquierda = encontrar_minimo_sku(inventario_izquierda.raiz)
print(f"SKU mínimo: {minimo_izquierda}")
