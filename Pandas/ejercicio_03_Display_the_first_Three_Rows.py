"""
DataFrame: employees
+-------------+--------+
| Column Name | Type   |
+-------------+--------+
| employee_id | int    |
| name        | object |
| department  | object |
| salary      | int    |
+-------------+--------+
Write a solution to display the first 3 rows of this DataFrame.

"""

import pandas as pd

def selectFirstRows(employees: pd.DataFrame) -> pd.DataFrame:
    return employees.head(3)

datos_empleados = {
    "employee_id": [3, 90, 9, 60, 49, 43],
    "name": ["Bob", "Alice", "Tatiana", "Annabelle", "Jonathan", "Khaled"],
    "department": [
        "Operations",
        "Sales",
        "Engineering",
        "InformationTechnology",
        "HumanResources",
        "Administration",
    ],
    "salary": [48675, 11096, 33805, 37678, 23793, 40454],
}

df_total = pd.DataFrame(datos_empleados)

print("--- DATOS ORIGINALES (6 filas) ---")
print(df_total)
print("\n" + "-" * 40 + "\n")


df_resultado = selectFirstRows(df_total)

print("--- RESULTADO DE LA FUNCIÓN (Primeras 3 filas) ---")
print(df_resultado)
