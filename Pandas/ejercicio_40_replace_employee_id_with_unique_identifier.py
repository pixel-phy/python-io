"""Replace Employee ID With The Unique Identifier

+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| id            | int     |
| name          | varchar |
+---------------+---------+
id is the primary key (column with unique values) for this table.
Each row of this table contains the id and the name of an employee in a company.
 

Table: EmployeeUNI

+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| id            | int     |
| unique_id     | int     |
+---------------+---------+
(id, unique_id) is the primary key (combination of columns with unique values) for this table.
Each row of this table contains the id and the corresponding unique id of an employee in the company.
 

Write a solution to show the unique ID of each user, If a user does not have a unique ID replace just show null.

Return the result table in any order.

    """

import pandas as pd

def replace_employee_id(employee: pd.DataFrame, employee_uni: pd.DataFrame) -> pd.DataFrame:
    # Left Join usando la columna 'id' como llave de unión
    merged_df = pd.merge(employee, employee_uni, on='id', how='left')

    return merged_df[['unique_id', 'name']]

# 1. Crear el DataFrame de Empleados
employees_data = {
    'id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie']
}
employee_df = pd.DataFrame(employees_data)

# 2. Crear el DataFrame de Identificadores Únicos
uni_data = {
    'id': [1, 2],
    'unique_id': [1001, 1002]
}
employee_uni_df = pd.DataFrame(uni_data)

# 3. Ejecutar la función
resultado = replace_employee_id(employee_df, employee_uni_df)

# 4. Mostrar el resultado
print("Tabla de Empleados:")
print(employee_df)
print("\nTabla de IDs Únicos:")
print(employee_uni_df)
print("\nResultado Final:")
print(resultado)
