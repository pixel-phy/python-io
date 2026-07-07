"""
    DataFrame customers
+-------------+--------+
| Column Name | Type   |
+-------------+--------+
| customer_id | int    |
| name        | object |
| email       | object |
+-------------+--------+
There are some duplicate rows in the DataFrame based on the email column.

Write a solution to remove these duplicate rows and keep only the first occurrence.

"""
import pandas as pd

def dropDuplicateEmails(customers: pd.DataFrame) -> pd.DataFrame:
    # Eliminamos duplicados basados en la columna 'email', conservando la primera ocurrencia
    return customers.drop_duplicates(subset=["email"], keep="first")

# 1. Creamos el DataFrame de prueba con correos duplicados
datos_clientes = {
    "customer_id": [1, 2, 3, 4],
    "name": ["Ella", "David", "Avatar", "Evan"],
    "email": [
        "emily@example.com",
        "david@example.com",
        "emily@example.com",
        "evan@example.com",
    ],
}

df_customers = pd.DataFrame(datos_clientes)

print("--- DATOS ORIGINALES (Con duplicados) ---")
print(df_customers)
print("\n" + "-" * 45 + "\n")

# 2. Llamamos a nuestra función
df_limpio = dropDuplicateEmails(df_customers)

print("--- DATOS LIMPIOS (Sin duplicados) ---")
print(df_limpio)
