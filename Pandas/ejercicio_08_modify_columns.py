"""
DataFrame employees
+-------------+--------+
| Column Name | Type   |
+-------------+--------+
| name        | object |
| salary      | int    |
+-------------+--------+
A company intends to give its employees a pay rise.

Write a solution to modify the salary column by multiplying each salary by 2.
"""

import pandas as pd

def modifySalaryColumn(employees: pd.DataFrame) -> pd.DataFrame:
    # Multiplicamos los valores actuales de 'salary' por 2 y los guardamos en la misma columna
    employees["salary"] = employees["salary"] * 2

    # Retornamos el Dataframe modificado
    return employees

# 1. Creamos el DataFrame original con los salarios iniciales
datos_empleados = {
    "name": ["Jack", "Piper", "Mia", "Ulysses"],
    "salary": [19666, 74754, 62509, 54866],
}

df_employees = pd.DataFrame(datos_empleados)

print("--- SALARIOS ORIGINALES ---")
print(df_employees)
print("\n" + "-" * 35 + "\n")

# 2. Llamamos a nuestra función para aplicar el aumento
df_modificado = modifySalaryColumn(df_employees)

print("--- SALARIOS MODIFICADOS (* 2) ---")
print(df_modificado)
