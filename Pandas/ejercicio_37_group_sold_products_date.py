"""Group Sold Products By The Date

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| sell_date   | date    |
| product     | varchar |
+-------------+---------+
There is no primary key (column with unique values) for this table. It may contain duplicates.
Each row of this table contains the product name and the date it was sold in a market.
 

Write a solution to find for each date the number of different products sold and their names.

The sold products names for each date should be sorted lexicographically.

Return the result table ordered by sell_date.

    """

import pandas as pd

def categorize_products(activities: pd.DataFrame) -> pd.DataFrame:
    # Eliminamos filas duplicadas para no contar el mismo producto
    df_unique = activities.drop_duplicates()

    # Agrupamos por fecha y aplicamos las agregaciones correspondientes
    result = df_unique.groupby('sell_date').agg(
        num_sold=('product', 'count'), # Cuenta los productos únicos de ese día
        products=('product', lambda x: ','.join(sorted(x))) # Los ordena y los une con comas
    ).reset_index()

    # Ordenamos el resultado final por fecha
    return result.sort_values(by='sell_date')

# 1. Crear el DataFrame de prueba
data = {
    'sell_date': ['2026-07-14', '2026-07-14', '2026-07-14', '2026-07-15', '2026-07-15', '2026-07-15'],
    'product': ['Aspirin', 'Penicillin', 'Aspirin', 'Mask', 'Lipstick', 'Backpack']
}
activities_df = pd.DataFrame(data)

# 2. Ejecutar la función
resultado = categorize_products(activities_df)

# 3. Mostrar el resultado
print("DataFrame Original de Actividades:")
print(activities_df)
print("\nResultado Agrupado y Ordenado:")
print(resultado)
