""" Ejericio 30: Balanceo por Rotación de Racks en Almacén (Rotación de Raíz)

En optimización de almacenamiento, si la raíz actual es un producto de muy baja rotación, el árbol se vuelve ineficiente.
Necesitamos que un nodo hijo específico (por ejemplo, el hijo derecho de la raíz) pase a ser la nueva raíz global del almacén,
reorganizando los punteros para no perder ningún SKU en el proceso. Escribe una función rotar_a_la_izquierda(raiz) que realice
esta operación física de balanceo estructural (Rotación Simple Izquierda) y devuelve la nueva raíz. """

class Nodo:
    def __init__(self, id_sku, descripcion="", factor_balance=0):
        self.id_sku = id_sku
        self.descripcion = descripcion
        self.izquierdo = None
        self.derecho = None
        self.factor_balance = factor_balance  # Para AVL (opcional)

def rotar_a_la_izquierda(raiz):
    """
    Realiza una rotación simple a la izquierda en el BST.
    El hijo derecho de la raíz se convierte en la nueva raíz.
    
    Args:
        raiz: nodo raíz del árbol (o subárbol)
    
    Returns:
        nueva raíz después de la rotación
    """
    # Validación: asegurar que la raíz existe
    if raiz is None:
        print("Error: No se puede rotar un árbol vacío.")
        return None
    
    # Validación: asegurar que tiene hijo derecho
    if raiz.derecho is None:
        print(f"Advertencia: La raíz ID {raiz.id_sku} no tiene hijo derecho para rotar.")
        print("   La rotación no se puede realizar.")
        return raiz
    
    # Paso 1: Identificar los nodos involucrados
    x = raiz                    # Raíz original
    y = x.derecho              # Hijo derecho (será nueva raíz)
    B = y.izquierdo            # Subárbol izquierdo de y
    
    # Mostrar información de la rotación
    print(f"Realizando Rotación a la Izquierda:")
    print(f"   Raíz original: ID {x.id_sku} - {x.descripcion}")
    print(f"   Nueva raíz: ID {y.id_sku} - {y.descripcion}")
    if B:
        print(f"   Subárbol B (se mueve): ID {B.id_sku}")
    else:
        print(f"   Subárbol B: (vacío)")
    
    # Paso 2: Realizar la rotación
    # y se convierte en la nueva raíz
    x.derecho = B               # El subárbol B pasa a ser el hijo derecho de x
    y.izquierdo = x             # x pasa a ser el hijo izquierdo de y
    
    # Paso 3: Actualizar factores de balance (opcional, para AVL)
    # En una implementación AVL, aquí se actualizarían los factores de balance
    actualizar_altura(x)
    actualizar_altura(y)
    
    print(f"Rotación completada exitosamente.")
    print(f"Nueva raíz: ID {y.id_sku}")
    
    return y

def actualizar_altura(nodo):
    """Actualiza la altura de un nodo (para AVL)"""
    if nodo is None:
        return 0
    
    altura_izq = actualizar_altura(nodo.izquierdo)
    altura_der = actualizar_altura(nodo.derecho)
    nodo.altura = 1 + max(altura_izq, altura_der)
    nodo.factor_balance = altura_izq - altura_der
    
    return nodo.altura

# Funciones complementarias

def rotar_a_la_derecha(raiz):
    """
    Rotación a la derecha (simétrica a rotar_a_la_izquierda)
    Incluida como complemento para completitud.
    """
    if raiz is None:
        print("Error: No se puede rotar un árbol vacío.")
        return None
    
    if raiz.izquierdo is None:
        print(f"Advertencia: La raíz ID {raiz.id_sku} no tiene hijo izquierdo para rotar.")
        return raiz
    
    x = raiz
    y = x.izquierdo
    B = y.derecho
    
    print(f"Realizando rotacińo a la Derecha:")
    print(f"   Raíz original: ID {x.id_sku}")
    print(f"   Nueva raíz: ID {y.id_sku}")
    
    x.izquierdo = B
    y.derecho = x
    
    actualizar_altura(x)
    actualizar_altura(y)
    
    return y

def rotar_a_la_izquierda_con_verificacion(raiz):
    """
    Versión mejorada con verificaciones de seguridad y
    visualización detallada del proceso.
    """
    # Validación exhaustiva
    if raiz is None:
        print("Error: Árbol vacío - no se puede realizar la rotación.")
        return None
    
    if not isinstance(raiz, Nodo):
        print("Error: El parámetro no es un nodo válido.")
        return None
    
    if raiz.derecho is None:
        print(f"Advertencia: El nodo ID {raiz.id_sku} no tiene hijo derecho.")
        print("   La rotación a la izquierda requiere un hijo derecho.")
        print("   Operación cancelada.")
        return raiz
    
    # Mostrar el árbol antes de la rotación
    print("\n")
    print("Árbol antes de la rotación:")
    mostrar_arbol_estructurado(raiz)
    
    # Realizar la rotación
    print("\nAnálisis de rotación:")
    print(f"   Nodo a rotar (raíz): ID {raiz.id_sku}")
    print(f"   Hijo derecho (nueva raíz): ID {raiz.derecho.id_sku}")
    
    # Verificar si hay subárboles intermedios
    if raiz.derecho.izquierdo:
        print(f"   Subárbol intermedio B: ID {raiz.derecho.izquierdo.id_sku} (se moverá)")
    else:
        print("   Subárbol intermedio B: (vacío)")
    
    # Realizar la rotación
    nueva_raiz = rotar_a_la_izquierda(raiz)
    
    # Mostrar el árbol después de la rotación
    print("\n")
    print("Árbol después de la rotación:")
    mostrar_arbol_estructurado(nueva_raiz)
    
    return nueva_raiz

#Funciones auxiliares

def insertar_nodo(raiz, id_sku, descripcion=""):
    """Inserta un nodo en el BST"""
    if raiz is None:
        return Nodo(id_sku, descripcion)
    
    if id_sku < raiz.id_sku:
        raiz.izquierdo = insertar_nodo(raiz.izquierdo, id_sku, descripcion)
    elif id_sku > raiz.id_sku:
        raiz.derecho = insertar_nodo(raiz.derecho, id_sku, descripcion)
    else:
        raiz.descripcion = descripcion
    
    return raiz

def inorder(nodo, nivel=0):
    """Muestra el árbol en orden"""
    if nodo:
        inorder(nodo.izquierdo, nivel + 1)
        print(f"{'  ' * nivel}ID: {nodo.id_sku}, Desc: {nodo.descripcion}")
        inorder(nodo.derecho, nivel + 1)

def mostrar_arbol_estructurado(raiz, prefix="", es_izquierdo=True):
    """Muestra el árbol de forma estructurada visualmente"""
    if raiz is None:
        return
    
    # Mostrar el nodo actual
    print(f"{prefix}{'└── ' if not es_izquierdo else '├── ' if prefix else ''}{raiz.id_sku} ({raiz.descripcion[:20]})")
    
    # Recursivamente mostrar hijos
    if raiz.izquierdo or raiz.derecho:
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

def obtener_altura(nodo):
    """Obtiene la altura de un nodo"""
    if nodo is None:
        return 0
    return 1 + max(obtener_altura(nodo.izquierdo), obtener_altura(nodo.derecho))

def verificar_bst(raiz, min_val=float('-inf'), max_val=float('inf')):
    """Verifica que el árbol cumpla con las propiedades BST"""
    if raiz is None:
        return True
    
    if not (min_val <= raiz.id_sku <= max_val):
        return False
    
    return (verificar_bst(raiz.izquierdo, min_val, raiz.id_sku - 1) and
            verificar_bst(raiz.derecho, raiz.id_sku + 1, max_val))

# Prueba del ejercicio

if __name__ == "__main__":
    print("Sistema de Rotación de Racks - Balanceo de Almacén")
    
    # Crear un árbol de prueba
    raiz = None
    
    # Insertar nodos para crear un árbol desbalanceado a la derecha
    skus = [
        (30, "Producto A - Baja rotación"),
        (20, "Producto B - Media rotación"),
        (40, "Producto C - Alta rotación"),
        (35, "Producto D - Media-Alta rotación"),
        (50, "Producto E - Muy alta rotación"),
        (45, "Producto F - Alta-Media rotación"),
    ]
    
    print("\nRegistro de productos en Almacén:")
    for id_sku, desc in skus:
        raiz = insertar_nodo(raiz, id_sku, desc)
        print(f"   Registrado: ID {id_sku} - {desc}")
    
    print(f"\nTotal de productos: {contar_nodos(raiz)}")
    print(f"Altura del árbol: {obtener_altura(raiz)}")
    
    print("\nÁrbol inicial (inorden):")
    inorder(raiz)
    
    print("\nEstructura inicial del árbol:")
    mostrar_arbol_estructurado(raiz)
    
    # Verificar que es BST válido
    print(f"\n¿Es BST válido? : {verificar_bst(raiz)}")
    
    # CASO 1: Rotación a la izquierda en la raíz
    print("\n")
    print("Caso 1: Rotación a la Izquierda en la Raíz")
    
    raiz = rotar_a_la_izquierda_con_verificacion(raiz)
    
    print("\nÁrbol después de la rotación (inorden):")
    inorder(raiz)
    
    print(f"\nTotal de productos: {contar_nodos(raiz)}")
    print(f"Altura del árbol: {obtener_altura(raiz)}")
    print(f"¿Es BST válido? : {verificar_bst(raiz)}")
    
    # CASO 2: Segunda rotación (ahora el árbol está más balanceado)
    print("\n")
    print("Caso 2: Segunda rotación para mejor balance")
    
    # Insertar más nodos para hacer el árbol más pesado a la derecha
    print("\nAgregando más productos:")
    nuevos_skus = [
        (55, "Producto G - Rotación máxima"),
        (60, "Producto H - Rotación extrema"),
        (58, "Producto I - Rotación muy alta"),
    ]
    
    for id_sku, desc in nuevos_skus:
        raiz = insertar_nodo(raiz, id_sku, desc)
        print(f"   Registrado: ID {id_sku} - {desc}")
    
    print("\nÁrbol antes de la segunda rotación:")
    mostrar_arbol_estructurado(raiz)
    
    print(f"\nAltura del árbol: {obtener_altura(raiz)}")
    
    # Realizar segunda rotación
    raiz = rotar_a_la_izquierda_con_verificacion(raiz)
    
    print("\nÁrbol después de la segunda rotación:")
    inorder(raiz)
    print(f"\nAltura del árbol: {obtener_altura(raiz)}")
    print(f"¿Es BST válido? : {verificar_bst(raiz)}")
    
    # CASO 3: Intentar rotar cuando no es posible
    print("\n")
    print("Caso 3: Intentar rotar un nodo sin hijo derecho")
    
    # Buscar un nodo hoja para intentar rotar
    def encontrar_hoja(raiz):
        if raiz is None:
            return None
        if raiz.izquierdo is None and raiz.derecho is None:
            return raiz
        # Buscar en el subárbol izquierdo primero
        hoja = encontrar_hoja(raiz.izquierdo)
        if hoja:
            return hoja
        return encontrar_hoja(raiz.derecho)
    
    hoja = encontrar_hoja(raiz)
    if hoja:
        print(f"\nIntentando rotar un nodo hoja (ID {hoja.id_sku}):")
        # La rotación debería fallar porque no tiene hijo derecho
        resultado = rotar_a_la_izquierda(hoja)
    
    # CASO 4: Demostración de rotación a la derecha (complementaria)
    print("\n")
    print("Caso 4: Demostración de Rotación a la derecha")
    
    # Crear un árbol desbalanceado a la izquierda
    raiz2 = None
    skus_izq = [
        (50, "Producto Z - Central"),
        (30, "Producto Y - Izquierda"),
        (20, "Producto X - Muy izquierda"),
        (25, "Producto W - Media izquierda"),
    ]
    
    for id_sku, desc in skus_izq:
        raiz2 = insertar_nodo(raiz2, id_sku, desc)
    
    print("\nÁrbol desbalanceado a la izquierda:")
    mostrar_arbol_estructurado(raiz2)
    
    print("\nAplicando rotación a la derecha:")
    raiz2 = rotar_a_la_derecha(raiz2)
    
    print("\nÁrbol después de rotación a la derecha:")
    mostrar_arbol_estructurado(raiz2)
