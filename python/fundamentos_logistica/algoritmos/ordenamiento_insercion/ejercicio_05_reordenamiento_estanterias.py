"""Ejercicio 05: Caso casi ordenado - Reordenamiento de Estanterías

    En un almacén automatizado, los productos ya están casi ordenados por código, pero hubo un error 
    en la última actualización y algunos están fuera de lugar. Debes reordenar la lista de códigos de producto
    (strings alfanuméricos) que ya está casi ordenada (solo 2-3 elementos están mal colocados). 
    Muestra la eficiencia del algoritmo de inserción para este caso. """

def ordenar_codigos_con_metricas(codigos):
    """
        Ordena códigos casi ordenador y muestra métricas de eficiencia. """
    lista_ordenada = list(codigos)
    comparaciones = 0
    movimientos = 0

    print("Ordenamiento de lista casi ordenada")
    print(f"Lista inicial: {lista_ordenada}")
    print("(Solo algunos elementos están desordenados)\n")

    for i in range(1, len(lista_ordenada)):
        actual = lista_ordenada[i]
        j = i - 1
        comparaciones_realizadas = 0

        print(f"Paso {i}: Verificando '{actual}'")

        while j >= 0 and lista_ordenada[j] > actual:
            lista_ordenada[j + 1] = lista_ordenada[j]
            j -= 1
            movimientos += 1
            comparaciones_realizadas += 1
            comparaciones += 1

        # Si no entró al while, solo hizo una comparación
        if j >= 0:
            comparaciones_realizadas += 1
            comparaciones += 1

        lista_ordenada[j+1] = actual

        print(f"    Comparaciones en este paso: {comparaciones_realizadas}")
        if comparaciones_realizadas == 1:
            print(f"    '{actual}' ya estaba en su lugar o se movió 1 posición")
        else:
            print(f"    '{actual}' se movió {comparaciones_realizadas - 1} posición(es)")
        print(f"    Estado actual: {lista_ordenada}\n")

    print("\n Métricas de eficiencia:")
    print(f"Total de comparaciones: {comparaciones}")
    print(f"Total de movimientos: {movimientos}")
    print(f"Tamaño de la lista: {len(codigos)}")
    print(f"En el peor caso (lista inversa) serían {len(codigos)*(len(codigos)-1)//2} comparaciones y movimientos")
    print(f"El algoritmo es muy eficiente cuando los datos ya están casi ordenados!")

    return lista_ordenada

#Prueba
codigos = ["A001", "A002", "A003", "A005", "A004", "A006", "A007"]

print("Lista de códigos inicial (casi ordenada):")
for i, c in enumerate(codigos):
    print(f"    [{i}] {c}")

print(f"Nota: Solo 'A005' y 'A004' están intercambiados")

print("\n")
resultado = ordenar_codigos_con_metricas(codigos)

print("\nResultado final")
print("Comparativa con lista inversa (peor caso):")
codigos_inversos = ["A007", "A006", "A005", "A004", "A003", "A002", "A001"]
print(f"Lista inversa: {codigos_inversos}")
print("En este caso, el algoritmo haría muchas más comparaciones y movimientos.")


