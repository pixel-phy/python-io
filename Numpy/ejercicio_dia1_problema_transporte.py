"""
Imagina que eres un analista de logística. Tienes 3 fábricas (orígenes) y 4 centros de distribución (destinos).
Los costos de envío por unidad desde cada fábrica a cada destino se representan en una matriz. Tu tarea de hoy
es crear y manipular esa matriz, que es el dato fundamental para un problema clásico de transporte.

"""
import numpy as np

# Creación de la matriz de costos (C)
C = np.array([
    [8, 6, 10, 9],  # Fábrica 1
    [9, 12, 13, 7], # Fábrica 2
    [14, 9, 16, 5]  # Fábrica 3
])

# Creación del Vector de Oferta (o)
o = np.array([150, 200, 180])

# Creación del Vector Demanda (d)
d = np.array([130, 120, 150, 130])

# Verificación de Atributos
print("--- Datos ---")
print(f"Matriz de Costos (C): \n{C}")
print(f"Dimensiones de C: {C.shape} \n")

print(f"Vector de Oferta (o): {o}")
print(f"Dimensiones de o: {o.shape} \n")

print(f"Vector de Demanda (d): {d}")
print(f"Dimensiones de d: {d.shape}\n")

oferta_total = np.sum(o)
demanda_total = np.sum(d)
print(f"Oferta total: {oferta_total} | Demanda total: {demanda_total}")
print(f"Balanceado: {oferta_total == demanda_total}\n")

# Slicing
fila_fabrica_2 = C[1, :]
print(f"Costos de la fábrica 2 a todos los destinos: {fila_fabrica_2}")

columna_destino_3 = C[:, 2]
print(f"Costos de todas las fábricas al Destino 3: {columna_destino_3}")

costo_f3_d2 = C[2, 1]
print(f"Costo específico Fábrica 3 -> Destino 2: ${costo_f3_d2}\n")

# Costo total
suma_costos = np.sum(C)
costo_total_hipotetico = suma_costos * oferta_total

print(f"Suma de todos los costos unitarios: ${suma_costos}")
print(f"Costo total hipotético del sistema: ${costo_total_hipotetico}")
