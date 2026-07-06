## Algoritmo de Ordenamiento burbuja (Bubble sort)

### Definición

El ordenamiento burbuja es un algoritmo de ordenamiento simple que funciona revisando repetidamente una lista,
comparando elementos adyacentes e intercambiándolos si están en el orden incorrecto. Este proceso se repite
hasta que no se necesitan más intercambios, lo que indica que la lista está ordenada. 

**Principio fundamental**: Los elementos más grandes "burbujean" hacia el final de la lista en cada pasada,
como burbujas en un líquido.

### Implementación general
```python
def ordenamiento_burbuja(lista):
    """
    Ordena una lista usando el algoritmo de burbuja (ascendente).
    
    Parámetros:
        lista: list de elementos comparables
    
    Retorna:
        list: la misma lista ordenada (modifica la original)
    
    Complejidad: O(n²) tiempo, O(1) espacio
    """
    n = len(lista)
    
    # Pasadas externas: necesitamos n-1 pasadas
    for i in range(n - 1):
        # Pasadas internas: comparamos adyacentes
        for j in range(n - 1 - i):
            # Si están en orden incorrecto, intercambiamos
            if lista[j] > lista[j + 1]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    
    return lista

# ============ VARIANTES DE IMPLEMENTACIÓN ============

# Variante 1: Con bandera de optimización (early exit)
def ordenamiento_burbuja_optimizado(lista):
    """
    Versión optimizada que termina temprano si la lista ya está ordenada.
    """
    n = len(lista)
    
    for i in range(n - 1):
        intercambiado = False  # Bandera
        
        for j in range(n - 1 - i):
            if lista[j] > lista[j + 1]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                intercambiado = True
        
        # Si no hubo intercambios, la lista ya está ordenada
        if not intercambiado:
            break
    
    return lista

# Variante 2: Burbuja bidireccional (Cocktail Sort)
def ordenamiento_cocktail(lista):
    """
    Burbuja que va en ambas direcciones (mejor rendimiento promedio).
    """
    n = len(lista)
    inicio = 0
    fin = n - 1
    intercambiado = True
    
    while intercambiado:
        intercambiado = False
        
        # Pasada de izquierda a derecha (burbujea el mayor)
        for i in range(inicio, fin):
            if lista[i] > lista[i + 1]:
                lista[i], lista[i + 1] = lista[i + 1], lista[i]
                intercambiado = True
        
        if not intercambiado:
            break
        
        intercambiado = False
        fin -= 1  # El último elemento ya está en su lugar
        
        # Pasada de derecha a izquierda (burbujea el menor)
        for i in range(fin - 1, inicio - 1, -1):
            if lista[i] > lista[i + 1]:
                lista[i], lista[i + 1] = lista[i + 1], lista[i]
                intercambiado = True
        
        inicio += 1  # El primer elemento ya está en su lugar
    
    return lista

# Variante 3: Con conteo de pasadas (versión didáctica)
def ordenamiento_burbuja_con_pasadas(lista):
    """
    Muestra el proceso paso a paso. Útil para aprendizaje.
    """
    n = len(lista)
    pasada = 1
    
    for i in range(n - 1):
        print(f"\n--- Pasada {pasada} ---")
        intercambiado = False
        
        for j in range(n - 1 - i):
            print(f"  Comparando {lista[j]} y {lista[j+1]}")
            if lista[j] > lista[j + 1]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                intercambiado = True
                print(f"  ¡Intercambio! → {lista}")
            else:
                print(f"  Sin intercambio")
        
        if not intercambiado:
            print("¡No hubo intercambios! Lista ordenada.")
            break
        
        pasada += 1
    
    return lista
```

---
## 📊 Complejidad Temporal

| Caso | Descripción | Notación | Explicación |
|----------|--------|------------|-------------|
| **Mejor caso** | Lista ordenada (con optimización) | **O(n)** | Solo una pasada |
| **Mejor caso** | Lista ya ordenada (sin optimización) | **O(n²)** | Sigue haciendo todas las pasadas |
| **Caso promedio** | Elemento en orden aleatorio | **O(n²)** | ~n²/2 comparaciones |
| **Peor Caso** | Lista ordenada inversamente | **O(n²)** | ~n²/2 comparaciones e intercambios |
---

## Ventajas y desventajas

### Ventajas

• Muy simple de entender e implementar
• No requiere memoria adicional (in-place)
• Estable: preserva el orden de elementos iguales
• Fácil de optimizar con banderas y variantes
• Útil para listas pequeñas o casi ordenadas

### Desventajas

• Extremadamente lento para datos grandes (O(n²))
• Ineficiente comparado con algoritmos modernos
• Muchos intercambios (operaciones costosas)
• No es adecuado para producción en sistemas reales
• El peor caso es muy común (listas inversas)
