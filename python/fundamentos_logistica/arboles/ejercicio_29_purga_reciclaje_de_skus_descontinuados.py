"""Ejercicio 29: Purga u Reciclaje de SKUs Descontinuados (Eliminación Selectiva)

Al final del año fiscal, el departamento de compras decide descontinuar un rango completo de productos cuyos IDs
caen en una categoría obsoleta (por ejemplo, todos los SKUs entre el ID L y el ID U). Escribe una función 
purgar_rango_skus(raiz, limite_inferior, limite_superior) que recorra el árbol y elimine todos los nodos que 
se encuentren dentro de ese rango inclusivo,, asegurando que la estructura final siga siendo un BST válido. """

class Nodo:
    def __init__(self, id_sku, descripcion=""):
        self.id_sku = id_sku
        self.descripcion = descripcion
        self.izquierdo = None
        self.derecho = None

def encontrar_minimo(nodo):
    """Encuentra el nodo con el menor ID"""
    actual = nodo
    while actual.izquierdo is not None:
        actual = actual.izquierdo
    return actual

def eliminar_nodo(raiz, id_sku):
    """Elimina un nodo específico del BST (usando sucesor in-order)"""
    if raiz is None:
        return raiz
    
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
        
        # Caso 3: dos hijos - usamos sucesor
        sucesor = encontrar_minimo(raiz.derecho)
        raiz.id_sku = sucesor.id_sku
        raiz.descripcion = sucesor.descripcion
        raiz.derecho = eliminar_nodo(raiz.derecho, sucesor.id_sku)
    
    return raiz

def purgar_rango_skus(raiz, limite_inferior, limite_superior):
    """
    Elimina todos los SKUs que se encuentren dentro del rango [limite_inferior, limite_superior].
    
    Args:
        raiz: raíz del BST de SKUs
        limite_inferior: ID mínimo del rango a eliminar (inclusive)
        limite_superior: ID máximo del rango a eliminar (inclusive)
    
    Returns:
        nueva raíz del BST después de la purga
    """
    # Validar límites
    if limite_inferior > limite_superior:
        print("Error: El límite inferior no puede ser mayor que el superior.")
        return raiz
    
    if raiz is None:
        print("El árbol de SKUs está vacío.")
        return None
    
    # Contar nodos antes de la purga
    nodos_antes = contar_nodos(raiz)
    
    print(f"Iniciando purga de SKUs:")
    print(f"   Rango a eliminar: [{limite_inferior} - {limite_superior}]")
    print(f"   Nodos totales antes: {nodos_antes}")
    
    # Caso base: si el nodo actual es None, retornar None
    if raiz is None:
        return None
    
    # IMPORTANTE: El orden de las operaciones es clave
    
    # 1. Si el ID actual está en el rango, lo eliminamos
    #    PERO antes debemos procesar sus hijos (especialmente el izquierdo)
    if limite_inferior <= raiz.id_sku <= limite_superior:
        # El nodo actual debe ser eliminado
        
        # Guardar los hijos antes de eliminar
        hijo_izquierdo = raiz.izquierdo
        hijo_derecho = raiz.derecho
        
        # Eliminar el nodo actual usando la función estándar
        # Esto mantiene la estructura BST
        nueva_raiz = eliminar_nodo(raiz, raiz.id_sku)
        
        # Procesar recursivamente los subárboles
        # Es importante procesar ambos subárboles después de la eliminación
        if nueva_raiz:
            # Si la raíz cambió, procesamos desde la nueva raíz
            nueva_raiz.izquierdo = purgar_rango_skus(nueva_raiz.izquierdo, limite_inferior, limite_superior)
            nueva_raiz.derecho = purgar_rango_skus(nueva_raiz.derecho, limite_inferior, limite_superior)
            return nueva_raiz
        else:
            # Si nueva_raiz es None, procesamos los hijos directamente
            hijo_izquierdo = purgar_rango_skus(hijo_izquierdo, limite_inferior, limite_superior)
            hijo_derecho = purgar_rango_skus(hijo_derecho, limite_inferior, limite_superior)
            # Necesitamos reconstruir el árbol uniendo los resultados
            if hijo_izquierdo and hijo_derecho:
                # Unir los dos subárboles (caso complejo)
                # Insertamos todos los nodos del subárbol derecho en el izquierdo
                # O viceversa - mejor usar un enfoque diferente
                return unir_subarboles(hijo_izquierdo, hijo_derecho)
            elif hijo_izquierdo:
                return hijo_izquierdo
            else:
                return hijo_derecho
    
    # 2. Si el ID actual es menor que el límite inferior,
    #    el rango está completamente en el subárbol derecho
    elif raiz.id_sku < limite_inferior:
        raiz.derecho = purgar_rango_skus(raiz.derecho, limite_inferior, limite_superior)
        return raiz
    
    # 3. Si el ID actual es mayor que el límite superior,
    #    el rango está completamente en el subárbol izquierdo
    else:  # raiz.id_sku > limite_superior
        raiz.izquierdo = purgar_rango_skus(raiz.izquierdo, limite_inferior, limite_superior)
        return raiz

def unir_subarboles(subarbol_izq, subarbol_der):
    """
    Une dos subárboles donde todos los elementos del izquierdo son menores
    que todos los del derecho.
    """
    if subarbol_izq is None:
        return subarbol_der
    if subarbol_der is None:
        return subarbol_izq
    
    # Encontrar el máximo del subárbol izquierdo
    max_izq = subarbol_izq
    while max_izq.derecho is not None:
        max_izq = max_izq.derecho
    
    # Insertar todo el subárbol derecho en el izquierdo
    # (usando inserción recursiva simple)
    def insertar_todos(raiz_destino, raiz_origen):
        if raiz_origen is None:
            return raiz_destino
        raiz_destino = insertar_nodo(raiz_destino, raiz_origen.id_sku, raiz_origen.descripcion)
        raiz_destino = insertar_todos(raiz_destino, raiz_origen.izquierdo)
        raiz_destino = insertar_todos(raiz_destino, raiz_origen.derecho)
        return raiz_destino
    
    return insertar_todos(subarbol_izq, subarbol_der)

# ===== VERSIÓN OPTIMIZADA Y MÁS SIMPLE =====

def purgar_rango_skus_optimizado(raiz, limite_inferior, limite_superior):
    """
    Versión optimizada y más simple de purgar rango de SKUs.
    Utiliza el enfoque de "reconstruir" el árbol eliminando nodos uno por uno.
    """
    # Validar límites
    if limite_inferior > limite_superior:
        print("Error: El límite inferior no puede ser mayor que el superior.")
        return raiz
    
    if raiz is None:
        print("El árbol de SKUs está vacío.")
        return None
    
    print(f"Iniciando purga de SKUs:")
    print(f"   Rango a eliminar: [{limite_inferior} - {limite_superior}]")
    print(f"   Nodos totales antes: {contar_nodos(raiz)}")
    
    # Función recursiva interna
    def purgar_recursivo(nodo):
        if nodo is None:
            return None
        
        # Primero procesamos los hijos (post-orden)
        nodo.izquierdo = purgar_recursivo(nodo.izquierdo)
        nodo.derecho = purgar_recursivo(nodo.derecho)
        
        # Ahora decidimos si el nodo actual debe ser eliminado
        if limite_inferior <= nodo.id_sku <= limite_superior:
            # Si está en el rango, lo eliminamos
            # Para mantener el BST, usamos la función de eliminación estándar
            # pero tenemos que pasar el nodo completo
            return eliminar_nodo(nodo, nodo.id_sku)
        else:
            # Si no está en el rango, lo mantenemos
            return nodo
    
    nueva_raiz = purgar_recursivo(raiz)
    
    # Contar nodos después de la purga
    nodos_despues = contar_nodos(nueva_raiz)
    eliminados = contar_nodos(raiz) - nodos_despues
    
    print(f"Purga completada:")
    print(f"Nodos eliminados: {eliminados}")
    print(f"Nodos restantes: {nodos_despues}")
    
    return nueva_raiz

# Fuciones Auxiliares

def insertar_nodo(raiz, id_sku, descripcion):
    """Inserta un SKU en el BST"""
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

def inorder_con_marcadores(nodo, limite_inferior, limite_superior, nivel=0):
    """Muestra el árbol marcando los nodos a eliminar"""
    if nodo:
        inorder_con_marcadores(nodo.izquierdo, limite_inferior, limite_superior, nivel + 1)
        marcador = "Basura" if limite_inferior <= nodo.id_sku <= limite_superior else ""
        print(f"{'  ' * nivel}ID: {nodo.id_sku}, Desc: {nodo.descripcion}{marcador}")
        inorder_con_marcadores(nodo.derecho, limite_inferior, limite_superior, nivel + 1)

def contar_nodos(raiz):
    """Cuenta el número de nodos en el árbol"""
    if raiz is None:
        return 0
    return 1 + contar_nodos(raiz.izquierdo) + contar_nodos(raiz.derecho)

def mostrar_arbol_estructurado(raiz, prefix="", es_izquierdo=True):
    """Muestra el árbol de forma estructurada"""
    if raiz is None:
        return
    
    print(f"{prefix}{'└── ' if not es_izquierdo else '├── ' if prefix else ''}{raiz.id_sku} ({raiz.descripcion[:20]})")
    
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

#Prueba:

if __name__ == "__main__":
    print("Sistema de Purga de SKUs")
    
    # Crear un inventario de SKUs de prueba
    raiz = None
    
    # Lista de SKUs (ID, descripción)
    skus = [
        (50, "Componente Electrónico A500"),
        (30, "Pieza Mecánica M300"),
        (70, "Sensor Óptico S700"),
        (20, "Resistor R200"),
        (60, "Capacitor C600"),
        (40, "Transistor T400"),
        (45, "Diodo D450"),
        (35, "Inductor I350"),
        (55, "Condensador C550"),
        (65, "Microcontrolador M650"),
        (10, "Conector X100"),
        (25, "Cableado W250"),
        (75, "Display D750"),
        (15, "Batería B150"),
        (80, "Motor M800"),
    ]
    
    print("\nregistro Inicial de SKUs:")
    for id_sku, desc in skus:
        raiz = insertar_nodo(raiz, id_sku, desc)
        print(f"   Registrado: ID {id_sku} - {desc}")
    
    print(f"\nTotal de SKUs: {contar_nodos(raiz)}")
    
    print("\nÁrbol de SKUs (inorden):")
    inorder(raiz)
    
    print("\nEstructura del árbol:")
    mostrar_arbol_estructurado(raiz)
    
    # CASO 1: Purga de rango medio
    print("\n")
    limite_inf, limite_sup = 30, 60
    print(f"\nRango a purgar: [{limite_inf} - {limite_sup}]")
    print("\nMarcando SKUs a eliminar:")
    inorder_con_marcadores(raiz, limite_inf, limite_sup)
    
    print("\n")
    raiz = purgar_rango_skus_optimizado(raiz, limite_inf, limite_sup)
    
    print("\nÁrbol después de la purga:")
    inorder(raiz)
    
    # CASO 2: Purga de rango bajo
    print("\n")
    limite_inf, limite_sup = 10, 20
    print(f"\nRango a purgar: [{limite_inf} - {limite_sup}]")
    print("\nMarcando SKUs a eliminar:")
    inorder_con_marcadores(raiz, limite_inf, limite_sup)
    
    print("\n")
    raiz = purgar_rango_skus_optimizado(raiz, limite_inf, limite_sup)
    
    print("\nÁrbol después de la purga:")
    inorder(raiz)
    
    # CASO 3: Purga de rango alto
    print("\n")
    limite_inf, limite_sup = 70, 80
    print(f"\nRango a Purgar: [{limite_inf} - {limite_sup}]")
    print("\nMarcando SKUs a eliminar:")
    inorder_con_marcadores(raiz, limite_inf, limite_sup)
    
    print("\n")
    raiz = purgar_rango_skus_optimizado(raiz, limite_inf, limite_sup)
    
    print("\nÁrbol después de la purga:")
    inorder(raiz)
    
    # CASO 4: Purga de rango que no existe
    print("\n")
    limite_inf, limite_sup = 90, 100
    print(f"\nRango a Purgar: [{limite_inf} - {limite_sup}]")
    raiz = purgar_rango_skus_optimizado(raiz, limite_inf, limite_sup)
    
    print("\nÁrbol sin cambios (no hay SKUs en ese rango):")
    inorder(raiz)
    
    # CASO 5: Purga de todo el árbol
    print("\n")
    # Encontrar el mínimo y máximo del árbol actual
    def encontrar_min(raiz):
        if raiz is None:
            return None
        while raiz.izquierdo:
            raiz = raiz.izquierdo
        return raiz.id_sku
    
    def encontrar_max(raiz):
        if raiz is None:
            return None
        while raiz.derecho:
            raiz = raiz.derecho
        return raiz.id_sku
    
    min_actual = encontrar_min(raiz)
    max_actual = encontrar_max(raiz)
    
    if min_actual is not None and max_actual is not None:
        print(f"\nPurgando todos los SKUs: [{min_actual} - {max_actual}]")
        raiz = purgar_rango_skus_optimizado(raiz, min_actual, max_actual)
        
        print("\nÁrbol después de purga total:")
        if raiz is None:
            print("El árbol está vacío - todos los SKUs han sido purgados")
        else:
            inorder(raiz)
    
    print("\n")
    print("Proceso de purga completado.")
