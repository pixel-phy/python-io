"""
DataFrame products
+-------------+--------+
| Column Name | Type   |
+-------------+--------+
| name        | object |
| quantity    | int    |
| price       | int    |
+-------------+--------+
Write a solution to fill in the missing value as 0 in the quantity column.
"""
import numpy as np
import pandas as pd

def fillMissingValues(products: pd.DataFrame) -> pd.DataFrame:
    # Rellenamos los valores nulos de la columna 'quantity' con 0
    products["quantity"] = products["quantity"].fillna(0)

    # Retornamos el DataFrame modificado
    return products

# 1. Creamos un DataFrame con valores nulos (None) en 'quantity'
datos_productos = {
    "name": ["Wristwatch", "WirelessEarbuds", "GolfClubs", "傳an"],
    "quantity": [None, None, 779, 849],  # Los primeros dos no tienen cantidad
    "price": [135, 30, 110, 60],
}

df_products = pd.DataFrame(datos_productos)

print("--- ANTES DE RELLENAR (Con nulos) ---")
print(df_products)
print("\n" + "-" * 40 + "\n")

# 2. Llamamos a nuestra función
df_rellenado = fillMissingValues(df_products)

print("--- DESPUÉS DE RELLENAR (Con ceros) ---")
print(df_rellenado)
