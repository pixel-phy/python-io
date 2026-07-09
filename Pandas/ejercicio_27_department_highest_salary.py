"""Department Highest Salary

+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| id           | int     |
| name         | varchar |
| salary       | int     |
| departmentId | int     |
+--------------+---------+
id is the primary key (column with unique values) for this table.
departmentId is a foreign key (reference columns) of the ID from the Department table.
Each row of this table indicates the ID, name, and salary of an employee. It also contains the ID of their department.
 

Table: Department

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| name        | varchar |
+-------------+---------+
id is the primary key (column with unique values) for this table. It is guaranteed that department name is not NULL.
Each row of this table indicates the ID of a department and its name.
 

Write a solution to find employees who have the highest salary in each of the departments.

Return the result table in any order.

"""

import pandas as pd

def department_highest_salary(employee: pd.DataFrame, department: pd.DataFrame) -> pd.DataFrame:

    df_combinado = employee.merge(department, left_on='departmentId', right_on='id', suffixes=('_emp', '_dept'))

    salario_max_por_dept = df_combinado.groupby('departmentId')['salary'].transform('max')

    empleados_top = df_combinado[df_combinado['salary'] == salario_max_por_dept]

    resultado = empleados_top[['name_dept', 'name_emp', 'salary']].rename(
        columns={
            'name_dept': 'Department',
            'name_emp': 'Employee',
            'salary': 'Salary'
        }
    )
    
    return resultado

# --- 1. Crear datos de prueba ---
df_emp = pd.DataFrame({
    'id': [1, 2, 3, 4],
    'name': ['Joe', 'Jim', 'Henry', 'Sam'],
    'salary': [70000, 90000, 80000, 90000],
    'departmentId': [1, 1, 2, 1]  # Joe, Jim y Sam son de TI (1)
})

df_dept = pd.DataFrame({
    'id': [1, 2],
    'name': ['IT', 'Sales']
})

# --- 2. Ejecutar la función ---
resultado = department_highest_salary(df_emp, df_dept)

print("--- RESULTADO FINAL ---")
print(resultado)
