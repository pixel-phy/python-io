"""Actors and Directors Who Cooperated At Least Three Times

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| actor_id    | int     |
| director_id | int     |
| timestamp   | int     |
+-------------+---------+
timestamp is the primary key (column with unique values) for this table.
 

Write a solution to find all the pairs (actor_id, director_id) where the actor has cooperated with the director at least three times.

Return the result table in any order.

    """

import pandas as pd

def actors_and_directors(actor_director: pd.DataFrame) -> pd.DataFrame:
    df_filtered = actor_director.groupby(['actor_id', 'director_id']).filter(lambda x: len(x) >= 3)
    return df_filtered[['actor_id', 'director_id']].drop_duplicates()

# 1. Crear el DataFrame de prueba
data = {
    'actor_id': [1, 1, 1, 1, 1, 2],
    'director_id': [1, 1, 1, 2, 2, 1],
    'timestamp': [10, 11, 12, 13, 14, 15]  # Llave primaria única
}
actor_director_df = pd.DataFrame(data)

# 2. Ejecutar la función
resultado = actors_and_directors(actor_director_df)

# 3. Mostrar el resultado
print("Historial de Cooperaciones:")
print(actor_director_df)
print("\nParejas con al menos 3 colaboraciones:")
print(resultado)
