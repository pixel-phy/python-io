"""Ejercicio 28: Sustitución de maquinaria obsoleta (Reemplazo manual)

Un centro de mecanizado con ID X ha fallado críticamente y debe ser retirado del sistema de control.
Para no romper el árbol de flujo, diseña una función que elimine el nodo X, pero implementando el
Antecesor In-order (el máximo del subárbol izquierdo) como el nodo sustituto en el Caso 3, en lugar del
sucesor por defecto. """

class Nodo:
    def __init__(self, id_maquina, descripcion=""):
        self.id_maquina = id_maquina
        self.descripcion = descripcion
        self.izquierdo = None
        self.derecho = None

def encontrar_maximo(nodo):
    """
        Encuentra el nodo con el mayor ID (el más a la derecha)
        Este será el antecesor in-order (máximo del subárobol izquierdo)
    """
    actual = nodo
    while actual.derecho is not None:
        actual = actual.derecho
    return actual

def eliminar_maquina(raiz, id_maquina):
    """
        Elimina una máquina del BST usando el ANTECESOR in-order
        (máximo del subárbol izquierdo) como sustituto en el caso 3.

    Args:
        raiz: raiz del BST
        id_maquina: ID de la máquina a eliminar

    Returns:
        nueva raiz del BST
    """
    if raiz is None:
        return raiz

    # Buscar el nodo a eliminar
    if id_maquina < raiz.id_maquina:
        raiz.izquierdo = eliminar_maquina(raiz.izquierdo, id_maquina)
    elif id_maquina > raiz.id_maquina:
        raiz.derecho = eliminar_maquina(raiz.derecho, id_maquina)
    else:
        # Nodo encontrado
        # Caso 1: Nodo sin hijos
        if raiz.izquierdo is None and raiz.derecho is None:
            return None

        # Caso 2: Nodo con un solo hijo
        if raiz.izquierdo is None:
            return raiz.derecho
        elif raiz.derecho is None:
            return raiz.izquierdo

        # Caso 3: Nodo con dos hijos
        # Usamos el ANTECESOR in-order (máximo del subárbol izquierdo)
        antecesor = encontrar_maximo(raiz.izquierdo)

        # Copiar los datos del antecesor al nodo actual
        raiz.id_maquina = antecesor.id_maquina
        raiz.descripcion = antecesor.descripcion

        # Eliminar el antecesor (que ahora está duplicado)
        # Importante: Eliminamos del subárbol izquierdo
        raiz.izquierdo = eliminar_maquina(raiz.izquierdo, antecesor.id_maquina)

    return raiz

def reemplazar_maquina_obsoleta(raiz, id_maquina):
    """
        Función principal que retira una máquina obsoleta del sistema.

        Args:
            raiz: raiz del BST de máquinas
            id_maquina: ID de la máquina a retirar
        Returns:
            nueva raiz del BST optimizado

    """
    # Validar que el árbol no esté vacío
    if raiz is None:
        print("EL sistema de máquinas está vacío.")
        return None

    # Buscar la máquina para confirmar que existe
    def buscar_nodo(nodo, id_maquina):
        if nodo is None:
            return None
        if id_maquina == nodo.id_maquina:
            return nodo
        elif id_maquina < nodo.id_maquina:
            return buscar_nodo(nodo.izquierdo, id_maquina)
        return buscar_nodo(nodo.derecho, id_maquina)

    nodo_encontrado = buscar_nodo(raiz, id_maquina)

    if nodo_encontrado is None:
        print(f"Error: La máquina con ID {id_maquina} no existe en el sistema.")
        return raiz

    # Mostrar información de la máquina a eliminar
    print(f"Reritando maquinaria obsoleta:")
    print(f"    ID: {id_maquina}")
    print(f"    Descripción: {nodo_encontrado.descripcion}")
    print(f"    La máquina ha fallado críticamente y será retirada.")

    # Eliminar la máquina usando antecesor in-order
    nueva_raiz = eliminar_maquina(raiz, id_maquina)

    print(f"Máquina ID {id_maquina} retirada existosamente.")
    print(f"Se utilizó el antecesor in-order como reemplazo.")

    return nueva_raiz

def insertar_nodo(raiz, id_maquina, descripcion):
    """Inserta una máquina en el BST"""
    if raiz is None:
        return Nodo(id_maquina, descripcion)
    
    if id_maquina < raiz.id_maquina:
        raiz.izquierdo = insertar_nodo(raiz.izquierdo, id_maquina, descripcion)
    elif id_maquina > raiz.id_maquina:
        raiz.derecho = insertar_nodo(raiz.derecho, id_maquina, descripcion)
    else:
        raiz.descripcion = descripcion
    
    return raiz

def inorder(nodo, nivel=0):
    """Muestra el árbol en orden"""
    if nodo:
        inorder(nodo.izquierdo, nivel + 1)
        print(f"{'  ' * nivel}ID: {nodo.id_maquina}, Desc: {nodo.descripcion}")
        inorder(nodo.derecho, nivel + 1)

def mostrar_arbol_estructurado(raiz, prefix="", es_izquierdo=True):
    """Muestra el árbol de forma estructurada (visual)"""
    if raiz is None:
        return
    
    # Mostrar el nodo actual con su posición
    print(f"{prefix}{'└── ' if not es_izquierdo else '├── ' if prefix else ''}{raiz.id_maquina} ({raiz.descripcion[:20]})")
    
    # Recursivamente mostrar hijos
    if raiz.izquierdo or raiz.derecho:
        # Construir el prefijo para los hijos
        nuevo_prefix = prefix + ('    ' if es_izquierdo else '│   ')
        
        if raiz.izquierdo:
            mostrar_arbol_estructurado(raiz.izquierdo, nuevo_prefix, True)
        else:
            print(f"{nuevo_prefix}├── None")
        
        if raiz.derecho:
            mostrar_arbol_estructurado(raiz.derecho, nuevo_prefix, False)
        else:
            print(f"{nuevo_prefix}└── None")

def contar_nodos(raiz):
    """Cuenta el número de nodos en el árbol"""
    if raiz is None:
        return 0
    return 1 + contar_nodos(raiz.izquierdo) + contar_nodos(raiz.derecho)

# Prueba:
if __name__ == "__main__":
    print("Sistema de control de maquinaria")
    
    # Crear un sistema de máquinas de prueba
    raiz = None
    
    # Lista de máquinas (ID, descripción)
    maquinas = [
        (50, "Torno CNC Modelo X2000"),
        (30, "Fresadora Vertical V1500"),
        (70, "Centro de Mecanizado C5000"),
        (20, "Rectificadora R1000"),
        (60, "Máquina de Electroerosión E300"),
        (40, "Taladro Radial T800"),
        (45, "Mandrinadora M200"),
        (35, "Cepilladora P450"),
        (55, "Molinillo M600"),
        (65, "Prensa Hidráulica H700"),
    ]
    
    print("\nRegistro inicial de maquinaria:")
    for id_maq, desc in maquinas:
        raiz = insertar_nodo(raiz, id_maq, desc)
        print(f"   Registrada: ID {id_maq} - {desc}")
    
    print(f"\nTotal de máquinas: {contar_nodos(raiz)}")
    
    print("\nÁrbol de maquinaria (inorden):")
    inorder(raiz)
    
    print("\nEstructura del árbol:")
    mostrar_arbol_estructurado(raiz)
    
    # CASO 1: Eliminar una máquina con dos hijos (usará antecesor)
    print("\n")
    id_a_eliminar = 50
    raiz = reemplazar_maquina_obsoleta(raiz, id_a_eliminar)
    
    print(f"\nTotal de máquinas después: {contar_nodos(raiz)}")
    print("\nÁrbol después del reemplazo:")
    inorder(raiz)
    
    # CASO 2: Eliminar una máquina hoja
    print("\n")
    id_a_eliminar = 20
    raiz = reemplazar_maquina_obsoleta(raiz, id_a_eliminar)
    
    print(f"\nTotal de máquinas después: {contar_nodos(raiz)}")
    print("\nÁrbol después del reemplazo:")
    inorder(raiz)
    
    # CASO 3: Eliminar una máquina con un solo hijo
    print("\n")
    id_a_eliminar = 60
    raiz = reemplazar_maquina_obsoleta(raiz, id_a_eliminar)
    
    print(f"\nTotal de máquinas después: {contar_nodos(raiz)}")
    print("\nÁrbol después del reemplazo:")
    inorder(raiz)
    
    # CASO 4: Intentar eliminar una máquina que no existe
    print("\n")
    id_a_eliminar = 999
    raiz = reemplazar_maquina_obsoleta(raiz, id_a_eliminar)
    
    # CASO 5: Eliminar la raíz restante
    print("\n")
    print("Eliminando máquinas restantes:")
    while raiz is not None:
        # Obtener la raíz actual
        id_actual = raiz.id_maquina
        print(f"\n--- Eliminando máquina ID {id_actual} ---")
        raiz = reemplazar_maquina_obsoleta(raiz, id_actual)
        if raiz:
            print(f"   Quedan {contar_nodos(raiz)} máquinas")
    
    print("\n")
    print("Todas las máquinas han sido retiradas del sistema.")
