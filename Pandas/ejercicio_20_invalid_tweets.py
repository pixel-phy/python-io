"""Invalid Tweets

+----------------+---------+
| Column Name    | Type    |
+----------------+---------+
| tweet_id       | int     |
| content        | varchar |
+----------------+---------+
tweet_id is the primary key (column with unique values) for this table.
content consists of alphanumeric characters, '!', or ' ' and no other special characters.
This table contains all the tweets in a social media app.
 

Write a solution to find the IDs of the invalid tweets. The tweet is invalid if the number of characters used in the content of the tweet is strictly greater than 15.

Return the result table in any order.

"""

import pandas as pd

def invalid_tweets(tweets: pd.DataFrame) -> pd.DataFrame:
    # Filtramos los tweets donde la longitud del contenido sea mayor a 15
    invalidos = tweets[tweets['content'].str.len() > 15]

    # Devolvemos la columna 'tweet_id'
    return invalidos[['tweet_id']]

data_tweets = {
    'tweet_id': [1, 2, 3],
    'content': [
        'Vote for ChatGPT',                     # 16 caracteres -> Inválido
        'Let us Code',                          # 11 caracteres -> Válido
        'Pandas is awesome and super powerful'  # 36 caracteres -> Inválido
    ]
}
df_tweets = pd.DataFrame(data_tweets)

resultado = invalid_tweets(df_tweets)

print("--- TODOS LOS TWEETS ---")
print(df_tweets)
print("\n--- RESULTADO (TWEETS INVÁLIDOS) ---")
print(resultado)
