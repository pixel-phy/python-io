"""
DataFrame df1
+-------------+--------+
| Column Name | Type   |
+-------------+--------+
| student_id  | int    |
| name        | object |
| age         | int    |
+-------------+--------+

DataFrame df2
+-------------+--------+
| Column Name | Type   |
+-------------+--------+
| student_id  | int    |
| name        | object |
| age         | int    |
+-------------+--------+

Write a solution to concatenate these two DataFrames vertically into one DataFrame.
"""

import pandas as pd


def concatenateTables(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    # Concatenamos verticalmente df1 y df2 pasando ambos en una lista
    return pd.concat([df1, df2])

# 1. Creamos el primer DataFrame (df1)
datos1 = {
    "student_id": [1, 2],
    "name": ["Mason", "Ava"],
    "age": [8, 6],
}
df1 = pd.DataFrame(datos1)

# 2. Creamos el segundo DataFrame (df2)
datos2 = {
    "student_id": [3, 4],
    "name": ["Taylor", "Georgia"],
    "age": [11, 7],
}
df2 = pd.DataFrame(datos2)

print("--- DATOS DE DF1 ---")
print(df1)
print("\n--- DATOS DE DF2 ---")
print(df2)
print("\n" + "-" * 35 + "\n")

# 3. Llamamos a nuestra función
df_resultado = concatenateTables(df1, df2)

print("--- RESULTADO DE LA CONCATENACIÓN ---")
print(df_resultado)
