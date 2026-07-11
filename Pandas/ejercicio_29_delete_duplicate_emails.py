"""Delete duplicate Emails

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| email       | varchar |
+-------------+---------+
id is the primary key (column with unique values) for this table.
Each row of this table contains an email. The emails will not contain uppercase letters.
 

Write a solution to delete all duplicate emails, keeping only one unique email with the smallest id.

For SQL users, please note that you are supposed to write a DELETE statement and not a SELECT one.

For Pandas users, please note that you are supposed to modify Person in place.

After running your script, the answer shown is the Person table. The driver will first compile and
run your piece of code and then show the Person table. The final order of the Person table does not matter.

    """

import pandas as pd

def delete_duplicate_emails(person: pd.DataFrame) -> None:
    # 1. Se ordena por 'id' de menor a mayor para asegurar que el id más pequeño
    # quede arriba
    person.sort_values(by='id', ascending=True, inplace=True)

    # 2. Se eliminan duplicados
    person.drop_duplicates(subset='email', keep='first', inplace=True)

data = {
    'id': [3, 1, 2, 4],
    'email': ['john@example.com', 'john@example.com', 'bob@example.com', 'bob@example.com']
}
df_personas = pd.DataFrame(data)

print("--- DataFrame Original ---")
print(df_personas)
print("\n" + "-"*30 + "\n")

# Ejecutamos la función (modifica df_personas in-place)
delete_duplicate_emails(df_personas)

print("--- DataFrame Después de la Función ---")
print(df_personas)
