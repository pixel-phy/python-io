"""Entendiendo la indexación de arreglos

La indexación de arreglos en Numpy nos permite acceder a un elemento dentro de un arreglo.
Funciona igual que con las listas en Python, donde se utiliza la indexación desde cero, lo que significa
que el primer elemento se encuentra en la posición 0. Así es como accedemos a los elementos. """

import numpy as np

print("Indexación de arreglos: ")
arr = np.array([1, 2, 3, 4, 5])
print(arr)
print(arr[0])
print(arr[2])
print(arr[-1])
print("\nSegementación de arreglos:")
print(arr[1:4])
print(arr[::2])

print("\nModificación de elementos en arreglos:")
arr_slice = arr[1:4]
arr_slice[1] = 10

print(arr)
