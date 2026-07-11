"""Rearrange Products Table

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| product_id  | int     |
| store1      | int     |
| store2      | int     |
| store3      | int     |
+-------------+---------+
product_id is the primary key (column with unique values) for this table.
Each row in this table indicates the product's price in 3 different stores: store1, store2, and store3.
If the product is not available in a store, the price will be null in that store's column.
 

Write a solution to rearrange the Products table so that each row has (product_id, store, price). If a product is not available in a store, do not include a row with that product_id and store combination in the result table.

Return the result table in any order.

    """

import pandas as pd

def rearrange_products_table(products: pd.DataFrame) -> pd.DataFrame:
    # Transformamos la tabla de formato ancho a formato largo
    resultado = pd.melt(
        products, 
        id_vars=['product_id'],                  # La columna que se queda fija
        value_vars=['store1', 'store2', 'store3'], # Las columnas que se van a "desenrollar"
        var_name='store',                         # El nombre de la nueva columna para las tiendas
        value_name='price'                        # El nombre de la nueva columna para los precios
    )
    
    # Eliminamos las filas donde el precio sea NaN (el problema pide no incluirlas)
    resultado.dropna(subset=['price'], inplace=True)
    
    return resultado

# Ejemplo de uso:

data = {
    'product_id': [0, 1],
    'store1': [95, 70],
    'store2': [None, 80],  # None se convertirá en NaN en Pandas
    'store3': [105, None]
}
df_productos = pd.DataFrame(data)

print("--- Tabla de Productos Original (Formato Ancho) ---")
print(df_productos)
print("\n")

# 3. Ejecutamos la transformación
df_transformado = rearrange_products_table(df_productos)

print("--- Tabla Rearreglada (Formato Largo sin Nulos) ---")
print(df_transformado.to_string(index=False)) # Ocultamos el índice para que se vea más limpio
