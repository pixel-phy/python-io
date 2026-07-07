"""
DataFrame animals
+-------------+--------+
| Column Name | Type   |
+-------------+--------+
| name        | object |
| species     | object |
| age         | int    |
| weight      | int    |
+-------------+--------+
Write a solution to list the names of animals that weigh strictly more than 100 kilograms.

Return the animals sorted by weight in descending order.
"""

import pandas as pd


def findHeavyAnimals(animals: pd.DataFrame) -> pd.DataFrame:
    # 1. Filtramos los animales que pesan más de 100
    pesados = animals[animals["weight"] > 100]

    # 2. Los ordenamos por peso de mayor a menor
    ordenados = pesados.sort_values(by="weight", ascending=False)

    # 3. Nos quedamos únicamente con la columna 'name'
    return ordenados[["name"]]

# 1. Creamos el DataFrame original con animales de ejemplo
datos_animales = {
    "name": ["Tatiana", "Khaled", "Alex", "Jonathan", "Stefan", "Tommy"],
    "species": ["Elephant", "Giraffe", "Leopard", "Monkey", "Bear", "Panda"],
    "age": [4, 9, 6, 3, 4, 2],
    "weight": [468, 480, 20, 11, 204, 100],  # Tommy pesa exactamente 100
}

df_animals = pd.DataFrame(datos_animales)

print("--- ANIMALES ORIGINALES ---")
print(df_animals)
print("\n" + "-" * 40 + "\n")

# 2. Llamamos a nuestra función
df_resultado = findHeavyAnimals(df_animals)

print("--- ANIMALES DE MÁS DE 100 KG (ORDENADOS) ---")
print(df_resultado)
