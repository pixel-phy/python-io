"""Fix Names in a Table

+----------------+---------+
| Column Name    | Type    |
+----------------+---------+
| user_id        | int     |
| name           | varchar |
+----------------+---------+
user_id is the primary key (column with unique values) for this table.
This table contains the ID and the name of the user. The name consists of only lowercase and uppercase characters.
 

Write a solution to fix the names so that only the first character is uppercase and the rest are lowercase.

Return the result table ordered by user_id.

"""

import pandas as pd

def fix_names(users: pd.DataFrame) -> pd.DataFrame:
    # 1. Aplicar capitalize a la columna 'name'
    users['name'] = users['name'].str.capitalize()

    # 2. Ordenar el DataFrame por 'user_id' en orden ascendente
    resultado = users.sort_values(by='user_id')

    return resultado

# --- 1. Crear datos de prueba ---
data_users = {
    'user_id': [2, 1, 3],
    'name': ['aLICE', 'bob', 'MArY']
}
df_users = pd.DataFrame(data_users)

# --- 2. Ejecutar la función ---
resultado = fix_names(df_users)

# --- 3. Mostrar el resultado ---
print("--- DATOS ORIGINALES ---")
print(df_users)
print("\n--- RESULTADO FINAL (CORREGIDO Y ORDENADO) ---")
print(resultado)
