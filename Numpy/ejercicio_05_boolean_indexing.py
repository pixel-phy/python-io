"""
Introducción a la indexación Booleana

Esta indexación nos permite acceder a los elementos de un array según ciertas
condiciones, en lugar de usar indices explícitos. """

import numpy as np

data = np.array([12, 43, 36, 32, 51, 18, 79, 7])
print("Data:", data)

# Máscara booleana
bool_array = data > 30
print("Arreglo booleano:", bool_array)

# Selección de data
filtered_data = data[bool_array]
print("Filtered Data:", filtered_data)

# Condición de filtro complejo
prices = np.array([15, 30, 45, 10, 20, 35, 50])
print("Prices: ", prices)

filtered_prices = prices[(prices > 20) & (prices < 60)]
print("Filtered Prices (20 < price < 40): ", filtered_prices)

filtered_prices_or = prices[(prices < 15) | (prices > 45)]
print("Filtered Prices (price < 15 OR price > 15): ", filtered_prices_or)

# Indexación Avanzada
data1 = np.array([11, 22, 33, 44, 55, 66, 77])
print("Datos: ", data1)

fancy_indexes = np.array([0, 2, 4])
fancy_data = data1[fancy_indexes]
print("Datos de Indexación Avanzada: ", fancy_data)

# Otro ejemplo de indexación avanzada
ages = np.array([15, 22, 27, 35, 41, 56, 63, 74, 81])
print("Arreglo inicial de edades: ", ages)

indexes = np.array([1, 4, 6])
fetched_ages = ages[indexes]
print("Fetched Ages: ", fetched_ages)
