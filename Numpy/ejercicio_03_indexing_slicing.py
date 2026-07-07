"""Entendiendo la indexación de arreglos

La indexación de arreglos en Numpy nos permite acceder a un elemento dentro de un arreglo.
Funciona igual que con las listas en Python, donde se utiliza la indexación desde cero, lo que significa
que el primer elemento se encuentra en la posición 0. Así es como accedemos a los elementos. """

import numpy as np

# Indexación de arreglos
print("Indexación de arreglos: ")
arr = np.array([1, 2, 3, 4, 5])
print(arr)
print(arr[0])
print(arr[2])
print(arr[-1])

# Segmentación de arreglos
print("\nSegementación de arreglos:")
print(arr[1:4])
print(arr[::2])

# Modificación de arreglos 
print("\nModificación de elementos en arreglos:")
arr_slice = arr[1:4]
arr_slice[1] = 10

print(arr)

# Indexación y Slicing en arreglos multidimencionales
print("\nArreglo multidimencional: ")
arr_multi = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(arr_multi)

print("\nElemento: ")
print(arr_multi[0, 2])
print("\nFila: ")
print(arr_multi[1])
print("\nColumna:")
print(arr_multi[:,2])

# Slicing en arreglos multidimencionales
print("\nSliging de arreglos multidimencionales: ")
print(arr_multi[:2, :2])
