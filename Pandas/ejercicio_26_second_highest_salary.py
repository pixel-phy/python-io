"""Second Highest Salary

+-------------+------+
| Column Name | Type |
+-------------+------+
| id          | int  |
| salary      | int  |
+-------------+------+
id is the primary key (column with unique values) for this table.
Each row of this table contains information about the salary of an employee.
 
Write a solution to find the second highest distinct salary from the Employee table. 
If there is no second highest salary, return null (return None in Pandas).

"""

import pandas as pd

def second_highest_salary(employee: pd.DataFrame) -> pd.DataFrame:
    # 1. Obtener los salarios únicos y ordenarlos de mayor a menor
    salarios_unicos = employee['salary'].drop_duplicates().sort_values(ascending=False)
    
    # 2. Verificar si hay al menos 2 salarios distintos
    if len(salarios_unicos) < 2:
        return pd.DataFrame({'SecondHighestSalary': [None]})
    
    # 3. El segundo salario más alto estará en la posición física 1 (índice 0 es el 1ero)
    second_salary = salarios_unicos.iloc[1]
    
    return pd.DataFrame({'SecondHighestSalary': [second_salary]})

# --- 1. Crear datos de prueba (Sin segundo salario más alto) ---
data_employee = {
    'id': [1, 2],
    'salary': [5000, 5000]
}
df_employee = pd.DataFrame(data_employee)

# --- 2. Ejecutar la función ---
resultado = second_highest_salary(df_employee)
print(resultado)
