"""Ejercicio 17: Contar elementos mayores que un Umbral (control de almacén)

    Para liberar espacio en Racks de almacenamiento, necesitas saber cuántos SKUs tienen un ID 
    mayor que un valor umbral X. Escribe una función contar_mayores_que(nodo, umbral) que compute
    eficientemente el total de nodos del BST cuyo ID sea estrictamente mayor que umbral. """

class Nodo:
    def __init__(self, id_sku, descripcion):
        self.id = id_sku
        self.descripcion = descripcion
        self.izquierdo = None
        self.derecho = None

def contar_mayores_que(nodo, umbral):
    """
        Retorna la cantidad de nodos con ID estrictamente mayor que el umbral.
        Aprovecha la estructura del BST para podar ramas.
    """

    # Caso base: nodo vacío
    if nodo is None:
        return 0

    if nodo.id > umbral:
        return 1 + contar_mayores_que(nodo.izquierdo, umbral) + contar_mayores_que(nodo.derecho, umbral)

    return contar_mayores_que(nodo.derecho, umbral)

def probar(umbral, esperado, descripcion=""):
    resultado = contar_mayores_que(raiz, umbral)
    print(f"    Umbral: {umbral:3d} | Esperado: {esperado:2d} | Obtenido: {resultado:2d} | {'Pasa' if resultado == esperado else 'Falla'} {descripcion}")

raiz = Nodo(50, "SKU-50")
raiz.izquierdo = Nodo(30, "SKU-30")
raiz.derecho = Nodo(70, "SKU-70")
raiz.izquierdo.izquierdo = Nodo(20, "SKU-20")
raiz.izquierdo.derecho = Nodo(40, "SKU-40")
raiz.derecho.izquierdo = Nodo(60, "SKU-60")
raiz.derecho.derecho = Nodo(80, "SKU-80")
raiz.izquierdo.izquierdo.izquierdo = Nodo(10, "SKU-10")
raiz.izquierdo.izquierdo.derecho = Nodo(25, "SKU-25")

print("Caso 1:")
probar(-999, 9, "(todos los nodos > -999)")
probar(999, 0, "(ningún nodo > 999)")

print("\nCaso 2:")
probar(10, 8, "(todos excepto el 10)")
probar(80, 0, "(ninguno > 80)")

print("\nCaso 3:")
probar(25, 7, "(IDs > 25: 30,40,50,60,70,80)")
probar(30, 6, "(IDs > 30: 40,50,60,70,80)")
probar(40, 5, "(IDs > 40: 50,60,70,80)")
probar(50, 4, "(IDs > 50: 60,70,80)")
probar(60, 3, "(IDs > 60: 70,80)")
probar(70, 2, "(IDs > 70: 80)")

print("\nCaso 4:")
probar(15, 8, "(IDs > 15: 20,25,30,40,50,60,70,80)")
probar(35, 6, "(IDs > 35: 40,50,60,70,80)")
probar(45, 5, "(IDs > 45: 50,60,70,80)")
probar(55, 4, "(IDs > 55: 60,70,80)")
probar(65, 3, "(IDs > 65: 70,80)")
probar(75, 2, "(IDs > 75: 80)")

print("\nCaso 5:")
probar(-5, 9, "(todos los nodos > -5)")
probar(-50, 9, "(todos los nodos > -50)")
