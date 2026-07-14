"""Students and Examinations

+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| student_id    | int     |
| student_name  | varchar |
+---------------+---------+
student_id is the primary key (column with unique values) for this table.
Each row of this table contains the ID and the name of one student in the school.
 

Table: Subjects

+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| subject_name | varchar |
+--------------+---------+
subject_name is the primary key (column with unique values) for this table.
Each row of this table contains the name of one subject in the school.
 

Table: Examinations

+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| student_id   | int     |
| subject_name | varchar |
+--------------+---------+
There is no primary key (column with unique values) for this table. It may contain duplicates.
Each student from the Students table takes every course from the Subjects table.
Each row of this table indicates that a student with ID student_id attended the exam of subject_name.
 

Write a solution to find the number of times each student attended each exam.

Return the result table ordered by student_id and subject_name.

    """

import pandas as pd

def students_and_examinations(students: pd.DataFrame, subjects: pd.DataFrame, examinations: pd.DataFrame) -> pd.DataFrame:
    students['_key'] = 1
    subjects['_key'] = 1
    all_combinations = pd.merge(students, subjects, on='_key').drop(columns=['_key'])

    # cuántas veces asistió cada estudiante a cada materia
    exam_counts = examinations.groupby(['student_id', 'subject_name']).size().reset_index(name='attended_exams')

    # Unir las combinaciones 
    result = pd.merge(all_combinations, exam_counts, on=['student_id', 'subject_name'], how='left')

    # Los estudiantes que no asistieron tendrán NaN, se cambia por 0
    result['attended_exams'] = result['attended_exams'].fillna(0).astype(int)

    # Se ordena como pide el ejercicio
    return result.sort_values(by=['student_id', 'subject_name']).reset_index(drop=True)

# 1. Datos de prueba
students_df = pd.DataFrame({'student_id': [1, 2], 'student_name': ['Alice', 'Bob']})
subjects_df = pd.DataFrame({'subject_name': ['Math', 'Physics']})

exam_data = {
    'student_id': [1, 1, 2],
    'subject_name': ['Math', 'Math', 'Physics']
}
examinations_df = pd.DataFrame(exam_data)

# 2. Ejecutar la función
resultado = students_and_examinations(students_df, subjects_df, examinations_df)

# 3. Mostrar el resultado
print("Resultado final de asistencias:")
print(resultado)
