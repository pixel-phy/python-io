"""Calculate Special Bonus

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| employee_id | int     |
| name        | varchar |
| salary      | int     |
+-------------+---------+
employee_id is the primary key (column with unique values) for this table.
Each row of this table indicates the employee ID, employee name, and salary.
 

Write a solution to calculate the bonus of each employee. The bonus of an employee is 100% of their salary if the ID of the employee is an odd number and the employee's name does not start with the character 'M'. The bonus of an employee is 0 otherwise.

Return the result table ordered by employee_id.
"""

import pandas as pd

def calculate_special_bonus(employees: pd.DataFrame) -> pd.DataFrame:
    id_impar = employees['employee_id'] % 2 != 0
    no_empieza_con_m = ~employees['name'].str.startswith('M')

    employees['bonus'] = 0

    employees.loc[id_impar & no_empieza_con_m, 'bonus'] = employees['salary']

    resultado = employees[['employee_id', 'bonus']].sort_values(by='employee_id')

    return resultado

# --- 1. Crear datos de prueba ---
data_employees = {
    'employee_id': [2, 3, 7, 8, 9],
    'name': ['Meir', 'Michael', 'Addison', 'Juan', 'Kaleb'],
    'salary': [3000, 3800, 7400, 6100, 7700]
}
df_employees = pd.DataFrame(data_employees)

# --- 2. Ejecutar la función ---
resultado = calculate_special_bonus(df_employees)

# --- 3. Mostrar el resultado ---
print("--- DATOS DE EMPLEADOS ---")
print(df_employees[['employee_id', 'name', 'salary']])
print("\n--- RESULTADO FINAL (BONOS) ---")
print(resultado)
