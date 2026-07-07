"""
DataFrame students
+-------------+--------+
| Column Name | Type   |
+-------------+--------+
| student_id  | int    |
| name        | object |
| age         | int    |
| grade       | float  |
+-------------+--------+
Write a solution to correct the errors:

The grade column is stored as floats, convert it to integers.
"""

import pandas as pd


def changeDatatype(students: pd.DataFrame) -> pd.DataFrame:
    # Convertimos la columna 'grade' a tipo entero usando .astype()
    students["grade"] = students["grade"].astype(int)

    # Retornamos el DataFrame modificado
    return students

# 1. Creamos el DataFrame original donde 'grade' tiene números decimales (float)
datos_estudiantes = {
    "student_id": [1, 2],
    "name": ["Ava", "Taylor"],
    "age": [6, 7],
    "grade": [73.0, 87.0],  # Al ponerle .0 Python los toma como floats
}

df_students = pd.DataFrame(datos_estudiantes)

print("--- ANTES DEL CAMBIO (Tipos de datos) ---")
print(df_students.dtypes)
print(df_students)
print("\n" + "-" * 45 + "\n")

# 2. Llamamos a nuestra función
df_modificado = changeDatatype(df_students)

print("--- DESPUÉS DEL CAMBIO (Tipos de datos) ---")
print(df_modificado.dtypes)
print(df_modificado)
