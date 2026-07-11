"""Ejercicio 07: Checksum de Vectores de Capacidad para Flotas (Fletcher-16 abreviado)

    El algoritmo clásico de suma modular simple tiene un gran defecto en IO: no detecta el orden de los datos.
    Si una matriz de capacidades de camiones cambia de [10, 20, 30] a [30, 20, 10], la suma básica da exactamente
    lo mismo, pero el modelo de asignación colapsaría al asignarle un camión chico a una ruta grande.
    Para solucionar esto se usa una versión del algoritmo de Fletcher Checksum, que depende de la posición. 

        Algoritmo: Mantén dos variables: suma_A = 0 y suma_B = 0. Por cada número en tu vector:
            1. suma_A = (suma_A + numero) % 255
            2. suma_B = (suma_B + suma_A) % 255

        Escribir una función que reciba una lista de enteros (capacidades de camiones en toneladas) y devuelva
        un único entero que contiene ambos bloques calculados como:
        (suma_B << 8) | suma_A (o simplemente una tupla (suma_A, suma_B) si prefieres no meterte con operadores de bits aún).
        
        Input de prueba: [12, 15, 22, 8, 30] """

def calcular_fletcher(capacidades:list[int]) -> tuple[int, int]:
    """Calcula el checksum Fletcher-16 para un vector de capacdidades.

        Args:
            capacidades (list): Lista de números enteros (capacidades en toneladas)

        Returns:
            tuple: (suma_A, suma_B) con los valores calculados
    """
    suma_A = 0
    suma_B = 0

    for numero in capacidades:
        # paso 1: actualizar suma_A con módulo 255
        suma_A = (suma_A + numero) % 255

        # paso 2: Actualizar suma_B con el nuevo suma_A
        suma_B = (suma_B + suma_A) % 255

    return suma_A, suma_B

capacidades_prueba = [12, 15, 22, 8, 30]

suma_A, suma_B = calcular_fletcher(capacidades_prueba)

print(f"\nVector: {capacidades_prueba}")
print(f"suma_A = {suma_A}")
print(f"suma_B = {suma_B}")

print(f"Tupla: ({suma_A}, {suma_B})")
