"""
DataFrame weather
+-------------+--------+
| Column Name | Type   |
+-------------+--------+
| city        | object |
| month       | object |
| temperature | int    |
+-------------+--------+
Write a solution to pivot the data so that each row represents temperatures for a specific
month, and each city is a separate column.
"""

import pandas as pd


def pivotTable(weather: pd.DataFrame) -> pd.DataFrame:
    # Pivotamos la tabla usando 'month' como filas y 'city' como columnas
    return weather.pivot(index="month", columns="city", values="temperature")

# 1. Creamos el DataFrame original en formato "largo"
datos_clima = {
    "city": [
        "Jacksonville",
        "Jacksonville",
        "Jacksonville",
        "Jacksonville",
        "Jacksonville",
        "ElPaso",
        "ElPaso",
        "ElPaso",
        "ElPaso",
        "ElPaso",
    ],
    "month": [
        "January",
        "February",
        "March",
        "April",
        "May",
        "January",
        "February",
        "March",
        "April",
        "May",
    ],
    "temperature": [13, 23, 38, 5, 34, 20, 6, 26, 2, 43],
}

df_weather = pd.DataFrame(datos_clima)

print("--- DATOS ORIGINALES (Formato Largo) ---")
print(df_weather)
print("\n" + "-" * 50 + "\n")

# 2. Llamamos a nuestra función
df_pivotado = pivotTable(df_weather)

print("--- DATOS PIVOTADOS (Formato Ancho) ---")
print(df_pivotado)
