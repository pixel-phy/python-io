"""Ejercicio 31: El "Garbage Collector" de la Cadena de Suministro

En un WMS, a veces los SKUs se registran con errores de dedo o códigos corruptos (por ejemplo, IDs 
negativos o descripciones vacías). Escribe una función limpiar_inventario_corrupto(raiz) que recorra el BST,
identifique cualquier nodo que tenga un id_sku <= 0 o una descripcipción == "", y lo  elimine fisicamente 
del árbol garantizando que el resto de los SKUs válidos mantengan la estructura y el orden del BST. """

class Nodo:
    def __init__(self, id_sku, descripcion, izquierdo=None, derecho=None):
        self.id_sku = id_sku
        self.descripcion = descripcion
        self.izquierdo = izquierdo
        self.derecho = derecho

def limpiar_inventario_corrupto(raiz):
    """
    Elimina del BST todos los nodos con id_sku <= 0 o descripcion == "".
    Retorna la nueva raíz del árbol limpio.
    """
    # Función auxiliar para encontrar el mínimo en un subárbol
    def minimo(nodo):
        while nodo.izquierdo:
            nodo = nodo.izquierdo
        return nodo

    # Función auxiliar para eliminar un nodo por ID (estándar BST)
    def eliminar_nodo(raiz, id_sku):
        if raiz is None:
            return None
        
        if id_sku < raiz.id_sku:
            raiz.izquierdo = eliminar_nodo(raiz.izquierdo, id_sku)
        elif id_sku > raiz.id_sku:
            raiz.derecho = eliminar_nodo(raiz.derecho, id_sku)
        else:
            # Nodo encontrado
            if raiz.izquierdo is None:
                return raiz.derecho
            elif raiz.derecho is None:
                return raiz.izquierdo
            else:
                # Nodo con dos hijos: reemplazar con el mínimo del subárbol derecho
                temp = minimo(raiz.derecho)
                raiz.id_sku = temp.id_sku
                raiz.descripcion = temp.descripcion
                raiz.derecho = eliminar_nodo(raiz.derecho, temp.id_sku)
        return raiz

    # Si el árbol está vacío, retornamos None
    if raiz is None:
        return None

    # Procesamiento Postorden (primero hijos, luego raíz)
    # Limpiamos los subárboles primero
    raiz.izquierdo = limpiar_inventario_corrupto(raiz.izquierdo)
    raiz.derecho = limpiar_inventario_corrupto(raiz.derecho)

    # Ahora evaluamos la raíz actual
    if raiz.id_sku <= 0 or raiz.descripcion == "":
        # Eliminamos este nodo corrupto usando la función estándar
        # Pero cuidado: necesitamos pasar la raíz del subárbol actual
        # y el ID a eliminar. Como ya tenemos los hijos limpios,
        # podemos eliminar este nodo fácilmente.
        if raiz.izquierdo is None:
            return raiz.derecho
        elif raiz.derecho is None:
            return raiz.izquierdo
        else:
            # Si tiene dos hijos, usamos la lógica estándar
            temp = minimo(raiz.derecho)
            raiz.id_sku = temp.id_sku
            raiz.descripcion = temp.descripcion
            raiz.derecho = eliminar_nodo(raiz.derecho, temp.id_sku)
            return raiz

    return raiz

#Prueba:

raiz = Nodo(10, "Producto A")
raiz.izquierdo = Nodo(5, "Producto B")
raiz.derecho = Nodo(20, "Producto C")
raiz.izquierdo.izquierdo = Nodo(3, "Producto D")
raiz.izquierdo.derecho = Nodo(8, "Producto E")
raiz.derecho.izquierdo = Nodo(15, "Producto F")
raiz.derecho.derecho = Nodo(-5, "Producto G")
raiz.izquierdo.izquierdo.izquierdo = Nodo(-2, "Producto H")  # corrupto
raiz.izquierdo.izquierdo.derecho = Nodo(7, "")  # corrupto (desc vacía)

print("Árbol original (recorrido in-order):")
def in_order(n):
    if n:
        in_order(n.izquierdo)
        print(f"ID: {n.id_sku}, Desc: '{n.descripcion}'")
        in_order(n.derecho)

in_order(raiz)

# Limpiamos
raiz_limpia = limpiar_inventario_corrupto(raiz)

print("\nÁrbol limpio (in-order):")
in_order(raiz_limpia)
