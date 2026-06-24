"""Árbol Binario

Un árbol binario es una estructura de datos jerárquica en la que cada nodo puede tener como máximo 
dos hijos, comúnmente denominados hijo izquierdo e hijo derecho.

En Investigación de Operaciones, los árboles binarios son fundamentales porque modelan perfectamente 
decisiones dicotómicas (Sí/No, Activar/Desactivar, Izquierda/Derecha). Son la base de:
    - Problemas de selección binaria (Knapsack/mochila): ¿Se incluye este proyecto/producto 
    en el portafolio (Sí/No)?
    - Árboles de clasificación y regresión (CART): Utilizados en Machine Learning para predecir demandas
    o riesgos operativos basándose en particiones binarias de los datos.
    - Algoritmos Estadísticos de Pronósticos: Estructuras de decisión jerárquica para segmentar mercados.

Conceptos clave:
    1. Hijo Izquierdo / Derecho: Punteros específicos. Si un nodo solo tiene un hijo, debemos saber
    exactamente si es el izquierdo o el derecho.
    2. Árbol binario lleno (full): Cada nodo tiene 0 o 2 hijos (ninguno tiene un solo hijo).
    3. Árbol Binario Perfecto: Un árbol lleno donde todas las hojas están exactamente al mismo nivel o
    profundidad. """

# Implementación en Python:

class NodoBinario:
    def __init__(self, nombre, valor=0):
        self.nombre = nombre
        self.valor = valor # Puede representar ganancia, costo, probabilidad, etc...
        self.izquierdo = None # Opción A
        self.derecho = None # Opción B

# Ejemplo: Selección de proyectos de inversión
"""Imagina que un comité de IO evalúa si financiar un proyecto logístico. La raíz representa evaluar 
el "Proyecto 1". La rama izquierda significa Sí financiarlo (aporta beneficio), la derecha significa 
No financiarlo (0 beneficio). """

# Creación de la estructura binaria de decisiones
raiz = NodoBinario("Evaluar Poryecto Logístico")

# Rama izquierda: Decidimos Sí invertir
raiz.izquierdo = NodoBinario("Sí invertir", 80000)

#Rama derecha: Decidimos No invertir
raiz.derecho = NodoBinario("No invertir", 0)

# Siguiente nivel: Evaluar la contratación de personal de reparto para la opción "Sí"
raiz.izquierdo.izquierdo = NodoBinario("Sí Contratar Flota Propia", -20000)
raiz.izquierdo.derecho = NodoBinario("No contratar (Subcontratar)", -5000)

# Función de visualización simplificada para árbol binario
def mostrar_arbol_binario(nodo, prefijo="Raíz: "):
    if nodo is not None:
        print(f"{prefijo}{nodo.nombre} [Valor: {nodo.valor}]")
        if nodo.izquierdo or nodo.derecho:
            mostrar_arbol_binario(nodo.izquierdo, prefijo + "(Izq/Sí) ")
            mostrar_arbol_binario(nodo.derecho, prefijo + "(Der/No) ")

    mostrar_arbol_binario(raiz)
