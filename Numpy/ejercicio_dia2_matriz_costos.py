"""
    El indexado booleano (filtrado condicional), operaciones técnicas y funciones de 
agregación como .mean() y .max(), todo aplicado a la matriz de costos.
    """

import numpy as np

# Utilizamos la misma matriz de costos del día 1

C = np.array([
    [8, 6, 10, 9],
    [9, 12, 13, 7],
    [14, 9, 16, 5]
])

print("Matriz original: ")
print(C)
print("\n")

print("a. Identificar rutas caras: ")
# Crear la máscara booleana
mascara_caras = C > 12
print("Máscara booleana (costo > 12): \n", mascara_caras)

# Constar cuántas rutas caras hay
total_caras = np.sum(mascara_caras)
print(f"\nCantidad de rutas caras: {total_caras}")

# Mostrar coordenadas (fila, columna)
coordenadas_caras = np.where(mascara_caras)
print("Coordenadas (fila, columna):")
for fila, col in zip(coordenadas_caras[0], coordenadas_caras[1]):
    print(f" -> Ruta en Fábrica (Fila) {fila}, Destino (Columna) {col}")
print("\n")

print("b. Análisis de sensibilidad: ")
# Costo promedio de cada fábrica (filas)
promedio_fabricas = np.mean(C, axis=1)
print(f"Costo promedio por fábrica (filas): {promedio_fabricas}")

# Costo máximo de cada destino (columnas)
max_destinos = np.max(C, axis=0)
print(f"Costo máximo por destino (columnas): {max_destinos}")

# Ruta más barata y más cara (valores e índices planos)
min_valor = C.min()
max_valor = C.max()
idx_min = C.argmin()
idx_max = C.argmax()

print(f"Ruta más barata (valor): {min_valor} (Índice plano: {idx_min})")
print(f"Ruta más cara (Valor): {max_valor} (Índice plano: {idx_max})")

# Opcional: Coordenadas exactas de los extremos
coord_min = np.unravel_index(idx_min, C.shape)
coord_max = np.unravel_index(idx_max, C.shape)
print(f" -> Coordenada exacta de la más barata: {coord_min}")
print(f" -> Coordenada exacta de la más cara: {coord_max}")

print("\n")
print("c. Simulación de escenario: ")
# Copia de la matriz
C_descuento = C.copy().astype(float)

# Aplicar 10% de descuento a rutas > 10
C_descuento[C_descuento > 10] *= 0.9

print("Matriz con el 10% de descuento aplicado a rutas > $10:\n", C_descuento)
print("\n")

print("Desafío extra (categorización)")
matriz_categorizada = np.where(C < 10, 0, np.where(C <= 13, 1, 2))

print("Matriz categorizada (0: Barato, 1: Medio, 2: Alto):\n", matriz_categorizada)
