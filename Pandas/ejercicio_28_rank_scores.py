"""Rank Scores

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| score       | decimal |
+-------------+---------+
id is the primary key (column with unique values) for this table.
Each row of this table contains the score of a game. Score is a floating point value with two decimal places.
 

Write a solution to find the rank of the scores. The ranking should be calculated according to the following rules:

The scores should be ranked from the highest to the lowest.
If there is a tie between two scores, both should have the same ranking.
After a tie, the next ranking number should be the next consecutive integer value. In other words, there should be no holes between ranks.
Return the result table ordered by score in descending order.

"""

import pandas as pd

def order_scores(scores: pd.DataFrame) -> pd.DataFrame:
    # 1. Ordenamos la tabla por puntaje de mayor a menor
    scores = scores.sort_values(by='score', ascending=False)

    # 2. Calculamos el ranking usando el método 'dense' de mayor a menor
    scores['rank'] = scores['score'].rank(method='dense', ascending=False).astype(int)
    return scores[['score', 'rank']]

# Ejemplo de uso:

datos_juego = {
    'id': [1, 2, 3, 4, 5, 6],
    'score': [3.50, 4.00, 4.00, 3.85, 4.00, 3.65]
}

df_original = pd.DataFrame(datos_juego)

print("=== DATOS ORIGINALES ===")
print(df_original)
print("\n" + "-"*30 + "\n")

# 3. Ejecutamos nuestra función
df_resultado = order_scores(df_original)

print("=== RESULTADO DEL RANKING ===")
print(df_resultado.to_string(index=False)) # to_string oculta los índices internos de Pandas
