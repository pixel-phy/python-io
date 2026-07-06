"""Ejercicio 18: Encontrar el Antecesor Inmediato en la cadena de Producción

En la planeación de requerimientos de materiales (MRP), necesitas encontrar el paso inmediatamente anterior
a una orden dada. En un BST, esto equivale al antecesor in-order (el valor más grande dentro de los valores que
son menores al nodo objetivo). Escribe una función encontrar_antecesor(nodo, id_objetivo, antecesor_actual=None)
que devuelva el ID del nodo que es el paso previo al id_objetivo. """

class Nodo:
    def __init__(self, id_sku, descripcion):
        self.id = id_sku
        self.descripcion = descripcion
        self.izquierdo = None
        self.derecho = None

def encontrar_antecesor(nodo, id_objetivo, antecesor_actual=None):
    """
    Encuentra el antecesor id-order (el valor más grande menor que id_objetivo).

    Args:
        nodo: nodo actual del BST
        id_objetivo: ID del nodo cuyo antecesor buscamos
        antecesor_actual: es el mejor candidato a antecesor hasta ahora

    Returns:
        ID del antecesor, o None si no existe
    """

    # Caso base: nodo vacío
    if nodo is None:
        return antecesor_actual

    # Si encontramos el nodo objetivo
    if nodo.id == id_objetivo:
        # El antecesor es el máximo del subárbol izquierdo (si existe)
        if nodo.izquierdo is not None:
            return encontrar_maximo(nodo.izquierdo)
        # Si no tiene subárbol izquierdo, usamos el antecesor_acutal
        return antecesor_actual

    elif nodo.id < id_objetivo:
        return encontrar_antecesor(nodo.derecho, id_objetivo, nodo.id)

    # Si el nodo actual es mayor que el objetivo, buscamos en el árbol izquierdo
    return encontrar_antecesor(nodo.izquierdo, id_objetivo, antecesor_actual)

def encontrar_maximo(nodo):
    """
        Encuentra el valor máximo en un subárbol (el nodo más a la derecha).
    """
    if nodo is None:
        return None
    while nodo.derecho is not None:
        nodo = nodo.derecho
    return nodo.id

#Pruebas:

def probar_antecesor(raiz, objetivo, esperado):
    """
    Función auxiliar para probar ambas implementaciones.
    """
    resultado = encontrar_antecesor(raiz, objetivo)
 
    print(f"Objetivo: {objetivo:3d} | Esperado: {str(esperado):>4s} | "
        f"Resultado: {str(resultado):>4s}"
          f"{' PASA ' if resultado == esperado else ' FALLA '}")

# Construir árbol
raiz = Nodo(50, "SKU-50")
raiz.izquierdo = Nodo(30, "SKU-30")
raiz.derecho = Nodo(70, "SKU-70")
raiz.izquierdo.izquierdo = Nodo(20, "SKU-20")
raiz.izquierdo.derecho = Nodo(40, "SKU-40")
raiz.derecho.izquierdo = Nodo(60, "SKU-60")
raiz.derecho.derecho = Nodo(80, "SKU-80")
raiz.izquierdo.izquierdo.izquierdo = Nodo(10, "SKU-10")
raiz.izquierdo.izquierdo.derecho = Nodo(25, "SKU-25")

print("Casos de prueba - Antecesor Id-order")
print("Árbol: 10,20,25,30,40,50,60,70,80")

# Pruebas
probar_antecesor(raiz, 10, None)
probar_antecesor(raiz, 20, 10)
probar_antecesor(raiz, 25, 20)
probar_antecesor(raiz, 30, 25)
probar_antecesor(raiz, 40, 30)
probar_antecesor(raiz, 50, 40)
probar_antecesor(raiz, 60, 50)
probar_antecesor(raiz, 70, 60)
probar_antecesor(raiz, 80, 70)

# Casos con valores que no están en el árbol
print("\n")
print("Con valores no existentes")

probar_antecesor(raiz, 15, 10)
probar_antecesor(raiz, 35, 30)
probar_antecesor(raiz, 55, 50)
probar_antecesor(raiz, 75, 70)
probar_antecesor(raiz, 85, 80)
probar_antecesor(raiz, 5, None)
