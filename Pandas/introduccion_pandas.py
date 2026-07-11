""" Introducción a DataFrames

En pandas un DataFrame es como una mesa, donde los datos son los platos. Un DataFrame a partir 
de una lista o un diccionario es muy sencillo de crear con Pandas. """

import pandas as pd     # Si importa la librería

# DataFrame desde una lista

data_list = ['apple', 'banana', 'cherry']
df_list = pd.DataFrame(data_list, columns=['fruit'])
print(df_list)

# DataFrame desde un diccionario
data_dict = {'fruit': ['apple', 'banana', 'cherry'], 
             'Count': [10, 20, 15]}
df_dict = pd.DataFrame(data_dict)
print("\n", df_dict)

# Visualizando los datos en un DataFrame: Head and Tail
print(f"\nDatos con Head: {df_list.head()}")    # Primeras 5 filas del DataFrame

print(f"\nDatos con Tail: {df_list.tail()}")    # Últimas 5 filas del DataFrame

# Visualizar información de un DataFrame
print("\nInformación: ")
print(df_list.info())
print(df_dict.info())

# Concatenación de DataFrames: pd.concat
print("\nConcatenación de DatraFrames: ")

data1 = {'Estibas': ['Arroz', 'Panela', 'Leche', 'Huevos'], 'Count': [50, 155, 22, 60]}
df_data1 = pd.DataFrame(data1)

data2 = {'Estibas': ['Detergente', 'Jabón en barra', 'Jabón líquido', 'Cloro'], 'Count': [18, 16, 12, 9]}
df_data2 = pd.DataFrame(data2)

# Concatenación DataFrames
df_combined = pd.concat([df_data1, df_data2], ignore_index=True)
print(df_combined)

# Series
print("\nSeries:")

fruver = ['banana', 'platano', 'mandarina', 'pera']
series = pd.Series(fruver)

print(series)
