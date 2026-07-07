"""
DataFrame report
+-------------+--------+
| Column Name | Type   |
+-------------+--------+
| product     | object |
| quarter_1   | int    |
| quarter_2   | int    |
| quarter_3   | int    |
| quarter_4   | int    |
+-------------+--------+
Write a solution to reshape the data so that each row represents sales data 
for a product in a specific quarter.
"""

import pandas as pd


def meltTable(report: pd.DataFrame) -> pd.DataFrame:
    # "Derretimos" la tabla para pasarla a formato largo
    return pd.melt(
        report,
        id_vars=["product"],
        var_name="quarter",
        value_name="sales",
    )

# 1. Creamos el DataFrame original en formato "ancho"
datos_reporte = {
    "product": ["Umbrella", "SleepingBag"],
    "quarter_1": [417, 519],
    "quarter_2": [224, 730],
    "quarter_3": [379, 44],
    "quarter_4": [611, 738],
}

df_report = pd.DataFrame(datos_reporte)

print("--- DATOS ORIGINALES (Formato Ancho) ---")
print(df_report)
print("\n" + "-" * 55 + "\n")

# 2. Llamamos a nuestra función
df_largo = meltTable(df_report)

print("--- DATOS DERRETIDOS / MELTED (Formato Largo) ---")
print(df_largo)
