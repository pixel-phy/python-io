"""Sales Person

+-----------------+---------+
| Column Name     | Type    |
+-----------------+---------+
| sales_id        | int     |
| name            | varchar |
| salary          | int     |
| commission_rate | int     |
| hire_date       | date    |
+-----------------+---------+
sales_id is the primary key (column with unique values) for this table.
Each row of this table indicates the name and the ID of a salesperson alongside their salary, commission rate, and hire date.
 

Table: Company

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| com_id      | int     |
| name        | varchar |
| city        | varchar |
+-------------+---------+
com_id is the primary key (column with unique values) for this table.
Each row of this table indicates the name and the ID of a company and the city in which the company is located.
 

Table: Orders

+-------------+------+
| Column Name | Type |
+-------------+------+
| order_id    | int  |
| order_date  | date |
| com_id      | int  |
| sales_id    | int  |
| amount      | int  |
+-------------+------+
order_id is the primary key (column with unique values) for this table.
com_id is a foreign key (reference column) to com_id from the Company table.
sales_id is a foreign key (reference column) to sales_id from the SalesPerson table.
Each row of this table contains information about one order. This includes the ID of the company, the ID of the salesperson, the date of the order, and the amount paid.
 

Write a solution to find the names of all the salespersons who did not have any orders related to the company with the name "RED".

Return the result table in any order.

    """

import pandas as pd

def sales_person(sales_person: pd.DataFrame, company: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    # Obtenemos el ID de la compañía "RED"
    red_company = company[company['name'] == 'RED']

    # Si la compañía "RED" no existe, todos los vendedores califican
    if red_company.empty:
        return sales_person[['name']]

    red_com_id = red_company['com_id'].values[0]

    # Buscamos los IDs de los vendedores que tienen órdenes con "RED"
    red_sales_ids = orders[orders['com_id'] == red_com_id]['sales_id'].unique()

    # Filtramos la tabla de vendedores
    result = sales_person[~sales_person['sales_id'].isin(red_sales_ids)]

    # Se devuelve la columna de nombres
    return result[['name']]

# 1. Tablas de prueba
sales_data = {
    'sales_id': [1, 2, 3],
    'name': ['Amy', 'Brad', 'Alex'],
    'salary': [50000, 60000, 70000],
    'commission_rate': [10, 12, 14],
    'hire_date': ['2023-01-01', '2024-03-15', '2025-06-01']
}
sales_df = pd.DataFrame(sales_data)

company_data = {
    'com_id': [10, 20],
    'name': ['RED', 'BLUE'],
    'city': ['Boston', 'New York']
}
company_df = pd.DataFrame(company_data)

orders_data = {
    'order_id': [100, 200],
    'com_id': [10, 20],       # 10 es RED, 20 es BLUE
    'sales_id': [1, 2],       # Amy (1) le vendió a RED, Brad (2) a BLUE
    'amount': [1500, 3000]
}
orders_df = pd.DataFrame(orders_data)

# 2. Ejecutar la función
resultado = sales_person(sales_df, company_df, orders_df)

# 3. Mostrar el resultado
print("Vendedores que NO vendieron a 'RED':")
print(resultado)
