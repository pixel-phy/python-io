"""Find Users With Valid E-Mails

+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| user_id       | int     |
| name          | varchar |
| mail          | varchar |
+---------------+---------+
user_id is the primary key (column with unique values) for this table.
This table contains information of the users signed up in a website. Some e-mails are invalid.
 

Write a solution to find the users who have valid emails.

A valid e-mail has a prefix name and a domain where:

The prefix name is a string that may contain letters (upper or lower case), digits, underscore '_', period '.', and/or dash '-'. The prefix name must start with a letter.
The domain must be exactly '@leetcode.com' in lowercase.
Return the result table in any order.

"""

import pandas as pd

def valid_emails(users: pd.DataFrame) -> pd.DataFrame:

    regex_valido = r'^[a-zA-Z][a-zA-Z0-9_.-]*@leetcode\.com$'
    
    # Filtrar usando str.match
    resultado = users[users['mail'].str.match(regex_valido, na=False)]
    
    return resultado

# --- 1. Crear datos de prueba ---
data_users = {
    'user_id': [1, 2, 3, 4, 5],
    'name': ['Winston', 'Jonathan', 'Annabelle', 'Sally', 'Marwan'],
    'mail': [
        'winston@leetcode.com',      # Válido
        'jonathanisgreat',           # Inválido (Falta dominio)
        'bella-r_g.1@leetcode.com',  # Válido (Caracteres especiales permitidos)
        '.sally@leetcode.com',       # Inválido (Empieza con punto)
        'marwan@leetcode.com.com'    # Inválido (Dominio incorrecto al final)
    ]
}
df_users = pd.DataFrame(data_users)

# --- 2. Ejecutar la función ---
resultado = valid_emails(df_users)

# --- 3. Mostrar el resultado ---
print("--- RESULTADO DE CORREOS VÁLIDOS ---")
print(resultado)
