"""Introducción a las operaciones básicas con arreglos

Las operaciones básicas con arreglos se refieren a las operaciones matemáticas como la suma, 
la resta, la multiplicación y la división, que se realizan sobre arreglos elemento a elemento.

Consideremos dos arreglos que represetan las temperaturas de ayer y de hoy. Para calcular la diferencia
de temperatura, se resta el arreglo de ayer del arreglo de hoy.

Debemos asegurarnos de que los arreglos tengan la misma forma antes de realizar cualquier operación.

"""

import numpy as np

# Sumas y restas
sales_month1 = np.array([120, 150, 90])
sales_month2 = np.array([130, 160, 80])
total_sales = sales_month1 + sales_month2

print(f"Total ventas: {total_sales}")

difference_sales = sales_month1 - sales_month2
print(f"Diferencia de ventas: {difference_sales}")

# Multiplicación y División
prices = np.array([20, 30, 50])
quantities = np.array([100, 200, 150])
revenue = prices * quantities
print(f"Total ganancia: {revenue}")

total_revenue = np.array([2000, 6000, 7500])
units_sold = np.array([100, 200, 150])
price_per_unit = total_revenue / units_sold
print(f"Precio por unidad: {price_per_unit}")

# Doc Product
""" El producto escalar o producto punto es la suma de los productos de los elementos correspondientes en un arreglo. """
array1 = np.array([1, 2, 3])
array2= np.array([4, 5, 6])
dot_product = np.dot(array1, array2)
print(f"El producto escalar: {dot_product}")
