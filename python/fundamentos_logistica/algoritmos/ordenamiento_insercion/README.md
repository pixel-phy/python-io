# Algoritmo de ordenamiento por Inserción

## Definición

El ordenamiento por inserción (Insertion Sort) es un algoritmo de ordenamiento que construye la lista ordenada
de forma incremental, tomando elementos de la parte no ordenada e insertándolos en su posición correcta dentro de la parte ya ordenada. Es similar a ordenar las cartas en nuestra mano cuando jugamos con cartas. 

**Principio fundamental**: En cada caso, tomamos un elemento de la parte no ordenada y lo colocamos en la posición correcta de la parte ordenada, desplazando los elementos mayores hace la derecha. 

## Implementación general

```python
def ordenamiento_insercion(lista):
    """
    Ordena una lista usando el algoritmo de inserción (ascendente).
    
    Parámetros:
        lista: list de elementos comparables
    
    Retorna:
        list: la misma lista ordenada (modifica la original)
    
    Complejidad: O(n²) tiempo, O(1) espacio
    """
    n = len(lista)
    
    # Empezamos desde el segundo elemento (índice 1)
    for i in range(1, n):
        # Guardamos el elemento a insertar
        elemento_actual = lista[i]
        j = i - 1
        
        # Desplazamos los elementos mayores hacia la derecha
        while j >= 0 and lista[j] > elemento_actual:
            lista[j + 1] = lista[j]
            j -= 1
        
        # Insertamos el elemento en su posición correcta
        lista[j + 1] = elemento_actual
    
    return lista

# ============ VARIANTES DE IMPLEMENTACIÓN ============

# Variante 1: Orden descendente (de mayor a menor)
def ordenamiento_insercion_descendente(lista):
    """
    Ordena de mayor a menor usando inserción.
    """
    n = len(lista)
    
    for i in range(1, n):
        elemento_actual = lista[i]
        j = i - 1
        
        # Cambio: desplazamos elementos menores
        while j >= 0 and lista[j] < elemento_actual:
            lista[j + 1] = lista[j]
            j -= 1
        
        lista[j + 1] = elemento_actual
    
    return lista

# Variante 2: Con función key (como sorted())
def ordenamiento_insercion_con_key(lista, key=None, reverse=False):
    """
    Permite usar una función key y orden ascendente/descendente.
    """
    if key is None:
        key = lambda x: x
    
    n = len(lista)
    
    for i in range(1, n):
        elemento_actual = lista[i]
        valor_actual = key(elemento_actual)
        j = i - 1
        
        while j >= 0:
            valor_j = key(lista[j])
            if (not reverse and valor_j > valor_actual) or (reverse and valor_j < valor_actual):
                lista[j + 1] = lista[j]
                j -= 1
            else:
                break
        
        lista[j + 1] = elemento_actual
    
    return lista

# Variante 3: Con búsqueda binaria para inserción (optimización)
def ordenamiento_insercion_binaria(lista):
    """
    Usa búsqueda binaria para encontrar la posición de inserción.
    Reduce el número de comparaciones, pero no de desplazamientos.
    """
    import bisect
    
    n = len(lista)
    
    for i in range(1, n):
        elemento_actual = lista[i]
        # Encontrar posición usando búsqueda binaria
        posicion = bisect.bisect_left(lista, elemento_actual, 0, i)
        
        # Desplazar elementos a la derecha
        for j in range(i, posicion, -1):
            lista[j] = lista[j - 1]
        
        # Insertar en la posición correcta
        lista[posicion] = elemento_actual
    
    return lista

# Variante 4: Versión didáctica con pasos
def ordenamiento_insercion_con_pasos(lista):
    """
    Muestra el proceso paso a paso. Útil para aprendizaje.
    """
    n = len(lista)
    print(f"Inicial: {lista}\n")
    
    for i in range(1, n):
        elemento_actual = lista[i]
        j = i - 1
        
        print(f"Pasada {i}: Insertando {elemento_actual}")
        
        while j >= 0 and lista[j] > elemento_actual:
            print(f"  Desplazando {lista[j]} a la derecha")
            lista[j + 1] = lista[j]
            j -= 1
        
        lista[j + 1] = elemento_actual
        print(f"  Resultado: {lista}\n")
    
    return lista
```
--- 
## Análisis de Complejidad

### Complejidad temporal

| Caso | Descripción | Notación | Explicación |
|----------|--------|-------------| ------------- |
| **Mejor caso** | Lista ya ordenada | **O(n)** | Solo compara, no desplaza |
| **Caso promedio** | Elementos en orden aleatorio | **O(n²)** | ~n²/4 comparaciones y desplazamientos |
| **Peor caso** | Lista ordenada inversamente | **O(n²)** | ~n²/2 comparaciones y desplazamientos |

---
## Ventajas y desventajas

### Ventajas 
• Muy eficiente para listas pequeñas o casi ordenadas (O(n))
• Elgoritmo estable (preserva el orden de elementos iguales)
• Adaptativo: se beneficia de datos pre-ordenamos
• Simple de implementar y entender
• In place: no requiere memoria adicional
• Excelente para datos que llegan en tiempo real (online algorithm)

### Desventajas 
• Ineficiente para listas grandes (O(n²))
• Muchos desplazamientos en el peor caso
• No es adecuado para listas con muchos elementos
