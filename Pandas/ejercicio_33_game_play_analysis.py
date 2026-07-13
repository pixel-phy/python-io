"""Game Play Analysis I

+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| player_id    | int     |
| device_id    | int     |
| event_date   | date    |
| games_played | int     |
+--------------+---------+
(player_id, event_date) is the primary key (combination of columns with unique values) of this table.
This table shows the activity of players of some games.
Each row is a record of a player who logged in and played a number of games (possibly 0) before logging out on someday using some device.
 

Write a solution to find the first login date for each player.

Return the result table in any order.

"""

import pandas as pd

# 1. Definimos la función
def game_analysis(activity: pd.DataFrame) -> pd.DataFrame:
    # Agrupamos por jugador y obtenemos la fecha más antigua
    result = activity.groupby('player_id')['event_date'].min().reset_index()
    # Renombramos la columna al formato esperado
    result = result.rename(columns={'event_date': 'first_login'})
    return result

# 2. Creamos el DataFrame con los datos de ejemplo
datos_prueba = {
    'player_id': [1, 1, 2, 3, 3],
    'device_id': [2, 2, 3, 1, 4],
    'event_date': ['2016-05-02', '2016-03-01', '2017-06-25', '2018-07-03', '2016-03-02'],
    'games_played': [6, 5, 1, 5, 0]
}

df_actividad = pd.DataFrame(datos_prueba)

# Convertimos la columna a tipo fecha para que ordene correctamente como fechas y no como texto
df_actividad['event_date'] = pd.to_datetime(df_actividad['event_date']).dt.date

print("--- DATOS DE ENTRADA (HISTORIAL) ---")
print(df_actividad)

# 3. Ejecutamos la función
df_resultado = game_analysis(df_actividad)

print("\n--- RESULTADO (PRIMER INICIO DE SESIÓN) ---")
print(df_resultado)
