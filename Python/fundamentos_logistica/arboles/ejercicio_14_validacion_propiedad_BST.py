"""Ejercicio 14: Validación de Propiedad BST (Auditoría de Base de datos)

A veces, por errores de red, los árboles de inventario pierden su orden. Escribe una función 
es_bst_valido(nodo, limite_inf=float('-inf'), limite_sup=float('inf')) que verifique si un 
árbol binario cumple estrictamente con las reglas de un BST. Debe devolver True o False. """

class NodoBST:
    def __init__(self, sku_id, descripcion=""):
        self.id = sku_id                
        self.descripcion = descripcion
        self.izquierdo = None
        self.derecho = None

def es_bst_valido(nodo, limite_inf=float('-inf'), limite_sup=float('inf')):
    """
        Valida si un árbol binario cumple con las propiedades de un BST.

        Args:
            nodo: Nodo raiz del subárbol a validar
            limite_inf: Límite inferior permitido (exclusivo)
            limite_sup: Límite superior permitido (exclusivo)

        Returns:
            bool: True si es un BST válido, False en caso contrario
    """

    # Caso base: un nodo vacío es válido
    if nodo is None:
        return True

    # Verificamos que el valor del nodo esté dentro del rango permitido
    if not (limite_inf < nodo.id < limite_sup):
        return False

    #Validar recursivamente el subárbol izquierdo
    # El límite superior para la izquierda es el valor del nodo actual
    izquierdo_valido = es_bst_valido(nodo.izquierdo, limite_inf, nodo.id)

    # Validar recurvidamente el subárbol derecho
    # El límite inferior para la derecha es el valor del nodo actual
    derecho_valido = es_bst_valido(nodo.derecho, nodo.id, limite_sup)

    # El árbol es válido solo si ambos subárboles son válidos
    return izquierdo_valido and derecho_valido

# Pruebas
print("Caso 1: ")
raiz_valida = NodoBST(50, "Raíz")
raiz_valida.izquierdo = NodoBST(30, "Izquierdo")
raiz_valida.derecho = NodoBST(70, "Derecho")
raiz_valida.izquierdo.izquierdo = NodoBST(20, "Izquierdo-Izquierdo")
raiz_valida.izquierdo.derecho = NodoBST(40, "Izquierdo-Derecho")
raiz_valida.derecho.izquierdo = NodoBST(60, "Derecho-Izquierdo")
raiz_valida.derecho.derecho = NodoBST(80, "Derecho-Derecho")

print(f"¿Es BST válido? {es_bst_valido(raiz_valida)}")

print("\nCaso 2: ")
raiz_invalida1 = NodoBST(50, "Raíz")
raiz_invalida1.izquierdo = NodoBST(60, "Error: 60 > 50, pero está a la izquierda")
# 60 debería estar a la derecha, pero está a la izquierda

print(f"¿Es BST válido? {es_bst_valido(raiz_invalida1)}")

print("\nCaso 3: ")
raiz_invalida2 = NodoBST(50, "Raíz")
raiz_invalida2.izquierdo = NodoBST(30, "Izquierdo")
raiz_invalida2.izquierdo.derecho = NodoBST(45, "Ok: 45 > 30 y < 50")
raiz_invalida2.izquierdo.derecho.izquierdo = NodoBST(55, "Error: 55 > 50, pero está en subárbol izquierdo")

print(f"¿Es BST válido? {es_bst_valido(raiz_invalida2)}")

print("\nCaso 4: ")
print(f"¿Es BST válido? {es_bst_valido(None)}")

print("\nCaso 5: ")
raiz_negativos = NodoBST(-10, "Negativo")
raiz_negativos.izquierdo = NodoBST(-20, "Más negativo")
raiz_negativos.derecho = NodoBST(0, "Cero")
print(f"¿Es BST válido? {es_bst_valido(raiz_negativos)}")
