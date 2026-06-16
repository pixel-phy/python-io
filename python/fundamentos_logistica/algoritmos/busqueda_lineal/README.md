# Semana 13: Algoritmos clásicos en logística

## Algoritmo de búsqueda lineal

### Definición

La búsqueda lineal (o secuencial) es un algoritmo que encuentra un elemento objetivo recorriendo cada elemento de una estructura de datos en orden, desde el primero hasta el último, comparando cada uno con el valor buscado hasta encontrar una coincidencia o llegar al final.

### Implementación general

```python
def busqueda_lineal(estructura, objetivo):
    """
    Busca un objetivo en cualquier estructura iterable.
    
    Parámetros:
        estructura: list, tuple, dict (claves), str, o cualquier iterable
        objetivo: elemento a buscar
    
    Retorna:
        - El índice/posición si se encuentra
        - None (o -1) si no se encuentra
    """
    # Caso 1: Búsqueda en listas o tuplas
    for i in range(len(estructura)):
        if estructura[i] == objetivo:
            return i  # Retorna el índice
    
    # Si llegamos aquí, no se encontró
    return None  # o -1 según convención

# ============ VARIANTES DE IMPLEMENTACIÓN ============

# Variante 1: Con for-each (más Pythonica, sin índice)
def busqueda_lineal_v2(estructura, objetivo):
    for elemento in estructura:
        if elemento == objetivo:
            return True  # Solo interesa saber si existe
    return False

# Variante 2: Con while (más explícita en el control)
def busqueda_lineal_v3(estructura, objetivo):
    i = 0
    while i < len(estructura):
        if estructura[i] == objetivo:
            return i
        i += 1
    return -1

# Variante 3: Con centinela (optimización para listas grandes)
def busqueda_lineal_v4(lista, objetivo):
    """Agrega el objetivo al final para evitar verificar límites."""
    lista_copia = lista + [objetivo]  # Añadimos centinela
    i = 0
    while True:
        if lista_copia[i] == objetivo:
            if i == len(lista):  # Llegamos al centinela
                return -1
            return i
        i += 1

# Variante 4: Búsqueda de todas las ocurrencias
def busqueda_lineal_todos(estructura, objetivo):
    """Retorna TODOS los índices donde aparece el objetivo."""
    indices = []
    for i in range(len(estructura)):
        if estructura[i] == objetivo:
            indices.append(i)
    return indices  # Retorna lista vacía si no hay
```

---
## 📊 Complejidad Temporal

| Caso | Descripción | Notación |
|----------|--------|-------------|
| **Mejor caso** | El objetivo está en la primera posición | **O(1)** |
| **Caso promedio** | El objetivo está en cualquier posición | **O(n)** |
| **Peor Caso** | El objetivo está al final o no existe | **O(n)** |
---

## Ventajas y Desventajas

### Ventajas 

• No requiere datos ordenados (a diferencia de búsqueda binaria)
• Fácil de implementar y entender
• Funciona con cualquier tipo de dato (números, strings, objetos)
• Útil para estructuras pequeñas o cuando los datos cambian frecuentemente
• Bueno para búsquedas únicas en datos desordenados

### Desventajas

• Ineficiente para grandes volúmenes de datos (O(n))
• No aprovecha estructuras ordenadas 
• Puede ser lento comparado con otros métodos en conjuntos grandes


