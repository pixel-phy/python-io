""" Recyclable and Low Fat Products

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| product_id  | int     |
| low_fats    | enum    |
| recyclable  | enum    |
+-------------+---------+
product_id is the primary key (column with unique values) for this table.
low_fats is an ENUM (category) of type ('Y', 'N') where 'Y' means this product is low fat and 'N' means it is not.
recyclable is an ENUM (category) of types ('Y', 'N') where 'Y' means this product is recyclable and 'N' means it is not.
 

Write a solution to find the ids of products that are both low fat and recyclable.

"""

import pandas as pd

def find_products(products: pd.DataFrame) -> pd.DataFrame:
    # Filtramos las filas donde ambas condiciones se cumplen
    filtered_df = products[(products['low_fats'] == 'Y') & (products['recyclable'] == 'Y')]
    
    # Retornamos solo la columna product_id como un DataFrame
    return filtered_df[['product_id']]

# Prueba de uso:
data = {
    'product_id': [0, 1, 2, 3, 4],
    'low_fats': ['Y', 'Y', 'N', 'Y', 'N'],
    'recyclable': ['Y', 'N', 'Y', 'Y', 'N']
}
df_productos = pd.DataFrame(data)

# Llamamos a la función y mostramos el resultado
resultado = find_products(df_productos)
print(resultado)
