""" Customer Placing the Largest Number of Orders

+-----------------+----------+
| Column Name     | Type     |
+-----------------+----------+
| order_number    | int      |
| customer_number | int      |
+-----------------+----------+
order_number is the primary key (column with unique values) for this table.
This table contains information about the order ID and the customer ID.
 

Write a solution to find the customer_number for the customer who has placed the largest number of orders.

The test cases are generated so that exactly one customer will have placed more orders than any other customer.

    """

import pandas as pd

def largest_orders(orders: pd.DataFrame) -> pd.DataFrame:
    # Si el DataFrame está vacío, retornamos un DataFrame vacío
    if orders.empty:
        return pd.DataFrame(columns=['customer_number'])

    top_customer = orders['customer_number'].value_counts().idxmax()

    # Se retorna el resultado como DataFrame
    return pd.DataFrame({'customer_number': [top_customer]})

# 1. Crear el DataFrame de prueba
data = {
    'order_number': [1, 2, 3, 4, 5, 6],
    'customer_number': [100, 200, 200, 300, 200, 300]
}
orders_df = pd.DataFrame(data)

# 2. Ejecutar la función
resultado = largest_orders(orders_df)

# 3. Mostrar el resultado
print("DataFrame de Órdenes:")
print(orders_df)
print("\nCliente con el mayor número de órdenes:")
print(resultado)
