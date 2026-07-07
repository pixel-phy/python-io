"""
DataFrame students
+-------------+--------+
| Column Name | Type   |
+-------------+--------+
| student_id  | int    |
| name        | object |
| age         | int    |
+-------------+--------+

Write a solution to select the name and age of the student with student_id = 101.
"""
import pandas as pd

def selectData(students: pd.DataFrame) -> pd.DataFrame:
    return students.loc[students["student_id"] == 101, ["name", "age"]]

# 1. Creamos un DataFrame de prueba con varios estudiantes
datos_estudiantes = {
    "student_id": [101, 102, 103, 104],
    "name": ["Ulysses", "Luis", "Marisa", "Niomi"],
    "age": [13, 14, 12, 13],
}

df_students = pd.DataFrame(datos_estudiantes)

print("--- DATOS ORIGINALES ---")
print(df_students)
print("\n" + "-" * 30 + "\n")

# 2. Llamamos a la función
resultado = selectData(df_students)

print("--- RESULTADO DEL FILTRADO ---")
print(resultado)
