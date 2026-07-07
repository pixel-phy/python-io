"""
DataFrame employees
+-------------+--------+
| Column Name | Type.  |
+-------------+--------+
| name        | object |
| salary      | int.   |
+-------------+--------+
A company plans to provide its employees with a bonus.

Write a solution to create a new column name bonus that contains the doubled values of the salary column.
"""

import pandas as pd

def createBonusColumn(employees: pd.DataFrame) -> pd.DataFrame:
    employees["bonus"] = employees["salary"] * 2

    return employees

# 1. Creamos el DataFrame con salarios de ejemplo
datos_empleados = {
    "name": ["Piper", "Grace", "Georgia", "Willow"],
    "salary": [4548, 28150, 1103, 6593],
}

df_employees = pd.DataFrame(datos_empleados)

print("--- ANTES DEL BONUS ---")
print(df_employees)
print("\n" + "-" * 30 + "\n")

# 2. Llamamos a nuestra función
df_resultado = createBonusColumn(df_employees)

print("--- DESPUÉS DEL BONUS ---")
print(df_resultado)
