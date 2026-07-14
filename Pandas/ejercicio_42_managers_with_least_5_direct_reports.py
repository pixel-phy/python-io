""" Managers with at Least 5 Direct Reports

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| name        | varchar |
| department  | varchar |
| managerId   | int     |
+-------------+---------+
id is the primary key (column with unique values) for this table.
Each row of this table indicates the name of an employee, their department, and the id of their manager.
If managerId is null, then the employee does not have a manager.
No employee will be the manager of themself.
 

Write a solution to find managers with at least five direct reports.

Return the result table in any order.

    """

import pandas as pd

def find_managers(employee: pd.DataFrame) -> pd.DataFrame:
    # Cuántos reportes tiene cada managerId
    manager_counts = employee['managerId'].value_counts()

    # Nos quedamos solo con los IDs que tienen 5 o más reportes
    top_managers = manager_counts[manager_counts >= 5].index

    # Buscamos en la tabla original a los empleados cuyo id esté en a lista
    result = employee[employee['id'].isin(top_managers)]

    # Regreamos el nombre de los gerentes
    return result[['name']]

# 1. Crear el DataFrame con un gerente estrella (John) y otro con pocos reportes (Amy)
data = {
    'id': [101, 102, 1, 2, 3, 4, 5, 6],
    'name': ['John', 'Amy', 'Alice', 'Bob', 'Charlie', 'Dan', 'Emma', 'Fred'],
    'department': ['HR', 'IT', 'HR', 'HR', 'HR', 'HR', 'HR', 'IT'],
    'managerId': [None, None, 101, 101, 101, 101, 101, 102] # 5 reportan a 101, 1 reporta a 102
}
employee_df = pd.DataFrame(data)

# 2. Ejecutar la función
resultado = find_managers(employee_df)

# 3. Mostrar el resultado
print("Tabla de Empleados:")
print(employee_df)
print("\nGerentes con al menos 5 reportes directos:")
print(resultado)
