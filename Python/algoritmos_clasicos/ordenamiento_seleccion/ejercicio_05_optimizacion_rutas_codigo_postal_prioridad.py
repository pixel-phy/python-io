"""Ejercicio 05: Optimización de rutas por código postal y prioridad de cliente

    Una empresa de mensajería debe ordenar los envíos para optimizar la ruta. Primero por 
    código postal (ascendente) y dentro del mismo código postal, por prioridad del cliente 
    (1 = VIP, 2 = normal, 3 = básico) de forma ascendente (VIP primero). """

def ordenar_envios(envios: list[tuple[int, int, str]]):
    """
        Ordena envíos: primero por código postal (ascendente), y dentro del mismo código postal por prioridad
        (1=VIP, 2=normal, 3=básico) ascendente.

        Args:
            envios: Lista de tuplas (codigo_postal, prioridad, normbre_cliente)

        Returns:
            envios
    """

    n = len(envios)

    for i in range(n):
        indice_menor = i

        for j in range(i + 1, n):
            # Primero comparar por código postal
            if envios[j][0] < envios[indice_menor][0]:
                indice_menor = j

            # Si igual CP, comparar por prioridad (menor número = mejor)
            elif envios[j][0] == envios[indice_menor][0]:
                if envios[j][1] < envios[indice_menor][1]:
                    indice_menor = j

        if indice_menor != i:
            envios[i], envios[indice_menor] = envios[indice_menor], envios[i]

    return envios

envios = [
    (28015, 2, "María López"),
    (28010, 1, "Carlos García"),
    (28015, 1, "Ana Martínez"),
    (28010, 3, "Luis Pérez"),
    (28020, 2, "Elena Rodríguez"),
    (28015, 3, "Jorge Sánchez")
]

prioridad = {1: "VIP", 2: "Normal", 3: "Básico"}

print("Entrada:")
for e in envios:
    print(f" CP {e[0]} | {prioridad[e[1]]} | {e[2]}")
print("\n")

resultado = ordenar_envios(envios)

for e in resultado:
    print(f"CP {e[0]} | {prioridad[e[1]]} | {e[2]}")

