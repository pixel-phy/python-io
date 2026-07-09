""" Problema de Inventarios (EOQ)

Eres el gerente de cadena de suministro de una empresa que vende 5 productos. Necesitas calcular
para cada producto:

La Cantidad Económica de Pedido (EOQ)

El número de pedidos por año

El costo total anual de inventario

La fórmula del EOQ es: EOQ = sqrt((2 * D * S) / H)

Donde:

D = Demanda anual (unidades/año)

S = Costo de ordenar ($/pedido)

H = Costo de mantener inventario ($/unidad/año)

Objetivo del Día:
Crear tu primer DataFrame en Pandas, calcular métricas de inventario y practicar operaciones básicas
con columnas.
"""

import numpy as np
import pandas as pd

data = {
    "Producto": ["A", "B", "C", "D", "E"],
    "Demanda_Anual": [1200, 800, 2500, 600, 1800],
    "Costo_Ordenar": [50, 75, 40, 100, 60],
    "Costo_Mantener": [2.5, 3.0, 1.8, 4.2, 2.2],
}

df = pd.DataFrame(data)

df["EOQ"] = np.sqrt((2 * df["Demanda_Anual"] * df["Costo_Ordenar"]) / df["Costo_Mantener"])
df["EOQ"] = df["EOQ"].round(2)

# Pedidos por año
df["Pedidos_por_año"] = (df["Demanda_Anual"] / df["EOQ"]).round(2)

# Costo total
df["Costo_total"] = ((df["Demanda_Anual"] / df["EOQ"]) * df["Costo_Ordenar"] + (df["EOQ"] / 2) * df["Costo_Mantener"]).round(2)

df["Categoria_EOQ"] = df["EOQ"].apply(lambda x: "Bajo" if x < 100 else ("Medio" if x < 200 else "Alto"))

print("--- PRIMERAS 3 FILAS DEL DATAFRAME ---")
print(df.head(3))
print("\n")

print("--- RESUMEN ESTADÍSTICO ---")
print(df.describe())
print("\n")

print("--- ANÁLISIS DE RESULTADOS ---")

# Producto con mayor y menor EOQ
idx_max_eoq = df["EOQ"].idxmax()
idx_min_eoq = df["EOQ"].idxmin()

print(
    f"Producto con MAYOR EOQ: {df.loc[idx_max_eoq, 'Producto']} ({df.loc[idx_max_eoq, 'EOQ']} unidades)"
)
print(
    f"Producto con MENOR EOQ: {df.loc[idx_min_eoq, 'Producto']} ({df.loc[idx_min_eoq, 'EOQ']} unidades)"
)

# Costo total promedio
costo_promedio = df["Costo_total"].mean()
print(f"Costo total promedio de inventario: ${costo_promedio:.2f}")

# Filtrar productos con Costo Total > $2,000
print("\nProductos con Costo Total mayor a $2,000:")
df_filtrado = df[df["Costo_total"] > 2000]
print(df_filtrado[["Producto", "Costo_total"]])
