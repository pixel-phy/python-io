"""
DataFrame students
+-------------+--------+
| Column Name | Type   |
+-------------+--------+
| student_id  | int    |
| name        | object |
| age         | int    |
+-------------+--------+
There are some rows having missing values in the name column.

Write a solution to remove the rows with missing values.
"""
import numpy as np
import pandas as pd

def dropMissingData(students: pd.DataFrame) -> pd.DataFrame:
    # Eliminamos las filas donde la columna 'name' tenga valores nulos (NaN)
    return students.dropna(subset=["name"])

# 1. Creamos datos de ejemplo con valores nulos (None) en la columna 'name'
datos_estudiantes = {
    "student_id": [32, 217, 779, 849],
    "name": ["Jon", None, "Sally", None],  # Aquí faltan dos nombres
    "age": [10, 19, 9, 23],
}

df_students = pd.DataFrame(datos_estudiantes)

print("--- DATOS ORIGINALES (Con valores faltantes) ---")
print(df_students)
print("\n" + "-" * 45 + "\n")

# 2. Llamamos a nuestra función
df_limpio = dropMissingData(df_students)

print("--- DATOS LIMPIOS (Sin nulos en 'name') ---")
print(df_limpio)
