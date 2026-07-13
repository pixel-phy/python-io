"""Number of Unique Subjects Taught by Each Teacher

+-------------+------+
| Column Name | Type |
+-------------+------+
| teacher_id  | int  |
| subject_id  | int  |
| dept_id     | int  |
+-------------+------+
(subject_id, dept_id) is the primary key (combinations of columns with unique values) of this table.
Each row in this table indicates that the teacher with teacher_id teaches the subject subject_id in the department dept_id.
 

Write a solution to calculate the number of unique subjects each teacher teaches in the university.

Return the result table in any order.

"""

import pandas as pd

# 1. Definimos la función
def count_unique_subjects(teacher: pd.DataFrame) -> pd.DataFrame:
    result = teacher.groupby('teacher_id')['subject_id'].nunique().reset_index()
    result = result.rename(columns={'subject_id': 'cnt'})
    return result

# 2. Creamos datos de prueba
# El profesor 1 enseña la materia 2 en dos departamentos distintos (filas 0 y 1)
# El profesor 1 también enseña la materia 3 (fila 2)
# El profesor 2 enseña las materias 1, 2, 3 y 4 en el mismo departamento
datos_prueba = {
    'teacher_id': [1, 1, 1, 2, 2, 2, 2],
    'subject_id': [2, 2, 3, 1, 2, 3, 4],
    'dept_id':    [3, 4, 3, 1, 1, 1, 1]
}

df_profesores = pd.DataFrame(datos_prueba)

print("--- DATOS DE ENTRADA ---")
print(df_profesores)

# 3. Ejecutamos la función
df_resultado = count_unique_subjects(df_profesores)

print("\n--- RESULTADO FINAL (MATERIAS ÚNICAS) ---")
print(df_resultado)

