"""Ejercicio 01: Introduction to Numpy """

# Para utilizar Numpy
import numpy as np

# Crear un arreglo
arr1D = np.array([1, 2, 3, 4, 5])
print(f"Mi primer arreglo usando Numpy: {arr1D}")

# Arreglo de ceros
zeros = np.zeros(5)
print(f"Todos los elementos son ceros: {zeros}")

# Arreglo de unos
unos = np.ones(5)
print(f"Todos los elementos son unos: {unos}")

# Arreglo vacío
empty = np.empty(5)
print(f"Arreglo vacío: {empty}")

# Secuencia de números en un Arreglo en Numpy
sequence = np.arange(0, 10, 2)
print(f"Sequence: {sequence}")
