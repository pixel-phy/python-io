""" Introducción

Estas operaciones estadísticas (básicas) en Python, incluyen la media, mediana, la moda, 
la varianza y la desviación estándar. Son herramientas fundamentales para comprender e interpretar 
datos.
"""

# Media, mediana, moda en Python

import numpy as np
from scipy import stats

grades = np.array([85, 87, 89, 82, 86, 80, 92, 80])
print("Media:", np.mean(grades))
print("Mediana:", np.median(grades))
print("Moda:", stats.mode(grades))

# Otra alternativa para la moda
print("Moda:", stats.mode(grades)[0])

# Varianza y desviación estándar
print("Varianza:", np.var(grades))
print("Desviación estándar:", np.std(grades))
