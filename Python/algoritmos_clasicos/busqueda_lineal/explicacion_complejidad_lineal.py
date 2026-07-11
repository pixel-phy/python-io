"""Tecnología de los algoritmos y Notación asintótica

Las tres notaciones clave:
    • Notación $O$ (Ómicron/Big O): Define el límite superior (el peor escenario). "El algoritmo no tardará más que esto".
    • Notación $\Omega$ (Omega): Define el límite superior (el peor escenario). "Tu algoritmo tardará más que esto".
    • Notación $\Theta$ (Theta): Define el límite estricto. Ocurre cuando el mejor y el peor escenario crecen al mismo ritmo. """

# Ejemplo 1: Complejidad lineal O(n):

def buscar_elemento(lista, objetivo):
    for elemento in lista: # Se ejecuta 'n' veces 
        if elemento == objetivo: # Operación crítica
            return True
    return False

# Ejemplo 2: Complejidad cuadrática O(n²):

def encontrar_duplicados(lista):
    n = len(lista)
    for i in range(n): # Se ejecuta 'n' veces
        for j in range (i + 1, n): # Se ejecuta aproximandamente n/2 veces en promedio
            if lista[i] == lista[j]: # Operación crítica
                return True
    return False

