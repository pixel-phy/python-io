"""Ejercicio 04: Ordenamiento por múltiples criterios (Tamaño y peso)
    
    Un almacén necesita clasificar paquetes para optimizar el espacio en los camiones.
    Primero deben ordenarse por tamaño (S, M, L, XL) y, dentro del mismo tamaño, por peso 
    (de menor a mayor). """

# Definimos el orden de los tamaños
orden_tamanos = {'S': 0, 'M': 1, 'L': 2, 'XL': 3}

def comparar_paquetes(p1, p2):
    """
    Compara dos paquetes por tamaño primero, luego por peso.
    Retorna True si p1 debe ir antes que p2.
    """
    # Comparar tamaño usando el diccionario de orden
    if orden_tamanos[p1[1]] != orden_tamanos[p2[1]]:
        return orden_tamanos[p1[1]] < orden_tamanos[p2[1]]
    # Si mismo tamaño, comparar por peso
    return p1[2] < p2[2]

def ordenar_paquetes(paquetes):
    """
    Ordena paquetes por tamaño (S < M < L < XL) y luego por peso.
    """
    lista_ordenada = list(paquetes)
    
    print("Orden de tamaños: S < M < L < XL")
    print(f"Lista inicial: {lista_ordenada}\n")
    
    for i in range(1, len(lista_ordenada)):
        actual = lista_ordenada[i]
        j = i - 1
        
        print(f"Paso {i}: Insertando paquete {actual[0]} (tamaño: {actual[1]}, peso: {actual[2]} kg)")
        
        # Mover elementos que deben ir después del actual
        while j >= 0 and not comparar_paquetes(lista_ordenada[j], actual):
            lista_ordenada[j + 1] = lista_ordenada[j]
            j -= 1
        
        lista_ordenada[j + 1] = actual
        
        print(f"  Paquete {actual[0]} insertado en posición {j + 1}")
        print(f"  Estado actual: {lista_ordenada}\n")
    
    return lista_ordenada


# Ejemplo de uso
paquetes = [
    ("PK003", "M", 5.2),
    ("PK001", "S", 2.1),
    ("PK005", "L", 8.3),
    ("PK002", "M", 3.7),
    ("PK004", "L", 7.1),
    ("PK006", "S", 1.8)
]

print("Paquetes iniciales:")
for p in paquetes:
    print(f"  {p[0]}: Tamaño {p[1]}, Peso {p[2]} kg")

print("\n")
resultado = ordenar_paquetes(paquetes)
print("Paquetes ordenados por tamaño (S, M, L, XL) y peso ascendente:")
for p in resultado:
    print(f"  {p[0]}: Tamaño {p[1]}, Peso {p[2]} kg")
