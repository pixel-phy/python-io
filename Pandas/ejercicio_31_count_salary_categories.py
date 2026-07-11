"""Count Salary Categories

+-------------+------+
| Column Name | Type |
+-------------+------+
| account_id  | int  |
| income      | int  |
+-------------+------+
account_id is the primary key (column with unique values) for this table.
Each row contains information about the monthly income for one bank account.
 

Write a solution to calculate the number of bank accounts for each salary category. The salary categories are:

"Low Salary": All the salaries strictly less than $20000.
"Average Salary": All the salaries in the inclusive range [$20000, $50000].
"High Salary": All the salaries strictly greater than $50000.
The result table must contain all three categories. If there are no accounts in a category, return 0.

Return the result table in any order.

    """

import pandas as pd

def count_salary_categories(accounts: pd.DataFrame) -> pd.DataFrame:
    # 1. Contamos cuántas cuentas caen en cada categoría usando filtros rápidos
    low_count = (accounts['income'] < 20000).sum()
    average_count = ((accounts['income'] >= 20000) & (accounts['income'] <= 50000)).sum()
    high_count = (accounts['income'] > 50000).sum()
    
    # 2. Construimos el DataFrame de salida con la estructura exacta que nos piden
    resultado = pd.DataFrame({
        'category': ['Low Salary', 'Average Salary', 'High Salary'],
        'accounts_count': [low_count, average_count, high_count]
    })
    
    return resultado

data = {
    'account_id': [1, 2, 3, 4],
    'income': [15000, 90000, 18000, 65000]
}
df_cuentas = pd.DataFrame(data)

print("--- Datos de Cuentas Originales ---")
print(df_cuentas)
print("\n" + "-"*40 + "\n")

# Ejecutamos la función
df_reporte = count_salary_categories(df_cuentas)

print("--- Reporte de Categorías Resultante ---")
print(df_reporte.to_string(index=False))
