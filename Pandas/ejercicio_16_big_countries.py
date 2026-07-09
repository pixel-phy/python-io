""" Big countries
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| name        | varchar |
| continent   | varchar |
| area        | int     |
| population  | int     |
| gdp         | bigint  |
+-------------+---------+
name is the primary key (column with unique values) for this table.
Each row of this table gives information about the name of a country, the continent to which it belongs, its area, the population, and its GDP value.
 

A country is big if:

it has an area of at least three million (i.e., 3000000 km2), or
it has a population of at least twenty-five million (i.e., 25000000).
Write a solution to find the name, population, and area of the big countries.

Return the result table in any order.
"""

import pandas as pd

def big_countries(world: pd.DataFrame) -> pd.DataFrame:
    # Filtramos las filas donde el área es >= 3.000.000 O la población es >= 25.000.000
    df_filtrado = world[(world['area'] >= 3000000) | (world['population'] >= 25000000)]

    # Seleccionamos únicamente las columnas requeridas
    return df_filtrado[['name', 'population', 'area']]

# Prueba de uso
datos_de_prueba = {
    'name': ['Andorra', 'Australia', 'Brazil', 'Canada', 'Monaco'],
    'continent': ['Europe', 'Oceania', 'South America', 'North America', 'Europe'],
    'area': [468, 7692024, 8515767, 9984670, 2],
    'population': [77000, 25600000, 214300000, 38250000, 39000],
    'gdp': [3154000000, 1326000000000, 1608000000000, 2001000000000, 6810000000]
}

df_mundo = pd.DataFrame(datos_de_prueba)

print("--- DATOS ORIGINALES ---")
print(df_mundo)
print("\n" + "="*40 + "\n")

resultado = big_countries(df_mundo)

print("--- PAÍSES GRANDES (RESULTADO) ---")
print(resultado)
