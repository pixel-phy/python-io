""" Ejercicio 05: Ordenamiento de Envíos por distancia y Peso (Combinación Compleja)

    Una empresa de logística debe priorizar envíos. La prioridad se define por: primero los envíos 
    con menor distancia (para optimizar turas), y para la misma distancia, lo de mayor peso 
    primero (porque son más urgentes de mover). """

def ordenar_envios(envios: list[tuple[str, int, int]]):
    """ Ordena tuplas (id, distancia, peso) por distancia ascendente,
    y para misma distancia, por peso descendente """

    n = len(envios)
    
    for i in range(n - 1):
        intercambio = False

        for j in range(0, n - i - 1):
            envio_actual = envios[j]
            envio_siguiente = envios[j + 1]

            id1, dist1, peso1 = envio_actual
            id2, dist2, peso2 = envio_siguiente

            # Criterio 1: distancia ascendente
            # Criterio 2: si misma distancia, peso descendente
            debe_intercambiar = False

            if dist1 > dist2:
                debe_intercambiar = True
            elif dist1 == dist2:
            # Para peso descendente: intercambiamos si peso1 < peso2
                if peso1 < peso2:
                    debe_intercambiar = True

            if debe_intercambiar:
                envios[j], envios[j+1] = envios[j+1], envios[j]

                intercambiado = True

        if not intercambiado:
            break
    return envios

#Prueba:

envios = [
    ("E001", 150, 45),
    ("E002", 80, 30),
    ("E003", 120, 60),
    ("E004", 80, 50),
    ("E005", 200, 25),
    ("006", 120, 45)
]

print("Envíos originales:")
for e in envios:
    print(f"    {e[0]} - Dist: {e[1]}km - Peso: {e[2]}kg")

print("\nProceso de ordenamiento:")
ordenados = ordenar_envios(envios)
print("\nEnvíos ordenados:")
for e in ordenados:
    print(f"    {e[0]} - Dist: {e[1]}km - Peso: {e[2]}kg")
