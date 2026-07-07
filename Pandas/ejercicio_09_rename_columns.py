"""
DataFrame students
+-------------+--------+
| Column Name | Type   |
+-------------+--------+
| id          | int    |
| first       | object |
| last        | object |
| age         | int    |
+-------------+--------+
Write a solution to rename the columns as follows:

id to student_id
first to first_name
last to last_name
age to age_in_years
"""

import pandas as pd


def renameColumns(students: pd.DataFrame) -> pd.DataFrame:
    # Creamos el diccionario con los cambios correspondientes
    nuevos_nombres = {
        "id": "student_id",
        "first": "first_name",
        "last": "last_name",
        "age": "age_in_years",
    }

    # Renombramos las columnas y retornamos el DataFrame resultante
    return students.rename(columns=nuevos_nombres)

# 1. Creamos el DataFrame original con los nombres de columna viejos
datos_estudiantes = {
    "id": [1, 2],
    "first": ["Mason", "Ava"],
    "last": ["King", "Wright"],
    "age": [6, 7],
}

df_students = pd.DataFrame(datos_estudiantes)

print("--- COLUMNAS ORIGINALES ---")
print(df_students.columns.tolist())
print(df_students)
print("\n" + "-" * 50 + "\n")

# 2. Llamamos a nuestra función
df_renombrado = renameColumns(df_students)

print("--- COLUMNAS RENOMBRADAS ---")
print(df_renombrado.columns.tolist())
print(df_renombrado)
