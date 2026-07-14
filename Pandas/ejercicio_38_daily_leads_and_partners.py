"""Daily Leads and Partners

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| date_id     | date    |
| make_name   | varchar |
| lead_id     | int     |
| partner_id  | int     |
+-------------+---------+
There is no primary key (column with unique values) for this table. It may contain duplicates.
This table contains the date and the name of the product sold and the IDs of the lead and partner it was sold to.
The name consists of only lowercase English letters.
 

For each date_id and make_name, find the number of distinct lead_id's and distinct partner_id's.

Return the result table in any order.

    """

import pandas as pd

def daily_leads_and_partners(daily_sales: pd.DataFrame) -> pd.DataFrame:
    # Se agrupan por fecha y marca de auto
    result = daily_sales.groupby(['date_id', 'make_name']).agg(
        unique_leads=('lead_id', 'nunique'),
        unique_partners=('partner_id', 'nunique')
    ).reset_index()

    return result

# 1. Crear el DataFrame de prueba
data = {
    'date_id': ['2026-07-14', '2026-07-14', '2026-07-14', '2026-07-15', '2026-07-15'],
    'make_name': ['toyota', 'toyota', 'toyota', 'toyota', 'honda'],
    'lead_id': [0, 1, 0, 1, 2],
    'partner_id': [1, 2, 1, 3, 1]
}
daily_sales_df = pd.DataFrame(data)

# 2. Ejecutar la función
resultado = daily_leads_and_partners(daily_sales_df)

# 3. Mostrar el resultado
print("DataFrame Original de Ventas:")
print(daily_sales_df)
print("\nResultado (Leads y Partners únicos):")
print(resultado)
