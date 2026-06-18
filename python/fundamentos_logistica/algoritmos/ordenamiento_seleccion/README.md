## Algoritmo de ordenamiento por selección

### Definición

El ordenamiento por selección (Selection Sort) es un algoritmo de ordenamiento que divide la lista en dos 
partes: una parte ordenada (al inicio) y una parte no ordenada (al final). En cada iteración, encuentra 
el elemento más pequeño de la parte no ordenada y lo intercambia con el primer elemento de la parte no
ordenada, expandiendo así la parte ordenada.

**Principio fundamental**: En cada pasada, selecciona el mínimo de la parte restante y lo coloca en su 
posición correcta. 
```python 

def ordenamiento_seleccion(lista):
    """
    Ordena una lista usando el algoritmo de selección (ascendente).
    
    Parámetros:
        lista: list de elementos comparables
    
    Retorna:
        list: la misma lista ordenada (modifica la original)
    
    Complejidad: O(n²) tiempo, O(1) espacio
    """
    n = len(lista)
    
    # Recorremos cada posición donde debe ir el mínimo
    for i in range(n - 1):
        # Suponemos que el mínimo está en la posición actual
        indice_minimo = i
        
        # Buscamos el mínimo en el resto de la lista
        for j in range(i + 1, n):
            if lista[j] < lista[indice_minimo]:
                indice_minimo = j
        
        # Intercambiamos el mínimo encontrado con la posición actual
        if indice_minimo != i:
            lista[i], lista[indice_minimo] = lista[indice_minimo], lista[i]
    
    return lista

# ============ VARIANTES DE IMPLEMENTACIÓN ============

# Variante 1: Orden descendente (selecciona el máximo)
def ordenamiento_seleccion_descendente(lista):
    """
    Ordena de mayor a menor seleccionando el máximo.
    """
    n = len(lista)
    
    for i in range(n - 1):
        indice_maximo = i
        
        for j in range(i + 1, n):
            if lista[j] > lista[indice_maximo]:  # Cambio aquí
                indice_maximo = j
        
        if indice_maximo != i:
            lista[i], lista[indice_maximo] = lista[indice_maximo], lista[i]
    
    return lista

# Variante 2: Con función key (como sorted())
def ordenamiento_seleccion_con_key(lista, key=None, reverse=False):
    """
    Permite usar una función key y orden ascendente/descendente.
    """
    if key is None:
        key = lambda x: x
    
    n = len(lista)
    
    for i in range(n - 1):
        indice_extremo = i
        
        for j in range(i + 1, n):
            a = key(lista[j])
            b = key(lista[indice_extremo])
            
            if (not reverse and a < b) or (reverse and a > b):
                indice_extremo = j
        
        if indice_extremo != i:
            lista[i], lista[indice_extremo] = lista[indice_extremo], lista[i]
    
    return lista

# Variante 3: Selección simultánea (encuentra min y max)
def ordenamiento_seleccion_simultaneo(lista):
    """
    Encuentra el mínimo Y el máximo en cada pasada para reducir pasadas.
    """
    n = len(lista)
    inicio = 0
    fin = n - 1
    
    while inicio < fin:
        indice_min = inicio
        indice_max = inicio
        
        # Buscar mínimo y máximo en el rango actual
        for i in range(inicio, fin + 1):
            if lista[i] < lista[indice_min]:
                indice_min = i
            if lista[i] > lista[indice_max]:
                indice_max = i
        
        # Colocar el mínimo al inicio
        if indice_min != inicio:
            lista[inicio], lista[indice_min] = lista[indice_min], lista[inicio]
            
            # Si el máximo estaba en inicio, se movió
            if indice_max == inicio:
                indice_max = indice_min
        
        # Colocar el máximo al final
        if indice_max != fin:
            lista[fin], lista[indice_max] = lista[indice_max], lista[fin]
        
        inicio += 1
        fin -= 1
    
    return lista

# Variante 4: Versión didáctica con pasos
def ordenamiento_seleccion_con_pasos(lista):
    """
    Muestra el proceso paso a paso. Útil para aprendizaje.
    """
    n = len(lista)
    print(f"Inicial: {lista}\n")
    
    for i in range(n - 1):
        indice_minimo = i
        print(f"Pasada {i+1}: Buscando mínimo desde posición {i}")
        
        for j in range(i + 1, n):
            if lista[j] < lista[indice_minimo]:
                indice_minimo = j
                print(f"  Nuevo mínimo en {j}: {lista[j]}")
        
        if indice_minimo != i:
            print(f"  Intercambiando {lista[i]} con {lista[indice_minimo]}")
            lista[i], lista[indice_minimo] = lista[indice_minimo], lista[i]
            print(f"  Resultado: {lista}")
        else:
            print(f"  {lista[i]} ya está en su lugar")
        
        print()
    
    return lista

```
---
## Complejidad Temporal

| Caso | Descripción | Notación | Explicación |
|------|-------------|----------|-------------|
| **Mejor caso** | Lista ya ordenada | **O(n²)** | Sigue buscando el mínimo en cada pasada |
| **Caso promedio** | Elementos en orden aleatorio | **O(n²)** | ~n²/2 comparaciones |
| **Peor caso** | Lista ordeada inversamente | **O(n²)** | ~n²/2 comparaciones |
---

## Ventajas y desventajas

### Ventajas

• Muy simple de entender e implementar
• Pocos intercambios (máximo n-1) vs burbuja
• No requiere memoria adicional (in-place)
• Rendimiento predecible (siempre O(n²) independientemente de los datos)
• Útil cuando el costo de intercambiar es alto (pocos intercambios)

### Desventajas

• Ineficiente para datos grandes (O(n²))
• No es estable (no preserva el orden de elementos iguales)
• Siempre hace el mismo número de comparaciones (incluso en listas ordenadas)
• No es adaptativo (no se beneficia de datos pre-ordenados)
