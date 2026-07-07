"""
Write a solution to calculate and display the number of rows and columns of players.

Return the result as an array:

[number of rows, number of columns]

"""

import pandas as pd

def getDataframeSize(players: pd.DataFrame) -> list[int]:
    # 1. Obtenemos las dimensiones (filas, columnas) usando .shape
    dimensiones = players.shape

    # 2. Convertimos la tupla resultante a una lista y la retornamos
    return list(dimensiones)

# Prueba de uso:

datos_ejemplo = {
    "player_id": [846, 749, 155, 583, 388, 883, 355, 247, 761, 642],
    "name": [
        "Mason",
        "Riley",
        "Bob",
        "Isabella",
        "Zachary",
        "Ava",
        "Violet",
        "Thomas",
        "Jack",
        "Charlie",
    ],
    "age": [21, 30, 28, 32, 24, 23, 18, 27, 33, 36],
    "position": [
        "Forward",
        "Winger",
        "Striker",
        "Goalkeeper",
        "Midfielder",
        "Defender",
        "Striker",
        "Striker",
        "Midfielder",
        "Center-back",
    ],
    "team": [
        "RealMadrid",
        "Barcelona",
        "ManchesterUnited",
        "Liverpool",
        "BayernMunich",
        "Chelsea",
        "Juventus",
        "ParisSaint-Germain",
        "ManchesterCity",
        "Arsenal",
    ],
}

df_players = pd.DataFrame(datos_ejemplo)

resultado = getDataframeSize(df_players)

print("Resultado de la función:", resultado)
