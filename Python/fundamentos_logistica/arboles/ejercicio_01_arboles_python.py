""" Ejercicio 01: Conceptos básicos de árboles en Python

Un árbol es una estructura de datos no lineal y jerárquica. A diferencia de las listas o matrices (que son lineales),
los árboles representan relaciones padre-hijo.

En investigación de operaciones, los árboles son la columna vertebral de:
    - Árboles de Dicisión: Evaluación de proyectos con incertidumbre (Riesgo vs. Retorno).
    - Algoritmos de Ramificación y Acotación (Branch and Bound): Para resolver problemas de 
    programación entera mixta (MILP).
    - Sistemas Jerárquicos de Producción: Descomposición de productos en componentes (BOM - Bill of Materials).

    Conceptos Clave:
    1. Raíz (Root): El nodo superior (el origen del problema o la decisión inicial).
    2. Nodo (Node): Cada punto que contiene datos (un estado, una decisión, un almacén).
    3. Hijo/Padre (Child/Parent): Relación de dependencia. Un nodo hijo se deriva de un nodo padre. 
    4. Hojas (Leaves): Nodos terminales que no tienen hijos.
    5. Subárbol (Subtree): Cualquier nodo y sus descendientes, visto como un árbol propio. """

# Implementación en Python
class NodoDecision:
    def __init__(self, nombre, costo_o_beneficio=0):
        self.nombre = nombre
        self.valor = costo_o_beneficio
        self.hijos = [] # Lista que guardará otros nodos (opciones)

    def agregar_opcion(self, nodo_hijo):
        self.hijos.append(nodo_hijo)

# Ejemplo
# 1. Crear la raíz (Decisión Inicial)
raiz = NodoDecision("Evaluar Red Logística", 0)

# 2. Crear nodos de primer nivel (Estrategias principales)
hub_A = NodoDecision("Abrir Hub en Ciudad A", -50000) # Inversión
hub_B = NodoDecision("Abrir Hub en Ciudad B", -75000)

# Conectar a la raíz
raiz.agregar_opcion(hub_A)
raiz.agregar_opcion(hub_B)

# 3. Crear nodos de segundo nivel (Sub-decisiones para Hub A)
micro_hub = NodoDecision("Instalar Micro-Hub Local", -10000)
outsourcing = NodoDecision("Contratar Flota Tercerizada", -500)

hub_A.agregar_opcion(micro_hub)
hub_A.agregar_opcion(outsourcing)

# Función simple para visualizar la estructura jerárquica
def mostrar_arbol_decisiones(nodo, nivel=0):
    indentacion = " " * nivel
    print(f"{indentacion}--> {nodo.nombre} (Valor/Costo: {nodo.valor})")
    for hijo in nodo.hijos:
        mostrar_arbol_decisiones(hijo, nivel + 1)

# Imprimir el árbol
mostrar_arbol_decisiones(raiz)
