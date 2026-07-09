"""Nth Highest Salary

+-------------+------+
| Column Name | Type |
+-------------+------+
| id          | int  |
| salary      | int  |
+-------------+------+
id is the primary key (column with unique values) for this table.
Each row of this table contains information about the salary of an employee.
 

Write a solution to find the nth highest distinct salary from the Employee table.
If there are less than n distinct salaries, return null.
"""

import pandas as pd

def nth_highest_salary(employee: pd.DataFrame, N: int) -> pd.DataFrame:
    # 1. Obtener los salarios únicos y ordenarlos de mayor a menor
    salarios_unicos = employee['salary'].drop_duplicates().sort_values(ascending=False)
    
    # El nombre de la columna resultado que exige el problema suele ser 'getNthHighestSalary(N)'
    col_name = f'getNthHighestSalary({N})'
    
    # 2. Verificar si N es válido (no es negativo/cero y está dentro del rango)
    if N <= 0 or N > len(salarios_unicos):
        return pd.DataFrame({col_name: [None]})
    
    # 3. Extraer el valor en la posición N-1 (.iloc maneja posiciones físicas de base 0)
    nth_salary = salarios_unicos.iloc[N - 1]
    
    return pd.DataFrame({col_name: [nth_salary]})

# --- 1. Crear datos de prueba (Tabla de Empleados) ---
data_employee = {
    'id': [1, 2, 3, 4],
    'salary': [100, 200, 300, 300]  # El 300 está duplicado
}
df_employee = pd.DataFrame(data_employee)

print("--- TABLA ORIGINAL ---")
print(df_employee)

# --- 2. Caso 1: Buscar el 2do salario más alto (N = 2) ---
resultado_2 = nth_highest_salary(df_employee, N=2)
print("\n--- CASO 1: N = 2 ---")
print(resultado_2)

# --- 3. Caso 2: Buscar el 4to salario más alto (N = 4) ---
# Como solo hay 3 salarios distintos (300, 200, 100), el 4to no existe.
resultado_4 = nth_highest_salary(df_employee, N=4)
print("\n--- CASO 2: N = 4 ---")
print(resultado_4)
