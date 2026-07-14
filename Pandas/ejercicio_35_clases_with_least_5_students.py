"""Classes With at Least 5 Students

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| student     | varchar |
| class       | varchar |
+-------------+---------+
(student, class) is the primary key (combination of columns with unique values) for this table.
Each row of this table indicates the name of a student and the class in which they are enrolled.
 

Write a solution to find all the classes that have at least five students.

Return the result table in any order.

    """

import pandas as pd

def find_classes(courses: pd.DataFrame) -> pd.DataFrame:
    # Agrupamos por clase y filtramos aquellas que tengan 5 o más filas
    df_filtered = courses.groupby('class').filter(lambda x : len(x) >= 5)

    # Obtenemos los nombres de las clases únicas y los devolvemos como un nuevo DataFrame
    return pd.DataFrame({'class': df_filtered['class'].unique()})

# 1. Crear el DataFrame de prueba
data = {
    'student': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
    'class': ['Math', 'Math', 'Math', 'Math', 'Math', 'English', 'English']
}
courses_df = pd.DataFrame(data)

# 2. Ejecutar la función
resultado = find_classes(courses_df)

# 3. Mostrar el resultado
print("DataFrame Original:")
print(courses_df)
print("\nClases con al menos 5 estudiantes:")
print(resultado)

