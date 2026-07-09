""" Customers who never Order

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| name        | varchar |
+-------------+---------+
id is the primary key (column with unique values) for this table.
Each row of this table indicates the ID and name of a customer.
 

Table: Orders

+-------------+------+
| Column Name | Type |
+-------------+------+
| id          | int  |
| customerId  | int  |
+-------------+------+
id is the primary key (column with unique values) for this table.
customerId is a foreign key (reference columns) of the ID from the Customers table.
Each row of this table indicates the ID of an order and the ID of the customer who ordered it.
 

Write a solution to find all customers who never order anything.

Return the result table in any order.
"""

import pandas as pd

def find_customers(customers: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    # 1. Filtramos los clientes cuyo 'id' NO esté en la columna 'customerId' de órdenes
    df_filtrado = customers[~customers['id'].isin(orders['customerId'])]

    # 2. Seleccionamos la columna 'name' y le renombramos el encabezado a 'Customers'
    resultado = df_filtrado[['name']].rename(columns={'name': 'Customers'})

    return resultado

# Tabla de Clientes
data_customers = {
    'id': [1, 2, 3, 4],
    'name': ['Joe', 'Henry', 'Sam', 'Max']
}
df_customers = pd.DataFrame(data_customers)

# Tabla de Órdenes
data_orders = {
    'id': [1, 2],
    'customerId': [3, 1]  # Sam (3) y Joe (1) han comprado
}
df_orders = pd.DataFrame(data_orders)

# --- 2. Ejecutar la función ---
resultado = find_customers(df_customers, df_orders)

# --- 3. Mostrar el resultado ---
print("--- TABLA DE CLIENTES ---")
print(df_customers)
print("\n--- TABLA DE ÓRDENES ---")
print(df_orders)
print("\n--- RESULTADO FINAL ---")
print(resultado)
