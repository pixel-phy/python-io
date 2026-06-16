# Algoritmo de búsqueda binaria

## Definición
La búsqueda binaria (o dicotómica) es un algoritmo de búsqueda que encuentra un elemento objetivo en una 
colección ordenada dividiendo repetidamente el intervalo de búsqueda a la mitad. Compara el objetivo 
con el elemento central del intervalo y descarta la mitad donde no puede estar.

Principio fundamental: Si los datos están ordenados, podemos aprovechar esa información para descartar 
grandes porciones en cada paso.

## Implementación general
```python
def busqueda_binaria(estructura, objetivo):
    """
    Busca un objetivo en una estructura ORDENADA (lista, tupla).
    
    Parámetros:
        estructura: list o tuple ordenados (ascendente o descendente)
        objetivo: elemento a buscar
    
    Retorna:
        - int: índice donde se encuentra
        - -1: si no se encuentra
    
    Complejidad: O(log n) tiempo, O(1) espacio (iterativa)
    """
    izquierda = 0
    derecha = len(estructura) - 1
    
    # Mientras quede un intervalo válido
    while izquierda <= derecha:
        # Calcular punto medio (evitando overflow)
        medio = izquierda + (derecha - izquierda) // 2
        
        # Comparar con el objetivo
        if estructura[medio] == objetivo:
            return medio  # ¡Encontrado!
        elif estructura[medio] < objetivo:
            # Descartar mitad izquierda
            izquierda = medio + 1
        else:  # estructura[medio] > objetivo
            # Descartar mitad derecha
            derecha = medio - 1
    
    return -1  # No encontrado

# ============ VARIANTES DE IMPLEMENTACIÓN ============

# Variante 1: Versión recursiva (más elegante pero consume pila)
def busqueda_binaria_recursiva(estructura, objetivo, izquierda=0, derecha=None):
    if derecha is None:
        derecha = len(estructura) - 1
    
    # Caso base: no encontrado
    if izquierda > derecha:
        return -1
    
    medio = izquierda + (derecha - izquierda) // 2
    
    if estructura[medio] == objetivo:
        return medio
    elif estructura[medio] < objetivo:
        return busqueda_binaria_recursiva(estructura, objetivo, medio + 1, derecha)
    else:
        return busqueda_binaria_recursiva(estructura, objetivo, izquierda, medio - 1)

# Variante 2: Búsqueda del primer elemento (con duplicados)
def busqueda_binaria_primero(lista, objetivo):
    """Encuentra la PRIMERA ocurrencia en lista con duplicados."""
    izquierda = 0
    derecha = len(lista) - 1
    resultado = -1
    
    while izquierda <= derecha:
        medio = izquierda + (derecha - izquierda) // 2
        
        if lista[medio] == objetivo:
            resultado = medio  # Guardamos la posición
            derecha = medio - 1  # Seguimos buscando a la izquierda
        elif lista[medio] < objetivo:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    
    return resultado

# Variante 3: Búsqueda del último elemento (con duplicados)
def busqueda_binaria_ultimo(lista, objetivo):
    """Encuentra la ÚLTIMA ocurrencia en lista con duplicados."""
    izquierda = 0
    derecha = len(lista) - 1
    resultado = -1
    
    while izquierda <= derecha:
        medio = izquierda + (derecha - izquierda) // 2
        
        if lista[medio] == objetivo:
            resultado = medio
            izquierda = medio + 1  # Seguimos buscando a la derecha
        elif lista[medio] < objetivo:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    
    return resultado

# Variante 4: Búsqueda de inserción (dónde debería estar)
def busqueda_binaria_insercion(lista, objetivo):
    """
    Retorna el índice donde DEBERÍA estar el objetivo si no existe.
    Útil para mantener orden al insertar.
    """
    izquierda = 0
    derecha = len(lista) - 1
    
    while izquierda <= derecha:
        medio = izquierda + (derecha - izquierda) // 2
        
        if lista[medio] == objetivo:
            return medio
        elif lista[medio] < objetivo:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    
    return izquierda  # Posición de inserción
```

## Análisis de complejidad

### Complejidad Temporal

| Caso | Descripción | Notación |
|----------|--------|-------------|
| **Mejor caso** | El objetivo está en el medio (primera comparación) | **O(1)** |
| **Caso promedio** | El objetivo está en cualquier posición | **O(log n)** |
| **Peor caso** | El objetivo no existe o está en los extremos | **O(log n)** |

## Ventajas y desventajas 

### Ventajas

• Extremadamente eficiente O(log n) vs O(n) de lineal
• Escalable para conjuntos de datos masivos
• Simplemente implementable (tanto iterativo como recursivo)
• Perfecto para búsquedas repetidas en datos estáticos

### Desventajas

• Requiere datos ordenados (costo de ordenar es O(n log n))
• Ineficiente para datos dinámicos (inserciones/eliminaciones frecuentes)
• Solo funciona con acceso aleatorio (arrays, listas, no con listas enlazadas)
• No funciona con árboles no balanceados (necesita estructura especial)
