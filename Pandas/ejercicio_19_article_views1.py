""" Article Views I

+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| article_id    | int     |
| author_id     | int     |
| viewer_id     | int     |
| view_date     | date    |
+---------------+---------+
There is no primary key (column with unique values) for this table, the table may have duplicate rows.
Each row of this table indicates that some viewer viewed an article (written by some author) on some date. 
Note that equal author_id and viewer_id indicate the same person.
 

Write a solution to find all the authors that viewed at least one of their own articles.

Return the result table sorted by id in ascending order.

"""

import pandas as pd

def article_views(views: pd.DataFrame) -> pd.DataFrame:
    # Filtro del autor es el mismo visor
    propios_vistos = views[views['author_id'] == views['viewer_id']]

    # Solo nos quedamos con la columna 'author_id' y eliminar duplicados
    autores_unicos = propios_vistos[['author_id']].drop_duplicates()

    # Se renombra la columna a 'id' y se ordena de forma ascendente
    resultado = autores_unicos.rename(columns={'author_id': 'id'}).sort_values(by='id')

    return resultado

data_views = {
    'article_id': [1, 2, 3, 3, 4, 1],
    'author_id':  [3, 7, 5, 5, 2, 3],
    'viewer_id':  [5, 6, 5, 5, 1, 3], 
    'view_date':  ['2026-08-01', '2026-08-02', '2026-08-02', '2026-08-03', '2026-08-04', '2026-08-05']
}
df_views = pd.DataFrame(data_views)

# --- 2. Ejecutar la función ---
resultado = article_views(df_views)

# --- 3. Mostrar el resultado ---
print("--- TABLA ORIGINAL DE VISTAS (views) ---")
print(df_views)
print("\n--- RESULTADO FINAL ---")
print(resultado)
